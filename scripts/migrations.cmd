cd ../
call env/Scripts/activate
python manage.py makemigrations
python manage.py migrate
cmd