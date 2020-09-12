options ?=

venv:
	@python3 -m venv venv

setup:
	@pip3 install -r requirements.txt

test:
	@venv/bin/pytest --tb=native -v -s

lint:
	@pylint *.py
