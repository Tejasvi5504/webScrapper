@echo off
echo Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Installing Playwright browsers...
python -m playwright install

echo.
echo Starting the application...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
