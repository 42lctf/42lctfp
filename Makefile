
APP_NAME	= ftlctfp

COMPOSE_BASE		= -f ./docker-compose.yml
COMPOSE_DEV		= -f ./docker-compose.yml -f ./docker-compose.dev.yml
COMPOSE_PROD	= -f ./docker-compose.yml -f ./docker-compose.override.yml

#Dev
DOCKER		= docker compose ${COMPOSE_DEV} -p ${APP_NAME}_dev

# To differentiate prod mode
ifeq ($(shell hostname), ctf.42lausanne.ch)
	ifeq ($(shell pwd), /home/deployer)
		#Prod
		DOCKER		= docker compose ${COMPOSE_PROD} ${ENV_FILE} -p ${APP_NAME}
	endif
endif


all:		start

build:
			${DOCKER} build

start:
			${DOCKER} up -d --build

ps:
			${DOCKER} ps -a

logs:
			${DOCKER} logs
flogs:
			${DOCKER} logs --tail 40 -ft

logsfront:
			${DOCKER} logs frontend
logsback:
			${DOCKER} logs backend
logspostg:
			${DOCKER} logs postgres
logsnginx:
			${DOCKER} logs nginx

flogsfront:
			${DOCKER} logs --tail 40 -ft front
flogsback:
			${DOCKER} logs --tail 40 -ft backend
flogspostg:
			${DOCKER} logs --tail 40 -ft postgres
flogsnginx:
			${DOCKER} logs --tail 40 -ft nginx

refront:
			${DOCKER} restart frontend
reback:
			${DOCKER} restart backend
repostg:
			${DOCKER} restart postgres

# info:
# 			${DOCKER} exec 
migrate:
			${DOCKER} exec backend bash alembic -c alembic.ini upgrade head
# repair:
# 			${DOCKER} exec 
# revert:
# 			${DOCKER} exec 

runfront:
			${DOCKER} exec frontend bash
runback:
			${DOCKER} exec backend bash
runpostg:
			${DOCKER} exec postgres bash

down:
			${DOCKER} down

clean:		down
					${DOCKER} down --volumes

re:			
					${MAKE} clean 
					${MAKE} all
					sleep 4
					${MAKE} migrate


.PHONY:		all build start ps logs flogs run down clean re
