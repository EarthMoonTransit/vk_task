### FastApi and Docker 
Склонируйте репозиторий:

```
https://github.com/EarthMoonTransit/vk_task.git
```
Заполните ```.env``` файл:
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
```
Создайте Docker образ
```
docker compose up --build
```