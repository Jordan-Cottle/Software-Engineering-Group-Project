python3 -m venv .venv

if [[ $? -ne 0 ]]; then
    echo "Installing on windows"
    python -m venv .venv
fi

if [[ -d .venv/bin ]]
then
    windows=false
else
    windows=true
fi

home_dir=$(pwd)

if [[ $windows == "true" ]]
then
    echo "Activating windows virtual environment"
    activate=.venv/Scripts/activate
    include=".venv/Lib/site-packages/include.pth"
    home_dir=${home_dir//\/c\//C:\/}
else  # Not windows
    echo "Activating linux virtual environment"
    activate=.venv/bin/activate
    include="$(find -name site-packages)/include.pth"
fi

note_14="${home_dir}/note_14"

source $activate

pip install -r requirements.txt

echo $home_dir > $include
echo $note_14 >> $include

# Generate secret key for use by the application to manage sessions
secret_key="SECRET_KEY = $(python -c 'import os; print(os.urandom(16))')"
echo $secret_key > note_14/server/secrets.py
