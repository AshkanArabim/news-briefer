PROD_ARGS = --env-file .env.prod -f docker-compose.yaml 

prod:
	docker compose $(PROD_ARGS) up --build $(service)

dev:
	docker compose $(PROD_ARGS) -f docker-compose.dev.yaml up --build $(service)

down:
	docker compose down $(service)
