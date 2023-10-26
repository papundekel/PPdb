#!/usr/bin/env sh

cd backend/ && \
PYTHONPATH=backend/ python -m backend > ../tmp/openapi.json && \
cd - && \
openapi-generator generate --input-spec tmp/openapi.json --generator-name typescript-fetch --output frontend/ppdb-frontend-api/src --additional-properties=importFileExtension=.js && \
npm run --prefix frontend/ppdb-frontend-api/ build
