# Spy Cat Backend

Бекенд для додатку Spy Cat Management на Django + Django REST Framework.

## Вимоги

- Python 3.9+
- virtualenv 

 Встановлення

1. Клонувати репозиторій бекенду:
   ```bash
   git clone <URL-репозиторію-бекенду>
   cd <папка-бекенду>
python -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows

python manage.py migrate

python manage.py runserver 8000
