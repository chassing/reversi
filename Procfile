web: python manage.py runserver_socketio 0.0.0.0:$PORT
#web: python manage.py run_gunicorn -c gunicorn -b 0.0.0.0:$PORT -w 9 -k gevent --max-requests 250
migrate: python manage.py migrate main
collectstatic: python manage.py collectstatic --noinput --ignore="*.less" --clear

# heroku labs:enable user-env-compile
# heroku config:set DJANGO_SETTINGS_MODULE=reversi.settings.production
# heroku config:set SECRET_KEY=unser_geheimer_schluessel_bestehend_aus_vielen_zeichen
# heroku config:add AWS_ACCESS_KEY_ID=XXX AWS_SECRET_ACCESS_KEY=XXX
# heroku config:set DISABLE_COLLECTSTATIC=1
