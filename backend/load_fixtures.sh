#!/bin/bash
python manage.py loaddata animal/fixtures/species.json
python manage.py loaddata animal/fixtures/breeds.json
python manage.py loaddata animal/fixtures/genders.json
python manage.py loaddata animal/fixtures/statuses.json
python manage.py loaddata animal/fixtures/identification_types.json
python manage.py loaddata user/fixtures/roles.json