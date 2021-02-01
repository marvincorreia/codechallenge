#!/bin/bash
RUN chown root: /app && chmod -R 100 /app
chmod -R 777 /app/submissions
daphne codechallenge.asgi:application --port $PORT --bind 0.0.0.0 -v2