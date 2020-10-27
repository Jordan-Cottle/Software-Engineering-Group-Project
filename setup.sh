python3 -m venv .venv

ls .venv/bin 2>/dev/null

if [[ $? -eq 2 ]]
then
    windows=true
else
    windows=false
fi

echo $windows

note_14="$(pwd)/note_14"
if [[ $windows == "true" ]]
then
    echo "Activating windows virtual environment"
    activate=.venv/Scripts/activate
    include=".venv/Lib/site-packages/include.pth"
else  # Not windows
    echo "Activating linux virtual environment"
    activate=.venv/bin/activate
    include="$(find -name site-packages)/include.pth"
fi

source $activate

pip install --upgrade pip
pip install -r requirements.txt

echo $note_14 > $include