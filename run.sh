ls .venv/bin 2>/dev/null

if [[ $? -eq 2 ]]
then  # Windows
    source .venv/Scripts/activate
else  # Not windows
    source .venv/bin/activate
fi

pushd note_14
python app.py
popd