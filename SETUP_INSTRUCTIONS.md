# 🔧 Setup Instructions - Fix Missing Files Error

## Problem
You're seeing: `Failed to load url /src/main.jsx. Does the file exist?`

This means the `src` folder and files weren't created in your project directory.

---

## ✅ Quick Fix - Option 1: Use the Complete Setup Script

I've created new automated scripts that create ALL files for you:

### Windows:
```cmd
complete-setup-windows.bat
```

### Mac/Linux:
```bash
chmod +x complete-setup-unix.sh
./complete-setup-unix.sh
```

These scripts will:
- ✅ Create the `src` folder
- ✅ Create all missing files (main.jsx, App.jsx, index.css)
- ✅ Set up Python virtual environment
- ✅ Install all dependencies

---

## ✅ Quick Fix - Option 2: Manual File Creation

If you want to do it manually:

### Step 1: Create the `src` folder
In your project root (where `package.json` is), create a folder named `src`

### Step 2: Copy these files INTO the `src` folder:
- `main.jsx` (from downloads)
- `App.jsx` (from downloads)
- `index.css` (from downloads)
- `ImageTamperingDetector.jsx` (from downloads)

### Step 3: Your structure should look like:

```
your-project/
├── src/                          ← CREATE THIS FOLDER
│   ├── main.jsx                  ← MOVE HERE
│   ├── App.jsx                   ← MOVE HERE
│   ├── index.css                 ← MOVE HERE
│   └── ImageTamperingDetector.jsx ← MOVE HERE
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── app.py
├── requirements.txt
└── README.md
```

### Step 4: Run Vite again
```bash
npm run dev
```

---

## ✅ Quick Fix - Option 3: Start Fresh

If nothing is working, here's the cleanest approach:

### 1. Create a new folder for your project:
```bash
mkdir image-tampering-detector
cd image-tampering-detector
```

### 2. Copy ALL downloaded files into this folder

### 3. Make sure you have this structure:
```
image-tampering-detector/
├── src/                    ← Must exist!
│   ├── main.jsx
│   ├── App.jsx
│   ├── index.css
│   └── ImageTamperingDetector.jsx
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── app.py
└── requirements.txt
```

### 4. Run the complete setup:

**Windows:**
```cmd
complete-setup-windows.bat
```

**Mac/Linux:**
```bash
chmod +x complete-setup-unix.sh
./complete-setup-unix.sh
```

---

## 🔍 Verify Your Setup

After setup, check if these files exist:

```bash
# Check if src folder exists
dir src         # Windows
ls src          # Mac/Linux

# You should see:
# main.jsx
# App.jsx
# index.css
# ImageTamperingDetector.jsx
```

---

## 🚀 Starting the App (After Fix)

### Terminal 1 - Backend:
**Windows:**
```cmd
start-backend.bat
```

**Mac/Linux:**
```bash
./start-backend.sh
```

### Terminal 2 - Frontend:
```bash
npm run dev
```

### Open Browser:
```
http://localhost:3000
```

---

## ❓ Still Having Issues?

### Error: "Cannot find module"
- Make sure ALL files are in the correct locations
- Run `npm install` again

### Error: "Port 3000 already in use"
```bash
npm run dev -- --port 3001
```

### Error: "Python not found"
- Install Python from python.org
- Check installation: `python --version`

### Frontend works but backend doesn't connect
- Make sure backend is running on port 5000
- Check: http://localhost:5000/api/health
- Make sure virtual environment is activated: you should see `(venv)` in terminal

---

## 📋 Checklist

Before running `npm run dev`, verify:

- [ ] `src` folder exists
- [ ] `src/main.jsx` exists
- [ ] `src/App.jsx` exists
- [ ] `src/index.css` exists
- [ ] `src/ImageTamperingDetector.jsx` exists
- [ ] `index.html` exists in root
- [ ] `package.json` exists in root
- [ ] `vite.config.js` exists in root
- [ ] Ran `npm install`

---

## 💡 Understanding the Issue

The error happened because:

1. Vite looks for `src/main.jsx` as the entry point (defined in `index.html`)
2. The `src` folder wasn't created in your project directory
3. Files were downloaded but not organized into the correct folder structure

The **complete-setup** scripts fix this by:
- Creating the `src` folder
- Creating all necessary files
- Setting up everything in one go

---

Need more help? Check the error messages carefully - they usually tell you exactly which file is missing!
