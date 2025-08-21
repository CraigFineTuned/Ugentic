@echo off
setlocal enabledelayedexpansion

rem Define output file
set "output_file=directory_structure.txt"

rem Start fresh
echo Listing directory structure... > "%output_file%"

rem Check for .venv and .git directories
if exist ".venv" echo [.venv exists - Virtual Environment] >> "%output_file%"
if exist ".git" echo [.git exists - Git Repository] >> "%output_file%"

rem List all files except those in .venv and .git directories
(for /f "delims=" %%A in ('dir /s /b /a-d ^| findstr /v /i "\.venv\\ \.git\\"') do (
    echo %%A
)) >> "%output_file%"

rem Completion message
echo Directory structure exported to "%output_file%"
