FROM python:3.8 as base
RUN apt-get update
RUN apt-get install -y pipenv
RUN apt-get install -y openjdk-11-jdk-headless
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN npm install -g typescript

FROM base as app
COPY . /app
WORKDIR /app
ENV PORT=8000
EXPOSE 8000/tcp
RUN pipenv install --system --deploy
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
CMD daphne codechallenge.asgi:application --port $PORT --bind 0.0.0.0 -v2
