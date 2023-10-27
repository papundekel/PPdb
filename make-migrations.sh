#/usr/bin/env sh

if [ -z "$1" ]; then
    echo "Usage: $0 <message>"
    exit 1
fi

cd backend/ && \
pwd && \
alembic --config backend/migrations/alembic.ini revision --autogenerate --message "$1"
