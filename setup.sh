python3 -m venv .venv

if [[ $? -ne 0 ]]; then
    python -m venv .venv
fi

if [[ -d .venv/bin ]]
then
    windows=false
else
    windows=true
fi

home_dir=$(pwd)
note_14="$(pwd)/note_14"

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

source $activate

pip install --upgrade pip
pip install -r requirements.txt

echo $home_dir > $include
echo $note_14 >> $include