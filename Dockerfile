FROM python:3.8 AS builder
RUN apt-get update
RUN apt-get install -y pipenv \
openjdk-11-jdk-headless \
nodejs \
npm && npm install -g typescript
WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install --system --deploy
ENV PORT=8000
ENV NO_ROOT_USER="newuser"
EXPOSE ${PORT}
RUN groupadd --gid 5000 ${NO_ROOT_USER} \
&& useradd --home-dir /home/${NO_ROOT_USER} --create-home --uid 5000 \
--gid 5000 --shell /bin/sh --skel /dev/null ${NO_ROOT_USER}
COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
RUN chmod -R 100 /app/*
# RUN chmod -R 755 /app
# VOLUME /app/submissions
CMD daphne codechallenge.asgi:application --port $PORT --bind 0.0.0.0 -v2
