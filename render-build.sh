echo "🚀 Running Django collectstatic, makemigrations, and migrate..."

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate