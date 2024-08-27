@echo off
echo Checking for existing venv...
if exist .venv\ (
    echo venv exists already.
) else (
    echo venv doesn't exist. Creating venv
    py -m venv .venv
)

echo Activating venv...
call .venv\Scripts\activate.bat

echo Checking pip up to date...
python -m pip install --upgrade pip
call python -m pip --version

echo Checking required packages...
python -m pip install -r requirements.txt
echo Packages checked

echo Starting...
python main.py --log-level INFO

