# Makefile

# Levanta todos los servicios en modo detached (en segundo plano)
up:
	docker-compose up -d --build

# Detiene y elimina los contenedores, redes y volúmenes
down:
	docker-compose down

# Muestra los logs de los servicios
logs:
	docker-compose logs -f

# Reinicia los servicios
restart:
	docker-compose restart

# Accede a la shell del contenedor del backend
shell-backend:
	docker-compose exec backend /bin/sh

