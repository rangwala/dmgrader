echo "hello world"
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:80

