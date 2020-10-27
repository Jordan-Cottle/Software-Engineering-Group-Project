ls .venv/bin 2>/dev/null

if [[ $? -eq 2 ]]
then  # Windows
    source .venv/Scripts/activate
else  # Not windows
    source .venv/bin/activate
fi

python note_14/app.py