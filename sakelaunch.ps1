
# check if pipenv is installed 
$cmdName = 'pipenv'
if (Get-Command $cmdName -errorAction SilentlyContinue)
{
    "$cmdName found"
}else{
    pip install pipenv
}

# check if pipenv install has been run
$pipinstall = 'Pipfile.lock'
if (Test-Path -Path $pipinstall)
{
    "$cmdName found"
}else{
    pipenv install
}


#$Folder = 'Miniconda3
$doc_path = [IO.Path]::Combine('C:\', $doc_path,  'Miniconda3\Scripts\activate.bat')
if (Test-Path -Path $doc_path) {
    $full_path = [IO.Path]::Combine('C:\', $doc_path,  'Miniconda3\Scripts\activate.bat')
} else {
    #$full_path = [IO.Path]::Combine('C:\', $doc_path,  'AppData\Local\Continuum\anaconda3\Scripts\activate.bat')
}

# activate conda
$full_path

# run sake
pipenv run sake.py
