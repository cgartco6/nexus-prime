#!/bin/bash

echo "Setting up Nexus Prime..."

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

mkdir -p workspace projects web_interface/templates

echo "Setup complete! Don't forget to:"
echo "1. Copy .env.example to .env and add your API keys"
echo "2. Run 'source venv/bin/activate' to activate the virtual environment"
echo "3. Run 'python web_interface/app.py' to start the web interface"
