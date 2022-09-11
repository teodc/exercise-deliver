install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

freeze:
	python3 -m pip freeze > requirements.txt

format:
	python3 -m black src/*.py

lint:
	python3 -m pylint --disable=R,C src/*.py

test:
	python3 -m pytest -vv tests/test_*.py

build:
	docker compose up --build -d

destroy:
	docker compose stop
	docker compose down

rebuild: destroy build
