PROD_ARGS = --env-file .env.prod -f docker-compose.yaml 

prod:
	docker compose $(PROD_ARGS) up --build $(service) $(detached)

dev:
	docker compose $(PROD_ARGS) -f docker-compose.dev.yaml up --build $(service) $(detached)

down:
	docker compose down $(service)
