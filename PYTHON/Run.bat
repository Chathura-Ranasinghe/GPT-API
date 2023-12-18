@echo off

echo Activate openai virtual environment
call openai-env\Scripts\activate

echo Running...
python -c "import run_script; run_script.main()"

rem Pause to keep the command prompt window open (optional)
pause

