# IT Assets

Учебный проект на Django для учёта IT-активов.

Здесь можно:
- добавлять и редактировать активы;
- привязывать их к сотрудникам;
- смотреть статус и местоположение;
- создавать заявки на ремонт;
- делать инвентаризацию;
- импортировать и экспортировать данные;
- печатать отчёты и QR-коды.

## Что используется

- Python 3.12+
- Django
- Django REST Framework
- PostgreSQL
- openpyxl
- qrcode
- reportlab

## Как запустить

### 1. Клонировать репозиторий

```powershell
git clone https://github.com/Terra909/it-assets.git
cd it-assets
```

### 2. Создать виртуальное окружение

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Установить зависимости

```powershell
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary qrcode openpyxl reportlab
```

### 4. Создать файл `.env`

Скопируйте `.env.example` в `.env` и заполните свои данные.

### 5. Сделать миграции

```powershell
python manage.py migrate
```

### 6. Создать суперпользователя

```powershell
python manage.py createsuperuser
```

### 7. Запустить проект

```powershell
python manage.py runserver
```

После этого сайт откроется по адресу:

```text
http://127.0.0.1:8000/
```

## Полезные команды

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## REST API

В проекте есть API для работы с активами.

### Авторизация

- `POST /api/token/` — получить токены
- `POST /api/token/refresh/` — обновить токен

Для запросов к API нужен заголовок:

```text
Authorization: Bearer <access_token>
```

### Основные адреса API

- `/api/assets/` — активы
- `/api/asset-types/` — типы активов
- `/api/statuses/` — статусы
- `/api/locations/` — локации

Для активов есть фильтры:

- `q` — поиск
- `type` — тип
- `status` — статус
- `employee` — сотрудник

## Про .env

Файл `.env` не надо загружать на GitHub. Для этого есть `.env.example`.
