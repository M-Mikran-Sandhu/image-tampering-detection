# Project Structure

```
image-tampering-detector/
│
├── Backend (Python + Flask)
│   ├── app.py                      # Flask API server
│   └── requirements.txt            # Python dependencies
│
├── Frontend (React + Vite)
│   ├── index.html                  # HTML entry point
│   ├── package.json                # Node dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── tailwind.config.js          # Tailwind CSS config
│   ├── postcss.config.js           # PostCSS config
│   ├── .gitignore                  # Git ignore rules
│   │
│   └── src/
│       ├── main.jsx                # React entry point
│       ├── App.jsx                 # Main App component
│       ├── ImageTamperingDetector.jsx  # Main detector component
│       └── index.css               # Global styles with Tailwind
│
└── README.md                       # Documentation
```

## File Descriptions

### Backend Files

**app.py**
- Flask server with REST API
- Image analysis endpoints
- ELA (Error Level Analysis) implementation
- Metadata extraction
- Tampering detection algorithms

**requirements.txt**
- Flask, Pillow, NumPy, Flask-CORS

### Frontend Files

**src/ImageTamperingDetector.jsx**
- Main React component
- Image upload interface
- Results display
- ELA visualization
- Analysis metrics

**src/App.jsx**
- Root application component
- Imports and renders ImageTamperingDetector

**src/main.jsx**
- React application entry point
- Renders App component into DOM

**src/index.css**
- Tailwind CSS directives
- Global styles

**index.html**
- HTML template
- Root div for React
- Script tag for main.jsx

**vite.config.js**
- Vite configuration
- React plugin setup
- Dev server port (3000)

**tailwind.config.js**
- Tailwind CSS configuration
- Content paths for purging
- Theme customization

**postcss.config.js**
- PostCSS configuration
- Tailwind and Autoprefixer plugins

**package.json**
- NPM dependencies
- Scripts (dev, build, preview)
- React, Vite, Tailwind

**.gitignore**
- Node modules
- Build artifacts
- Python cache
- Environment files

## Setup Order

1. Set up backend first (Python)
2. Set up frontend (Node.js/Vite)
3. Start both servers
4. Access app at http://localhost:3000

## Ports

- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:3000
