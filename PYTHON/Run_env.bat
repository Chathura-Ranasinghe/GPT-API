@echo off

echo Create openai virtual environment
python -m venv openai-env

echo Activate...
call openai-env\Scripts\activate

echo Install the OpenAI Python library...
pip install --upgrade openai

echo Running...
python -c "import run_script; run_script.main()"

rem Pause to keep the command prompt window open (optional)
pause
