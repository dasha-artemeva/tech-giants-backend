MANAGE = poetry run python src/manage.py
FIXTURES_PATH = src/fixtures
load_data:
	$(MANAGE) loaddata $(FIXTURES_PATH)/members/groups.json $(FIXTURES_PATH)/members/admin.json


