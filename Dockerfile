FROM python:3.8 AS builder
RUN apt-get update && apt-get install -y pipenv \
openjdk-11-jdk-headless \
nodejs \
npm \
npm install -g typescript
ENV PORT=8000
EXPOSE 8000/tcp

FROM builder AS app
COPY . /app
WORKDIR /app
RUN pipenv install --system --deploy
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
CMD daphne codechallenge.asgi:application --port $PORT --bind 0.0.0.0 -v2
