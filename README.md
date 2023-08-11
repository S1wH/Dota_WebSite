# Dota_WebSite
___
Dota WebSite is an educational project that was written on Python web framework - Django. My goal here was to learn Django basics and other useful tools such as Django REST Framework, Docker, principles of CI/CD, etc.
___
## **Compatibility**
Tested on Python 3.11
All configurations are added in `requirements.txt`
## **Useful commands**
- Fill sqlite database with test data
```shell
python manage.py test_fill_db
```
- Add superuser
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```shell
python manage.py auto_superuser
```
