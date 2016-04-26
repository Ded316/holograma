# holocam
Servidor en Python para un sistema de proyección holográfica en tiempo real para la Feria de la Ciencia Escolar de Écija - ASTIGICIENCIA 2016 (<http://www.astigiciencia.com/>).

Copyright (c) 2016 Antonio Negro


## Requisitos

* Ubuntu 14.04
* libmagickwand-dev
* libmagickcore5-extra
* Python: 2.7.6
* Wand: 0.4.2
* OpenCV: 2.4.8

## Instalación

	sudo apt-get install python-wand
	sudo apt-get install libmagickwand-dev
	sudo apt-get install libmagickcore5-extra
	sudo apt-get install python-opencv

## Configuración

Edita `holomaster.py` para seleccionar la fuente de cada plano:

~~~.py
    # Crear instancias para capturar frames de distintas fuentes
    localImg = LocalImage(HTTP_ROOT + sep + "man.jpg")
    remoteCam = HTTPImage("http://localhost:8001/output.jpg")
    localCam = CameraImage(0)
    
    # Seleccionar la fuente para cada plano
    front = localCam
    #left  = remoteCam
    #bottom = localCam
    #right  = localCam
~~~

Edita `holomaster.py` para ajustar la composición de los planos de proyección:

~~~.py
    # Configurar los planos a usar para construir la proyeccion
    projection = Projector([front])
    #projection = Projector([front, left])
    #projection = Projector([front, left, right])
    #projection = Projector([front, left, right, bottom])
~~~

## Puesta en marcha

1. (Opcional) Ejecuta `holocam.py` en los equipos que harán de webcam para captura remota de imágenes.
2. Ejecuta `holomaster.py` en el equipo principal que capturará las imágenes provenientes de diversos medios: webcam local del propio equipo, webcam remota de otro equipo o archivo de imagen.

## Visualizar y controlar el holograma

Utiliza el navegador web para visualizar y controlar la proyección holográfica. Para ello, conéctate al puerto 8080 del equipo principal:

* Utiliza la URL <http://servidor:8080/index.html> para visualizar la proyección.
* Utiliza la URL <http://servidor:8080/control.html> para controlar los parámetros del holograma.

