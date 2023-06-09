test:
  poetry run pytest -v

build:
  poetry build

publish:
  poetry publish

shell:
  poetry shell

yaml:
  poetry run python kultimate/utils/process_yaml.py

run:
  kultimate

install:
  poetry install

dev:
  textual run --dev ./kultimate/app.py

pru:
  python prueba.py

