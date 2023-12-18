@echo off

echo Activate openai virtual environment
call openai-env\Scripts\activate

echo Running
rem call python langchain-test_Chat.py 
call python langchain-test_Techlead.py

rem Pause to keep the command prompt window open (optional)
pause