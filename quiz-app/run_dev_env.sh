#!/bin/bash

echo "Lancement du backend..."
(cd quiz-api && ./venv/Scripts/python.exe ./app.py) &

echo "Lancement du frontend..."
(cd quiz-ui && npm run dev) &

wait