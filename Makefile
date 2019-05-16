dev: dev-build dev-run

dev-build:
	docker-compose -f ./docker-compose.yml build

dev-run:
	docker-compose -f ./docker-compose.yml up

dev-down:
	docker-compose -f ./docker-compose.yml down