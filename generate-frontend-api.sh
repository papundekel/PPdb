#!/usr/bin/env sh

export PATH="/usr/lib/jvm/java-21-openjdk/bin/:$PATH"

mkdir --parents tmp/ backend/static/ && \
cd backend/ && \
PYTHONPATH=backend/ python -m backend > ../tmp/openapi.json && \
cd - && \
rm -rf frontend/ppdb-frontend-api/src/ && \
mkdir --parents frontend/ppdb-frontend-api/src/ && \
touch frontend/ppdb-frontend-api/src/dummy.ts && \
npm install --prefix frontend/ppdb-frontend-api/ && \
rm frontend/ppdb-frontend-api/src/dummy.ts && \
npm run --prefix frontend/ppdb-frontend-api/ generate -- generate --input-spec ../../tmp/openapi.json --generator-name typescript-fetch --output src/ --additional-properties=importFileExtension=.js && \
npm run --prefix frontend/ppdb-frontend-api/ build && \
rm -rf frontend/ppdb-frontend/node_modules/ppdb-frontend-api/ && \
npm install --prefix frontend/ppdb-frontend/ --install-links=true
