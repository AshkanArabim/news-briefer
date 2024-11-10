PROD_ARGS = --env-file .env.prod -f docker-compose.yml 

prod:
	docker compose $(PROD_ARGS) up --build $(service)

dev:
	docker compose $(PROD_ARGS) -f docker-compose.dev.yml up --build $(service)

down:
	docker compose down $(service)
