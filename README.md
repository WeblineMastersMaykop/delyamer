# DELYAMER

#### Создание виртуального окружения
```bash
python -m venv venv
```

#### Активация виртуального окружения
Linux:
```bash
source venv/bin/activate
```
Windows:
```bash
venv\Scripts\activate
```

#### Установка зависимостей
```bash
pip install -r requirements.txt
```

#### Миграции в базу
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Создание суперпользователя
```bash
python manage.py createsuperuser
```

#### Сбор статики
```bash
python manage.py collectstatic
```

#### Запуск приложения
```bash
python manage.py runserver
```