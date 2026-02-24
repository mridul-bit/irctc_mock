RUN :
- clone the repo 
- run : docker compose up 
- open localhost:8000
- register as admin to add/book/search train , see top 5 routes and get last 20 logs for GET /api/trains/search/?source=&destination= 
- register as user to book/search train

Refernces:
- https://www.mongodb.com/docs/languages/python/django-mongodb/current/connect/
- https://pypi.org/project/django-cors-headers/
- https://pypi.org/project/mysqlclient/
- https://hub.docker.com/_/mongo#mongo_initdb_database
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#requirements
- https://docs.djangoproject.com/en/6.0/ref/databases/#mysql-notes
- https://www.django-rest-framework.org/api-guide/permissions/
- https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#requirements