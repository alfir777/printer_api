# Тестовое задание

Тестовое задание [по ссылке](https://github.com/smenateam/assignments/tree/master/backend)

## Запуск
1. Клонировать репозиторий или форк
```
git clone https://github.com/alfir777/printer_api.git
```
2. Выполнить копирование файла .env_template на .env и выставить свои параметры
```
cd printer_api/
cp .env_template .env
```
3. Развернуть контейнеры с помощью в docker-compose
```
docker-compose -f docker-compose.yml up -d
```
4. Создать виртуальную среду venv
```
python3 -m venv env
source env/bin/activate
```
5. Установка зависимостей
```
pip install -r requirements.txt
```
6. Выполнить миграции/сбор статики
```
cd config/
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
```
6. Создать суперпользователя
```
python3 manage.py createsuperuser
```
7. Загрузить ранее созданные фикстуры
```
python3 manage.py loaddata core/fixtures/subjects.json
```
8. Запустить worker
```
python3 manage.py rqworker
```
9. Запустить сам проект
```
python3 manage.py runserver
```

#### Дополнительная команда
Выгрузить фикстуры
```
python3 manage.py dumpdata core --indent=4 --output=core/fixtures/subjects.json
```