#!/usr/bin/env sh

mkdir --parents tmp/ backend/static/ && \
cd backend/ && \
PYTHONPATH=backend/ python -m backend > ../tmp/openapi.json && \
cd - && \
npm install --prefix frontend/ppdb-frontend-api/ && \
rm -rf frontend/ppdb-frontend-api/src/ && \
npm run --prefix frontend/ppdb-frontend-api/ generate -- generate --input-spec ../../tmp/openapi.json --generator-name typescript-fetch --output src/ --additional-properties=importFileExtension=.js && \
npm run --prefix frontend/ppdb-frontend-api/ build && \
rm -rf frontend/ppdb-frontend-api/node_modules/ppdb-frontend-api/ && \
npm install --prefix frontend/ppdb-frontend/ --install-links=true
