# Dota_WebSite
___
Dota WebSite is an educational project that was written on Python web framework - Django. My goal here was to learn Django basics and other useful tools such as Django REST Framework, Docker, principles of CI/CD, etc.
___
## **Compatibility**
Tested on Python 3.11

All configurations are added in `requirements.txt`
## **Stack**
- Python
- Django
- Django REST Framework
- Docker
- Celery
- Aiogram
## **Useful commands**
- Fill sqlite database with test data
```shell
python manage.py test_fill_db
```
- Add superuser
```shell
python manage.py auto_superuser
```
## **Quickstart**
There are several ways to start Dota WebSite
- Base django command
```shell
python manage.py runserver
```
Site will be available at http://127.0.0.1:8000
- Start Docker container with docker-compose
```shell
docker-compose up --build
```
Site will be available at http://localhost
## **Additions for Ubuntu**
If you want to use queue tasks you have to:
- Start RabbitMQ server 
```shell
sudo apt-get install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```
- Start celery worker
```shell
celery -A my_dota worker
```
- Run django
```shell
python manage.py runserver
```
