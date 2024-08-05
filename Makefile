APP_NAME="iec-api"

################################
# COMMANDS TO RUN LOCALLY
################################

local/install:
	poetry install

local/tests:
	poetry run pytest --cov-report=html --cov-report=term --cov . 

local/lint:
	poetry run ruff check .
	poetry run ruff . --fix --exit-non-zero-on-fix

local/lint/fix:
	poetry run black .

local/run:
	poetry run python src/main.py


############################################
# COMMANDS TO RUN USING DOCKER (RECOMMENDED)
############################################

docker/install:
	docker compose build ${APP_NAME}

docker/up:
	docker compose up -d

docker/down:
	docker compose down --remove-orphans

docker/test:
	docker compose run ${APP_NAME} poetry run pytest --cov-report=html --cov-report=term --cov .

docker/lint:
	docker compose run ${APP_NAME} poetry run ruff check .

docker/lint/fix:
	docker compose run ${APP_NAME} poetry run ruff . --fix --exit-non-zero-on-fix

docker/run:
	docker compose run ${APP_NAME} poetry run python src/main.py

##################
# HEPFUL COMMANDS
##################
