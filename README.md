# BilimHub — жеке билим берүү борбору үчүн веб-тиркеме

## Технологиялар
Python 3.11+, Django 5.2, PostgreSQL (локалдык демо үчүн SQLite), Django Templates, HTML, CSS, JavaScript.

## Баштапкы функциялар
- Курстардын ачык каталогу жана толук маалымат барагы.
- Курска онлайн арыз жөнөтүү.
- Кызматкерлер үчүн кирүү жана менеджер панели.
- Арыздарды издөө, статусун өзгөртүү жана эскертүү калтыруу.
- Django Admin аркылуу курстарды, студенттерди жана окуу топторун башкаруу.

## Linux / macOS орнотуу
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Windows PowerShell: `py -m venv .venv`, андан кийин `.venv\\Scripts\\activate`, `pip install -r requirements.txt`, `copy .env.example .env`, `py manage.py migrate`, `py manage.py createsuperuser`, `py manage.py runserver`.

Сайт: http://127.0.0.1:8000/  |  Админ: http://127.0.0.1:8000/admin/  |  Менеджер: http://127.0.0.1:8000/manager/

## PostgreSQL туташтыруу
PostgreSQL'де `education_center` маалымат базасын түзүп, `.env` файлына төмөнкүнү жазыңыз:
```env
DATABASE_URL=postgresql://dbuser:dbpassword@localhost:5432/education_center
```
Андан кийин `python manage.py migrate`.

## Эскертүү
Менеджер барактары `is_staff=True` болгон колдонуучуларга гана ачылат. Бул баштапкы иштелип жаткан версия. Кийинки этапта менеджердин өзүнчө интерфейси аркылуу студенттерди/топторду башкаруу, кабыл алынган арыздан студент түзүү, ролдорду бөлүү, билдирүүлөр, тесттер жана production коопсуздугу кошулат. Production'го чыгарууда `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, HTTPS жана резервдик көчүрмөлөрдү тууралоо зарыл.
# bilim_hub
