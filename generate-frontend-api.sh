#!/usr/bin/env sh

mkdir --parents tmp/ backend/static/ && \
cd backend/ && \
PYTHONPATH=backend/ python -m backend > ../tmp/openapi.json && \
cd - && \
npm install --prefix frontend/ppdb-frontend-api/ && \
npm run --prefix frontend/ppdb-frontend-api/ generate -- generate --input-spec ../../tmp/openapi.json --generator-name typescript-fetch --output src/ --additional-properties=importFileExtension=.js && \
npm run --prefix frontend/ppdb-frontend-api/ build
