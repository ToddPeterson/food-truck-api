# food-truck-api
Food truck api source code.

### Dev commands

Build:
```
docker-compose build
```

Run a command inside the docker container:
```
docker-compose run app sh -c "<your command>"
```

Run tests and linting:
```
docker-compose run app sh -c "python manage.py test && flake8"
```

Run app on localhost:8000:
```
docker-compose up
```

Stop app:
```
docker-compose down
```
