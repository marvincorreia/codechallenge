FROM python:3.7-slim-buster
COPY . /app
ENV PORT=8000
EXPOSE 8000/tcp
WORKDIR /app
RUN apt-get update
RUN apt-get install 
RUN sudo apt-get install -y postgresql \
libpq5 \
libpq-dev
# RUN pip install pipenv
# RUN pipenv sync
# CMD pipenv run daphne codechallenge.asgi:application --port $PORT --bind 0.0.0.0 -v2
