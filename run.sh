echo Checking for existing venv..
if [ -d ".venv" ]; then
    echo venv exists already
else
    echo venv doesnt exist. Creating venv,
    python3 -m venv .venv
fi

echo Activating venv
source ./.venv/bin/activate

echo Checking pip up to date...
python3 -m pip install --upgrade pip
python3 -m pip --version

echo Checking required packages...
python3 -m pip install -r requirements.txt
echo Packages checked

echo Starting...
python3 main.py
