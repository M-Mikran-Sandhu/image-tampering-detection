# Image Tampering Detector

A full-stack web application that uses forensic analysis techniques to detect if an image has been digitally manipulated or tampered with.

## 🚀 Quick Start

**Backend (Terminal 1):**

```bash
pip install -r requirements.txt
python app.py
```

**Frontend (Terminal 2):**

```bash
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser!

## Features

- **Error Level Analysis (ELA)**: Detects compression inconsistencies that indicate tampering
- **Metadata Inspection**: Examines EXIF data for signs of editing software
- **Quality Analysis**: Analyzes statistical patterns in image data
- **Visual Feedback**: Shows ELA heatmap highlighting potential tampered areas
- **Confidence Scoring**: Provides tampering probability with detailed reasoning

## Technologies

### Backend (Python)

- Flask - Web framework
- Pillow - Image processing
- NumPy - Numerical analysis
- Flask-CORS - Cross-origin resource sharing

### Frontend (React + Vite)

- Vite - Fast build tool and dev server
- React - UI framework
- Tailwind CSS - Styling
- Lucide React - Icons

## Setup Instructions

### Backend Setup

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Run the Flask server:**

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Frontend Setup (Vite + React)

1. **The project structure is already set up for you!** All files are included.

2. **Install dependencies:**

```bash
npm install
```

3. **Start the development server:**

```bash
npm run dev
```

The app will open at `http://localhost:3000`

**Alternative - Manual Setup:**

If you want to set up from scratch:

```bash
# Create Vite React project
npm create vite@latest image-tampering-detector -- --template react
cd image-tampering-detector

# Install dependencies
npm install
npm install lucide-react

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Copy the provided files:
# - src/ImageTamperingDetector.jsx
# - src/App.jsx
# - src/main.jsx
# - src/index.css
# - tailwind.config.js
# - postcss.config.js
# - vite.config.js

# Start development server
npm run dev
```

## Usage

1. Start both the Python backend and React frontend
2. Click the upload area or drag and drop an image
3. Click "Analyze Image" button
4. View the results:
   - Overall assessment (Likely Authentic, Possibly Tampered, Likely Tampered)
   - Confidence score
   - ELA visualization (bright areas indicate potential tampering)
   - Metadata information
   - Detailed analysis findings

## How It Works

### Error Level Analysis (ELA)

ELA works by resaving the image at a known quality level and comparing it to the original. Areas that have been edited or tampered with will show different error levels because they've already been compressed differently than the rest of the image.

- **Bright areas in ELA**: Indicate recent edits or inconsistent compression
- **Uniform dark areas**: Suggest original, unmodified content
- **Patchy patterns**: May indicate copy-paste manipulation

### Metadata Analysis

Examines EXIF data for:

- Editing software signatures (Photoshop, GIMP, etc.)
- Missing metadata (often stripped during editing)
- Inconsistent timestamps or camera information

### Quality Metrics

Analyzes statistical properties like:

- Brightness distribution
- Color variance
- Compression artifacts

## Limitations

- **Not 100% accurate**: This tool provides indicators, not definitive proof
- **False positives**: Heavily compressed images or images with filters may show high tampering scores
- **Modern techniques**: Advanced manipulation techniques may not be detected
- **File format**: Works best with JPEG images (where compression analysis is most effective)

## Tips for Best Results

1. Use original, high-quality images for analysis
2. Avoid re-compressed or heavily filtered images
3. Consider multiple indicators together, not just the score
4. Use this as one tool among many for forensic analysis

## Example Scenarios

**Likely Authentic:**

- Low ELA variance
- Complete EXIF metadata
- No editing software tags
- Consistent compression throughout

**Likely Tampered:**

- High ELA variance in specific regions
- Missing or stripped metadata
- Evidence of editing software
- Inconsistent compression patterns

## API Endpoints

### POST /api/analyze

Analyzes an uploaded image for tampering

**Request:**

- Method: POST
- Content-Type: multipart/form-data
- Body: image file

**Response:**

```json
{
  "success": true,
  "ela_image": "base64_encoded_image",
  "metadata": {...},
  "quality_metrics": {...},
  "tampering_analysis": {
    "score": 45,
    "assessment": "Possibly Tampered",
    "confidence": "45%",
    "reasons": [...]
  }
}
```

### GET /api/health

Health check endpoint

## License

MIT

## Disclaimer

This tool is for educational and research purposes. Results should not be used as sole evidence of image manipulation in legal or professional contexts. Always consult forensic experts for critical analysis.
