
<h3>Экспорт/импорт fixtures:</h3>

    python3 manage.py dumpdata core --indent=4 --output=core/fixtures/subjects.json

    python3 manage.py loaddata core/fixtures/subjects.json

<h3>Команды для RQ:</h3>

    python3 manage.py rqscheduler --interval 10

    python3 manage.py rqworker default
