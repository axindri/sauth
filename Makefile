.PHONY: run run-logs stop destroy rebuild rebuild-logs update

run:
	docker compose up -d

run-logs:
	docker compose up

stop:
	docker compose down

destroy:
	rm -rf db_data/
	docker compose down -v

rebuild:
	docker compose up -d --build

rebuild-logs:
	docker compose up --build

update:
	git pull
	docker compose up -d --build
