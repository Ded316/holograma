#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from hologram import *
from masterhandler import *


# Clase para manejar las peticiones que se reciban del navegador
class httpHandler(BaseHTTPRequestHandler):
	# Tratamiento las peticiones GET
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			# Procesar peticion
			holoHandler.handle(self.path)
			
			# Enviar el recurso solicitado
			self.send_response(200)
			self.send_header('Content-type', holoHandler.mimetype)
			self.end_headers()
			self.wfile.write(holoHandler.response)

		except IOError:
			self.send_error(404,'Archivo no encontrado: %s' % self.path)


# Iniciar servidor
try:
	# Ajustes iniciales
	PORT_NUMBER = 8080
	HTTP_ROOT = "http_root"
	SCALE = -3
	PERSP = 0
	APPLY_FX = False	

	# Crear instancias para capturar frames de distintas fuentes
	localImg = LocalImage(HTTP_ROOT + sep + "man2.jpg")
	remoteCam = HTTPImage("http://localhost:8001/output.jpg")
	localCam = CameraImage(0)
	
	# Seleccionar la fuente para cada plano
	front = localCam
	#front = localImg
	#left  = remoteCam
	#bottom = localCam
	#right  = localCam
	
	# Configurar los planos a usar para construir la proyeccion
	projection = Projector([front])
	#projection = Projector([front, left])
	#projection = Projector([front, left, right])
	#projection = Projector([front, left, right, bottom])

	projection.scale = SCALE
	projection.persp = PERSP
	projection.applyFX = APPLY_FX
	
	# Ejecuta las ordenes que recibe por HTTP y actualiza la proyeccion
	holoHandler = HoloHandler(HTTP_ROOT, projection)
	
	# Crear un servidor web y definir el manejador que procesara las peticiones entrantes
	server = HTTPServer(('', PORT_NUMBER), httpHandler)
	print 'Servidor HTTP iniciado en el puerto ', PORT_NUMBER
	
	# Esperar indefinidamente peticiones entrantes
	server.serve_forever()

except KeyboardInterrupt:
	print '^C recibido, apagando el servidor web'
	server.socket.close()
