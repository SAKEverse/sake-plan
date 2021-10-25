call %USERPROFILE%\miniconda3\Scripts\activate.bat
call %USERPROFILE%\AppData\Local\Continuum\anaconda3\Scripts\activate.bat
cd %USERPROFILE%\Documents\GitHub\sake-plan
pipenv run python sake.py
SLEEP 100