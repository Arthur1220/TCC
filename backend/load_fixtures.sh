#!/bin/bash
python manage.py loaddata blockchain/fixtures/status.json
python manage.py loaddata event/fixtures/event_types.json
python manage.py loaddata animal/fixtures/species.json
python manage.py loaddata animal/fixtures/breeds.json
python manage.py loaddata animal/fixtures/genders.json
python manage.py loaddata animal/fixtures/status.json
python manage.py loaddata animal/fixtures/identification_types.json
python manage.py loaddata user/fixtures/role.json