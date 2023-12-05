start_docker_local:
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d
	docker-compose -f docker-compose.yml -f docker-compose.local.yml exec db sh -c "psql -U postgres -c 'create database ${POSTGRES_DB};'" || true
	docker-compose -f docker-compose.yml -f docker-compose.local.yml exec db sh -c "psql -U postgres -c 'GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};'" || true

stop_docker_local:
	docker-compose -f docker-compose.yml -f docker-compose.local.yml down

create_migration:
	alembic -c service/alembic.ini revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrate:
	alembic -c service/alembic.ini upgrade head
