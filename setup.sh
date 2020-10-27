python -m venv .venv

ls .venv/bin 2>/dev/null

if [[ $? -eq 2 ]]
then  # Windows
    source .venv/Scripts/activate
else  # Not windows
    source .venv/bin/activate
fi

pip install --updrade pip
pip install -r requirements.txt