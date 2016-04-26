#!/usr/bin/python
# -*- coding: utf-8 -*-

from cv2 import *
from PIL import Image as ImagePIL
import StringIO
from wand.image import Image
from wand.color import Color
import urllib



# Clase para capturar directamente de la webcam
class CameraImage:
	# Constructor
	def __init__(self, cam):
		self.vcCam = VideoCapture(cam)
		self.img = Image(width = 320, height = 320, background = Color('red'))
		self.captured = False
	
	# Capturar un fotograma
	def capture(self):
		if not self.captured:
			# Capturar de webcam
			success, imgND = self.vcCam.read()

			#if success:
				#imwrite("captura.png", imgND)

			# Corregir color BGR -> RGB
			imgND = cvtColor(imgND, COLOR_BGR2RGB)

			# Convertir imagen capturada: numpy.ndarray -> PIL.Image -> blob (BMP) -> wand.image.Image
			imgPIL = ImagePIL.fromarray(imgND)
			strBuff = StringIO.StringIO()
			imgPIL.save(strBuff, format="BMP")
			imgBlob = strBuff.getvalue()
			img = Image(blob=imgBlob)
			strBuff.close()

			self.img = img;
			self.captured = True

	# Devolver imagen
	def getImage(self):
		return self.img
	
	# Resetear flag de captura
	def reset(self):
		self.captured = False

# Clase para capturar remotamente a traves de HTTP
class HTTPImage:
	# Constructor
	def __init__(self, source):
		self.source = source
		self.img = Image(width = 320, height = 320, background = Color('blue'))
		self.captured = False
	
	# Capturar un fotograma
	def capture(self):
		if not self.captured:
			# Capturar de webcam
			file = urllib.urlopen(self.source)
			imgBlob = file.read()
			self.img = Image(blob=imgBlob)
			file.close()

			self.captured = True

	# Devolver imagen
	def getImage(self):
		return self.img
	
	# Resetear flag de captura
	def reset(self):
		self.captured = False


# Clase para capturar localmente desde una imagen de archivo
class LocalImage:
	# Constructor
	def __init__(self, source):
		self.source = source
		self.img = Image(width = 320, height = 320, background = Color('blue'))
		self.captured = False
	
	# Capturar un fotograma
	def capture(self):
		if not self.captured:
			# Capturar de webcam
			file = open(self.source)
			imgBlob = file.read()
			self.img = Image(blob=imgBlob)
			file.close()

			self.captured = True

	# Devolver imagen
	def getImage(self):
		return self.img
	
	# Resetear flag de captura
	def reset(self):
		self.captured = False
