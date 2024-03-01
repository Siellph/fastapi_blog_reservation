# fastapi_blog_reservation
Онлайн платформа для бронирования ресторанов с использованием Fast Api

Модели: Пользователи, Рестораны, Бронирования

Идея проекта: Разработка онлайн платформы для бронирования столиков в ресторанах с возможностью просмотра меню, выбора даты и времени и оформления бронирования.

Требования к проекту:
- Упаковка проекта в докер-компоуз и запуск через docker compose up без дополнительной настройки
- прохождение flake8 + mypy в соответствии с конфигурациями проекта
- Кеширование всего, что возможно закешировать через redis
- Orm:  sqlalchemy2.0
- Migration: alembic (необязательно т.к. не делали на парах)
- Тесты - pytest + mock на redis и rollback транзакций фикстур вместо удаления.
- Минимальные данные при разворачивании проекта (фикстуры)
- Метрики: 
  - На кол-во полученных запросов в разрезе каждой ручки.
  - На кол-во ошибок по каждой ручке
  - На кол-во отправленных запросов
  - Время выполнения каждой ручки в среднем (гистограмма)
  - Время выполнения всех интеграционных методов (запросы в бд, редис и тп (гистограмма))
- Валидация входящих данных (pydantic)
- Настройки в env
- Без дублирования кода
- poetry как сборщик пакетов
- Обработка ошибок и соответствующие статусы ответов
- В README.md ожидается увидеть как что работает, чтобы можно было ознакомиться проще с проектом
___
**Логика работы**

* Пользователи могут зарегистрироваться на платформе, предоставив свои данные, такие как имя, телефон и пароль.
* После успешной регистрации пользователи могут аутентифицироваться, используя свои учетные данные. Также доступен функционал обновления данных для пользователя.
* Пользователи могут просматривать список ресторанов, доступных для бронирования.
* По каждому ресторану можно посмотреть подробную информацию, включая адрес, описание и меню.
* Пользователи могут просматривать меню с блюдами, ценами и категориями.
* Пользователи могут выбрать ресторан, дату и время для бронирования столика.
* Пользователи могут просматривать свои текущие и предыдущие бронирования.
* Администраторы и сотрудники могут управлять ресторанами, меню, а также просматривать и управлять бронированиями.
* Администраторы могут добавлять новые рестораны и обновлять информацию о существующих.
___
**Стэк технологий**
___
+ :rocket: Framework: FAST API 0.103.1
+ ORM: SQLAlchemy2.0 2.0.23
+ Pydantic 2.3.0
+ :scroll: Poetry 1.3.2
+ :ship: Docker
+ :snake: Python 3.11
___
Перед запуском проекта необходимо создать:
1. Файл `.env` в папке `/grafana`. Пример находится в файле '/grafana/env.example'
2. Файл `.env` в папке `/conf`. Пример находится в файле '/conf/env.example'
___
Для запуска проекта на локальном ПК используется следующая команда
```
sudo docker-compose up
```
___
При запуске проекта разворачиваются контейнеры и соответствующие им образы со следующими именами:

|Имя контейнера        |Описание|
|----------------------|--------|
|prometheus            |Система мониторинга предназначенная для сбора и анализа метрических данных о работе приложений и инфраструктуры|
|grafana               |Открытое ПО для визуализации данных и мониторинга. Предоставляет гибкие инструменты для создания интерактивных и информативных дашбордов|
|web                   |Контейнер с основным проектом|
|web_db                |Контейнер с БД|
|redis                 |Высокопроизводительная система управления базами данных, использующая в памяти хранение данных и работающая по принципу ключ-значение|
___
*Для просмотра контейнеров:*
```
sudo docker container ls
```

*Для просмотра образов:*
```
sudo docker image ls
```
*Для того чтобы просмотреть имеющиеся volume:*
```
sudo docker volume ls
```
*Для того чтобы очистить БД необходимо удалить volume:*
```
sudo docker volume rm [volume_name]
```
___
Для быстрого удаления всех контейнеров, образов и данных из Docker можно воспользоваться следующим набором комманд
```
sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -f "dangling=true" -q)
sudo docker rmi $(sudo docker images -a -q)
sudo docker volume prune
sudo docker volume rm fastapi_blog_prom_data
sudo docker system prune -a
```
___
**После запуска проекта доступны:**

|Название     |URL  |
|-------------|-----|
|Документация | http://0.0.0.0:8000/swagger|
|Метрика      | http://0.0.0.0:8000/metrics|
|Prometheus   | http://0.0.0.0:9090|
|Grafana      | http://0.0.0.0:3000/login|

___
🏎️ **Roadmap**

- [X] Модели SQLAlchemy
- [X] Фикстуры
- [X] Миграции
- [X] Схемы Pydantic
- [X] CRUD
- [X] Эндпоинты
- [X] Обработка исключений
- [ ] Метрики
- [ ] Кэширование данных
- [ ] Тесты
