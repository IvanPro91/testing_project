# Тестовое задание для соискателя на вакансию инженер-программист лаборатории разработки ПО



## Описание тестового задания

Реализовать api-сервис регистрации и авторизации пользователя.
Сервис должен быть реализован с использованием микрофреймворка Flask для хранения информации используется  СУБД Postgres.
В приложении должно быть предусмотрено 2 конфигурации для разработки (development) и для продуктовой версии (production), какую СУБД использовать для development на усмотрение Исполнителя.
Реализовать не менее 2-х функций отображения (endpoint):

1) Для регистрации где вносится ФИО, логин пользователя и задается пароль. После успешной регистрации в ответной части возвращается сообщение об успехе или ошибке связанной с дублированием логина. Логин д.б. уникальным.
2) Для авторизации где задается логин и пароль. В ответной части возвращается JWT в котором должна быть закодированная информация содержащая логин пользователя.

Все запросы и ответные сообщения передаются в формате json.
Данные функции д.б. документированы по стандарту Open API.
Проект разместить в репозитории gitlab.com по готовности направить ссылку на него.
Проект должен быть достаточно документирован для его развертывания и запуска.

# Начало установки

## Установка и запуск

Для того что бы начать установку данного тестового задания, требуется установить:

1. [Python версии 3.11](https://www.python.org/downloads/release/python-3110/)

Зависимости:
```
pip install Flask==2.3.2
pip install Flask-Migrate==4.0.4
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-RESTful==0.3.10
pip install PyJWT==1.4.2
pip install psycopg2==2.9.6
```

## Базы данных
В данном примере используется локальная БД Postgresql, которая не устанавливается в Docker
и SQLite3.

## Настройка базы данных Postgresql

В файле конфигурации pg_hba.conf в директории C:\Program Files\PostgreSQL\14\data
необходимо прописать правила доступа:
```
# IPv4 local connections:
host    all             all             0.0.0.0/0            scram-sha-256
```
Или свои

В файле postgresql.conf этой же директории, проверить строку 
```
# - Connection Settings -
listen_addresses = '*'		# what IP address(es) to listen on;
```

***

# Настройка Docker файла
```
FROM python:3.9
WORKDIR /testing_project
ADD . /testing_project
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENV MODE=dev
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "./run.py"]
```

Для запуска веб-приложения в 2-х доступных конфигурациях необходимо:

1. Для продуктивной части в элементах окружения используется MODE = dev
и используется БД SQLite3

2. Для продуктивной части в элементах окружения используется MODE = prod 
и используется БД [PostgreSQL 14](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)


# Запуск веб-приложения в Docker

1. [Установка Docker](https://www.docker.com/) и регистрация
2. Необходимо запустить комманду:
```
docker build . -t [тут имя после регистрации]/[название проекта]
```

По окончанию установки будет похожее сообщение:
```
View build details: docker-desktop://dashboard/build/default/default/p0yqelzhkXXXXXXXXXXXXXX
```
3. После того как образ соберется, можно приступить к запуску, запуск веб-приложения осуществляется командой:
```
docker run -p=5000:5555 [имя пользователя]/[название проекта]
```
где -p [порт исходящий]:[порт входящий] [имя пользователя Docker]/[название проекта]

после запуска веб-приложения можно обратиться по url:

127.0.0.1:5000 на локальной машине и получить ответ от Docker порта 5555 (по правилу запуска выше)

# Работа с API тестового проекта

В тестовом проекте доступны 2-ва endpoint:
1. Регистрация пользователя
2. Авторизация пользователя

Описание запроса регистрации пользователя, данный запрос можно осуществить с помощью 
[REST & SOAP API Testing Tool](reqbin.com)

```
http://127.0.0.1:5000/api/v1/user_registration
{"login": "LOGIN", "password": "12345678", "username": "Фамилия Имя Отчество"}
```

Для предусмотрения возможности импользования других версия api в url используется v1 и может меняться по мере изменния кода

для запроса 'user_registration' используется:

| Параметр | Тип данных | Описание                                                            |
|----------|------------|---------------------------------------------------------------------|
| login | String     | (обязательный), передается уникальный логин пользователя приложения |
| password | String          | (обязательный), передается строковое значение пароля пользователя   |
| username     | String        | (обязательный), передается ФИО пользователя приложения              |

Регистрация прошла успешно:
```
{
    "msg": "Registration successful",
    "status": true
}
```

для запроса 'user_login' используется:

```
http://127.0.0.1:5000/api/v1/user_login
{"login": "LOGIN", "password": "12345678"}
```

| Параметр | Тип данных | Описание                               |
|----------|------------|----------------------------------------|
| login | String     | Передаем уникальный login пользователя |
| password | String          | Передаем пароль пользоветеля           |

При успешной авторизации возвращается токен пользователя:

```
{
    "token": "eyJ0eXAiOiJKV1QiLCiJ9.eyJsb2dpbiI6Iml2YW4if..."
}
```

# Ошибки регистрации пользователя

Логин пользователя уже существует
```
{
    "error": "Login already exists!",
    "status": false
}
```
Решение: Необходимо проверить введенные данные.

# Ошибки авторизации пользователя

Пользователь не найден или пароль не верен
```
{
    "error": "User not found or password not valid!",
    "status": false
}
```
Решение: Необходимо проверить введенные авторизационные данные.