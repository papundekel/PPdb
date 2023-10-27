#/usr/bin/env sh

cd backend/ && \
alembic --config backend/migrations/alembic.ini upgrade head
