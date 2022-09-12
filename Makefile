build:
	docker compose up --build -d

start:
	docker compose up -d

stop:
	docker compose stop

restart: stop start

destroy:
	docker compose stop
	docker compose down

rebuild: destroy build
