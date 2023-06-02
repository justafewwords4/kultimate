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
