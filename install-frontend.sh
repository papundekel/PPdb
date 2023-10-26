#!/usr/bin/env sh

rm -rf backend/static/js backend/static/node_modules && \
mkdir --parents tmp/ && \
npm install --prefix frontend/ppdb-frontend/ --install-links=true && \
npm pack frontend/ppdb-frontend/ --pack-destination tmp/ && \
npm install --omit=dev --global --prefix tmp/ file://./tmp/ppdb-frontend-1.0.0.tgz && \
mv tmp/lib/node_modules/ppdb-frontend/dist backend/static/js && \
mv tmp/lib/node_modules/ppdb-frontend/node_modules backend/static/
