#!/bin/bash
set -e

echo "Installing dependencies..."

cd ../barbershop-frontend
npm install

echo "Frontend dependencies installed."

cd ../barbershop
pip install -r requirements.txt

echo "Backend dependencies installed."
