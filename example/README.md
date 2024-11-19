# solo-django-admin
## Django admin for non Django ORM

### Run
rename .env_example to .env
```
docker-compose up -d
docker exec -it app-example python -m solo_django_admin.manage createsuperuser
```
