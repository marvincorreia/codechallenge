from os import system

commands = [
    "python manage.py makemigrations --noinput",
    "python manage.py migrate --noinput",
    "python manage.py collectstatic --noinput",
]

for command in commands:
    try:
        system(command)
    except Exception as e:
        pass
