python3 -m venv .venv

if [[ -d .venv/bin ]]
then
    windows=false
else
    windows=true
fi

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

pwd
echo "$(pwd)" > $include
echo $note_14 >> $include