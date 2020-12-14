if [[ -d .venv/bin ]]; then
    source .venv/bin/activate
elif [[ -d .venv/Scripts ]]; then
    source .venv/Scripts/activate
else
    echo "ERROR: Unable to find virtual environment, please run setup.sh to setup the environment";
    exit 1
fi

pytest --cov=note_14 tests