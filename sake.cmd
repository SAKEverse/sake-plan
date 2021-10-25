call %USERPROFILE%\miniconda3\Scripts\activate.bat
call %USERPROFILE%\AppData\Local\Continuum\anaconda3\Scripts\activate.bat
cd %USERPROFILE%\Documents\GitHub\sake-plan
pip install pipenv
IF EXIST Pipfile.lock (
    echo "Environment already installed"
) ELSE (
    pipenv install
)
pipenv run python sake.py
SLEEP 100