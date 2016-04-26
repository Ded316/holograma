#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cv2 import *
from PIL import Image as ImagePIL
import StringIO
from wand.image import Image

from hologram import CameraImage



# Clase para manejar las peticiones que se reciban del navegador
class myHandler(BaseHTTPRequestHandler):
	# Tratamiento las peticiones GET
	def do_GET(self):
		try:
			# Captura de webcam
			if self.path.startswith("/output.jpg"):
				mode = 1
				mimetype='image/jpg'
			else:
				mode = 2
				mimetype='text/plain'

			# Enviar el recurso solicitado
			self.send_response(200)
			self.send_header('Content-type', mimetype)
			self.end_headers()

			# Mandar captura o archivo
			if mode == 1:
				myCam.capture()
				img = myCam.getImage()
				blob = img.make_blob('jpeg')
				self.wfile.write(blob)
				myCam.reset()
			else:
				self.wfile.write("Ok")

		except IOError:
			self.send_error(404,'File not found: %s' % self.path)



# Iniciar servidor
try:
	# Ajustes iniciales
	PORT_NUMBER = 8001
	SCALE = -3

	# Crear una instancia para manejar la webcam
	myCam = CameraImage(0)
	myCam.scale = SCALE
	
	# Crear un servidor web y definir el manejador que procesara las peticiones entrantes
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Cámara HTTP iniciada en el puerto ', PORT_NUMBER
	
	# Esperar indefinidamente peticiones entrantes
	server.serve_forever()

except KeyboardInterrupt:
	print '^C recibido, apagando el servidor web'
	server.socket.close()
