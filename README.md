# Electric Meter
## Описание
Сервис позволяет опрашивать пассивные электросчетчики в локальной сети, получая от них данные в формате JSON: {"id":"<id>", "A":"50","kW":"44325"}, где
- id – счетчика;
- A – текущий ток (кол-во Ампер) потребления сети;
- kW – суммарное потребление энергии (Киловатт) за все время работы.

Все счетчики находятся в одной сети (диапазон адресов 127.0.0.1:9000 - 127.0.0.1:65000). Для отладки и эмуляции счетчиков используется эндпойнт из репозитория [electric_endpoint](https://github.com/DOSuzer/electric_endpoint). Данный эндпойнт вместо разных портов использует порт 8001 и принимает порт счетчика в качестве аргумента пути: 127.0.0.1/**9000**/.

В проекте доступны следующие эндпойнты:
+ /meters/
  * POST запрос - добавление счетчика;
    ```
    {
        "meter_id": "345631237",
        "address": "127.0.0.1",
        "port": 4321
    }
    ```
+ /meters/<meter_id>/
  * DELETE запрос - удаление счетчика;
+ /meters/<meter_id>/data/
  * GET запрос - получение данных с счетчика
+ /meters/<meter_id>/data/
  * GET запрос - получение статистики по счетчику за период
    ```
    {
        "start_date": "12-08-2023",
        "end_date": "14-08-2023"
    }
    ```
    
Если в settings.py стоит DEBUG=True, то предусмотрена работа с тестовыми данными и тестовыми счетчиками из [electric_endpoint](https://github.com/DOSuzer/electric_endpoint).

## Запуск проекта
1. клонировать репозиторий
   ```
   git clone git@github.com:DOSuzer/electric_meter.git
   ```
2. Cоздать и активировать виртуальное окружение:
   ```
   cd electric_meter
   py -3.10 -m venv env
   ```
   ```
   . venv/Scripts/activate - Windows
   . venv/bin/activate     - Linux
   ```
3. Установить зависимости из файла requirements.txt:
   ```
   python -m pip install --upgrade pip
   ```
   ```
   pip install -r requirements.txt
   ```
4. Выполнить миграции:
   ```
   python manage.py migrate
   ```
5. При необходимости можно заполнить БД тестовыми данными (счетчиками и данными по счетчику):
   ```
   python manage.py create_meters
   python manage.py create_data   
   ```
6. Запуск сервера
   ```
   python manage.py runserver 
   ```
7. Запуск Redis в Docker контейнере
   ```
   docker run -d -p 6379:6379 redis
   ```
9. Запустить при необходимости [electric_endpoint](https://github.com/DOSuzer/electric_endpoint).
10. Запуск Celery
    ```
    celery -A electric_meter worker --loglevel=INFO -P gevent   - Windows
    celery -A electric_meter worker --loglevel=INFO             - Linux
    celery -A electric_meter beat --loglevel=INFO
    ```
