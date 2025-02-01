init: start_docker
	docker compose exec python sh -c "pip install -r requirements.txt"
	make migrate

start_server: start_docker
	docker compose exec python sh -c "gunicorn -b 0.0.0.0:8000 -w 3 --forwarded-allow-ips='*' --reload django_rest_api.wsgi"

collect_static_files: start_docker
	docker compose exec python sh -c "python manage.py collectstatic"

test: start_docker static_type_check
	docker compose exec python sh -c "python -Wa manage.py test"

restart_docker: start_docker start_server

make_migrations: start_docker
	docker compose exec python sh -c "python manage.py makemigrations"

migrate: start_docker
	docker compose exec python sh -c "python manage.py migrate"

start_docker:
	docker compose up -d

stop_docker:
	docker compose stop

static_type_check:
	docker compose exec python sh -c "python -m mypy api"
