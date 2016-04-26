#! /usr/bin/python
# -*- coding: utf-8 -*-

from os import curdir, sep


# Funciones auxiliares para variar un parametro entre -10 y 10
def up(n, k = 1):
	v = n+k
	if v <= 10:
		return v
	else:
		return 10

def down(n, k = 1):
	v = n-k
	if v >= -10:
		return v
	else:
		return -10


# Clase para ejecutar las ordenes que se reciben por HTTP y actualizar la proyeccion
class HoloHandler:
	def __init__(self, http_root, projection):
		self.http_root = http_root
		self.projection = projection
		self.mimetype='text/plain'
		self.response = ""
	
	def handle(self, path):
		# Comprobar peticion  y seleccionar el tipo mime adecuado
		mode = 2
		self.mimetype='text/plain'

		# Captura de webcam
		if path.startswith("/output.jpg"):
			mode = 1
			self.mimetype='image/jpg'
		# Control de escala (resolucion)
		elif path=="/scale/up":
			self.projection.scale = up(self.projection.scale)
		elif path=="/scale/down":
			self.projection.scale = down(self.projection.scale)
		# Control de perspectiva
		elif path=="/persp/up":
			self.projection.persp = up(self.projection.persp, 2)
		elif path=="/persp/down":
			self.projection.persp = down(self.projection.persp, 2)
		# Control de sombras
		elif path=="/black/up":
			self.projection.levelBlack = up(self.projection.levelBlack, 2)
		elif path=="/black/down":
			self.projection.levelBlack = down(self.projection.levelBlack, 2)
		# Control gamma
		elif path=="/gamma/up":
			self.projection.levelGamma = up(self.projection.levelGamma, 2)
		elif path=="/gamma/down":
			self.projection.levelGamma = down(self.projection.levelGamma, 2)
		# Control de luces
		elif path=="/white/up":
			self.projection.levelWhite = up(self.projection.levelWhite, 2)
		elif path=="/white/down":
			self.projection.levelWhite = down(self.projection.levelWhite, 2)
		# Control de efectos
		elif path=="/fx/off":
			self.projection.applyFX = False
		elif path=="/fx/on":
			self.projection.applyFX = True
		# Archivos corrientes
		elif path.endswith(".html"):
			mode = 0
			self.mimetype='text/html'
		elif path.endswith(".jpg"):
			mode = 0
			self.mimetype='image/jpg'
		elif path.endswith(".gif"):
			mode = 0
			self.mimetype='image/gif'
		elif path.endswith(".js"):
			mode = 0
			self.mimetype='application/javascript'
		elif path.endswith(".css"):
			mode = 0
			self.mimetype='text/css'

		# Mandar captura o archivo
		if mode==1:
			self.projection.capture()
			self.projection.compose()
			img = self.projection.getImage()
			self.response = img.make_blob('jpeg')
		elif mode==2:
			self.response = "Ok"
		else:
			f = open(curdir + sep + self.http_root + sep + path) 
			self.response = f.read()
			f.close()
