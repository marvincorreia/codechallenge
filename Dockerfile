FROM python:3.8 AS builder
RUN apt-get update
RUN apt-get install -y pipenv \
openjdk-11-jdk-headless \
nodejs \
npm && npm install -g typescript
COPY Pipfile* /
RUN pipenv install --system --deploy
ENV PORT=8000
ENV GUEST_USER="guest"
EXPOSE ${PORT}
RUN groupadd --gid 5000 ${GUEST_USER} \
&& useradd --home-dir /home/${GUEST_USER} --create-home --uid 5000 \
--gid 5000 --shell /bin/bash --skel /dev/null ${GUEST_USER}
# COPY docker-entrypoint.sh /
WORKDIR /app
COPY . .
# RUN python manage.py collectstatic --noinput && python manage.py migrate --noinput
# RUN chown root: /app && chmod -R 555 /app
# RUN chmod -R 444 /app
# RUN mkdir submissions && chmod -R 777 submissions
# RUN chown guest: /app/submissions
# USER ${GUEST_USER}
CMD daphne codechallenge.asgi:application --port $PORT --bind 0.0.0.0 -v2
# CMD python manage.py runserver $PORT
