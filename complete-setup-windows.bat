@echo off
echo ========================================
echo Image Tampering Detector - Complete Setup
echo ========================================
echo.

echo [1/6] Creating project structure...

REM Create src directory
if not exist "src" mkdir src

REM Create main.jsx
echo import React from 'react' > src\main.jsx
echo import ReactDOM from 'react-dom/client' >> src\main.jsx
echo import App from './App.jsx' >> src\main.jsx
echo import './index.css' >> src\main.jsx
echo. >> src\main.jsx
echo ReactDOM.createRoot(document.getElementById('root')).render( >> src\main.jsx
echo   ^<React.StrictMode^> >> src\main.jsx
echo     ^<App /^> >> src\main.jsx
echo   ^</React.StrictMode^>, >> src\main.jsx
echo ^) >> src\main.jsx

REM Create App.jsx
echo import ImageTamperingDetector from './ImageTamperingDetector' > src\App.jsx
echo. >> src\App.jsx
echo function App() { >> src\App.jsx
echo   return ^<ImageTamperingDetector /^> >> src\App.jsx
echo } >> src\App.jsx
echo. >> src\App.jsx
echo export default App >> src\App.jsx

REM Create index.css
echo @tailwind base; > src\index.css
echo @tailwind components; >> src\index.css
echo @tailwind utilities; >> src\index.css

echo [2/6] Files created successfully!

echo [3/6] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    echo Make sure Python is installed and in your PATH
    pause
    exit /b 1
)

echo [4/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [5/6] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [6/6] Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo Warning: Node dependencies installation had issues
    echo You may need to run 'npm install' manually
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your project structure:
echo   src/
echo   ├── main.jsx
echo   ├── App.jsx
echo   ├── index.css
echo   └── ImageTamperingDetector.jsx
echo.
echo To start the application:
echo   1. Backend: Double-click start-backend.bat
echo   2. Frontend: Run 'npm run dev' in a new terminal
echo.
pause
