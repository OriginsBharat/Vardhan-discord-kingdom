@echo off
echo "Installing necessary Python libraries... This may take a moment."
pip install -r requirements.txt

echo "Launching My AI World Setup Wizard..."
python SETUP_THE_WORLD.py
pause