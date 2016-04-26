#! /usr/bin/python
# -*- coding: utf-8 -*-

from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color



# Funciones auxiliares para variar un parametro entre -10 y 10
def conv(val, min, max):
	return (max - min) * (val+10)/20 + min

def fconv(val, min, max):
	return (max - min) * (float(val)+10)/20 + min


# Clase para manejar la webcam y hacer capturas
class Projector:
	# Constructor
	def __init__(self, sources):
		self.sources = sources
		self.frames = []
		self.img = Image(width = 600, height = 600)
		self.scale = -3
		self.persp = 0
		self.applyFX = False
		self.levelBlack = -10
		self.levelWhite = 0
		self.levelGamma = 0
	
	# Devolver imagen
	def getImage(self):
		return self.img
	
	# Capturar un fotograma
	def getFrame(self, source):
		source.capture()
		img = source.getImage().clone()

		# Calculo de dimensiones
		hHeight = conv(self.scale, 10, 100)*320 / 100
		hWidth = hHeight*133 / 100
		hDiff = (hWidth - hHeight) / 2
		
		# Redimensionar y recortar plano
		#img = Image(filename='captura.png')
		img.resize(hWidth, hHeight)
		img.crop(hDiff, 0, hWidth - hDiff - 1, hHeight - 1)

		# Voltear para compensar el reflejo
		img.flop()

		dim = img.height
		iBase = Image(width=dim, height=dim)
		
		with Drawing() as dCompo:
			dCompo.fill_color = Color('green')
			dCompo.rectangle(left=0, top=0, width=iBase.width, height=iBase.height)

			# Crear composicion
			dCompo.composite(operator='copy', left=0, top=0, width=img.width, height=img.height, image=img)
			dCompo(iBase)
			img = iBase

		# Redimensionar
		img.resize(hHeight, hHeight)

		return img;

	# Capturar los cuatro fotogramas
	def capture(self):
		self.frames = []

		for source in self.sources:
			img = self.getFrame(source)

			# Calculo de dimensiones
			hHeight = img.height
			hWidth = img.width
			hDiff = (hWidth - hHeight) / 2

			# Ajustes de imagen
			img.level(
				fconv(self.levelBlack, 0, 0.5),
				fconv(self.levelGamma, 0, 2),
				fconv(self.levelWhite, 0.5, 1.5))

			# Aplicar efectos
			if self.applyFX:
				img.modulate(saturation=0)
				img.evaluate(operator='set', value=0, channel='red')
				img.evaluate(operator='set', value=0, channel='blue')
		
			# Correcion de perspectiva
			# (x,y) -> (x',y')
			img.virtual_pixel='black'
			d=hHeight-1
			p=hHeight/2 * (conv(self.persp, 0, 10) - 5)/10

			if p > 0:
				img.distort('perspective',
					[0,0,     0,0,	#top-left
					 d,0,     d,0,	#top-rigth
					 0,d,   p/2,d-2*p,	#bottom-left
					 d,d, d-p/2,d-2*p])	#bottom-right
			else:
				img.distort('perspective',
					[0,0, 0-p/2,0-2*p,	#top-left
					 d,0, d+p/2,0-2*p,	#top-rigth
					 0,d,     0,d,	#bottom-left
					 d,d,     d,d])	#bottom-right

			#~ if p > 0:
				#~ img.distort('perspective',
					#~ [0,0,   -p,p,	#top-left
					 #~ d,0,  d+p,p,	#top-rigth
					 #~ 0,d,    p,d-p,	#bottom-left
					 #~ d,d,  d-p,d-p])	#bottom-right
			#~ else:
				#~ img.distort('perspective',
					#~ [0,0,    0-p,0-p,	#top-left
					 #~ d,0,  d+p/2,0-p,	#top-rigth
					 #~ 0,d,      p,d+p,	#bottom-left
					 #~ d,d,    d-p,d+p])	#bottom-right

			self.frames.append(img)

		for source in self.sources:
			img = source.reset()
		
		n = len(self.frames)
		if n == 1:
			self.frames.append(self.frames[0])
			self.frames.append(self.frames[0])
			self.frames.append(self.frames[0])
		elif n == 2:
			self.frames.append(self.frames[0].clone())
			self.frames[1].flop()
			self.frames.append(self.frames[1].clone())
			self.frames[3].flop()
		elif n == 3:
			self.frames.append(self.frames[1])

	# Realizar la composicion para la proyeccion
	def compose(self):
		# Calculo de dimensiones
		hHeight = self.frames[0].height
		hWidth = self.frames[0].width
		hDiff = (hWidth - hHeight) / 2

		iBase = Image(width=3*hHeight, height=3*hHeight)

		with Drawing() as dCompo:
			dCompo.fill_color = Color('black')
			dCompo.line((0, 0), iBase.size)
			dCompo.rectangle(left=0, top=0, width=iBase.width, height=iBase.height)

			# Crear composicion
			img = self.frames[0].clone()
			dCompo.composite(operator='copy', left=hHeight, top=0, width=img.width, height=img.height, image=img)

			img = self.frames[1].clone()
			img.rotate(90)
			dCompo.composite(operator='copy', left=2*hHeight, top=hHeight, width=img.width, height=img.height, image=img)

			img = self.frames[2].clone()
			img.rotate(180)
			dCompo.composite(operator='copy', left=hHeight, top=2*hHeight, width=img.width, height=img.height, image=img)

			img = self.frames[3].clone()
			img.rotate(270)
			dCompo.composite(operator='copy', left=0, top=hHeight, width=img.width, height=img.height, image=img)

			dCompo(iBase)
			self.img = iBase
			#self.img = self.frames[0].clone() ###
