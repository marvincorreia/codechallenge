FROM python:3.8 AS builder
RUN apt-get update
RUN apt-get install -y pipenv
RUN groupadd --gid 5000 newuser \
&& useradd --home-dir /home/newuser --create-home --uid 5000 \
--gid 5000 --shell /bin/sh --skel /dev/null newuser
WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install --system --deploy
# openjdk-11-jdk-headless \
# nodejs \
# npm \
# npm install -g typescript
ENV PORT=8000
EXPOSE ${PORT}

# FROM builder AS app
WORKDIR /app
COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
# VOLUME /app/submissions
# USER newuser
CMD daphne codechallenge.asgi:application --port $PORT --bind 0.0.0.0 -v2
