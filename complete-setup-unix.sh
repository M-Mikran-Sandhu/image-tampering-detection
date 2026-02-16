#!/bin/bash

echo "========================================"
echo "Image Tampering Detector - Complete Setup"
echo "========================================"
echo ""

echo "[1/6] Creating project structure..."

# Create src directory
mkdir -p src

# Create main.jsx
cat > src/main.jsx << 'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOF

# Create App.jsx
cat > src/App.jsx << 'EOF'
import ImageTamperingDetector from './ImageTamperingDetector'

function App() {
  return <ImageTamperingDetector />
}

export default App
EOF

# Create index.css
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

echo "[2/6] Files created successfully!"

echo "[3/6] Creating Python virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    echo "Make sure Python 3 is installed"
    exit 1
fi

echo "[4/6] Activating virtual environment..."
source venv/bin/activate

echo "[5/6] Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[6/6] Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "Warning: Node dependencies installation had issues"
    echo "You may need to run 'npm install' manually"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Your project structure:"
echo "  src/"
echo "  ├── main.jsx"
echo "  ├── App.jsx"
echo "  ├── index.css"
echo "  └── ImageTamperingDetector.jsx"
echo ""
echo "To start the application:"
echo "  1. Backend: ./start-backend.sh"
echo "  2. Frontend: npm run dev (in a new terminal)"
echo ""
