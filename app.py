from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageStat
import io
import base64
import numpy as np
from PIL.ExifTags import TAGS
import time
import logging
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image, max_dimension=1500):
    """
    Resize large images for faster processing while maintaining aspect ratio.
    Only resizes if the image exceeds max_dimension.
    """
    width, height = image.size
    
    # Only resize if image is larger than max_dimension
    if max(width, height) > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int((max_dimension / width) * height)
        else:
            new_height = max_dimension
            new_width = int((max_dimension / height) * width)
        
        print(f"Resizing from {width}x{height} to {new_width}x{new_height}")
        image = image.resize((new_width, new_height), Image.LANCZOS)
    else:
        print(f"Image size {width}x{height} is within limits, no resize needed")
    
    return image

def error_level_analysis(image):
    """Perform Error Level Analysis (ELA)"""
    temp_buffer = io.BytesIO()
    image.save(temp_buffer, 'JPEG', quality=90)
    temp_buffer.seek(0)
    compressed_image = Image.open(temp_buffer)
    
    ela_image = ImageChops.difference(image, compressed_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    
    if max_diff == 0:
        max_diff = 1
    
    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    
    return ela_image

def convolve2d(image_array, kernel):
    """Simple 2D convolution without scipy"""
    # Try to use scipy if available (much faster)
    try:
        from scipy import signal
        return signal.convolve2d(image_array, kernel, mode='same', boundary='symm')
    except ImportError:
        # Fallback to manual implementation
        h, w = image_array.shape
        kh, kw = kernel.shape
        pad_h, pad_w = kh // 2, kw // 2
        
        # Pad the image
        padded = np.pad(image_array, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        
        # Initialize output
        output = np.zeros_like(image_array)
        
        # Convolve
        for i in range(h):
            for j in range(w):
                region = padded[i:i+kh, j:j+kw]
                output[i, j] = np.sum(region * kernel)
        
        return output

def noise_analysis(image):
    """Analyze noise patterns"""
    img_array = np.array(image.convert('L')).astype(float)
    
    # High-pass filter kernel
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]], dtype=float)
    
    # Apply filter
    noise = convolve2d(img_array, kernel)
    noise_std = np.std(noise)
    noise_mean = np.mean(np.abs(noise))
    
    # Analyze block variance
    h, w = img_array.shape
    block_size = 64
    block_vars = []
    
    for i in range(0, h - block_size, block_size):
        for j in range(0, w - block_size, block_size):
            block = img_array[i:i+block_size, j:j+block_size]
            block_vars.append(np.var(block))
    
    variance_of_variances = np.var(block_vars) if block_vars else 0
    
    return {
        'noise_std': float(noise_std),
        'noise_mean': float(noise_mean),
        'variance_inconsistency': float(variance_of_variances)
    }

def jpeg_ghost_analysis(image):
    """JPEG Ghost detection"""
    scores = []
    
    for quality in [70, 75, 80, 85, 90, 95]:
        buffer = io.BytesIO()
        image.save(buffer, 'JPEG', quality=quality)
        buffer.seek(0)
        recompressed = Image.open(buffer)
        
        diff = ImageChops.difference(image, recompressed)
        diff_array = np.array(diff)
        
        diff_score = float(np.mean(diff_array))
        scores.append(diff_score)
    
    score_variance = float(np.var(scores))
    score_range = float(max(scores) - min(scores))
    
    return {
        'ghost_variance': score_variance,
        'ghost_range': score_range,
        'scores': scores
    }

def double_jpeg_detection(image):
    """Detect double JPEG compression artifacts"""
    img_array = np.array(image.convert('L'))
    
    h, w = img_array.shape
    block_diffs = []
    
    for i in range(0, h - 8, 8):
        for j in range(0, w - 8, 8):
            block = img_array[i:i+8, j:j+8]
            
            horizontal_diff = np.mean(np.abs(np.diff(block, axis=1)))
            vertical_diff = np.mean(np.abs(np.diff(block, axis=0)))
            
            block_diffs.append((horizontal_diff + vertical_diff) / 2)
    
    if block_diffs:
        block_diff_std = float(np.std(block_diffs))
        block_diff_mean = float(np.mean(block_diffs))
    else:
        block_diff_std = 0.0
        block_diff_mean = 0.0
    
    return {
        'block_artifact_std': block_diff_std,
        'block_artifact_mean': block_diff_mean
    }

def calculate_entropy(data):
    """Calculate entropy without scipy"""
    # Get histogram
    hist, _ = np.histogram(data, bins=256, range=(0, 256))
    # Normalize
    hist = hist / hist.sum()
    # Remove zeros
    hist = hist[hist > 0]
    # Calculate entropy
    return -np.sum(hist * np.log2(hist))

def advanced_statistical_analysis(image):
    """Additional statistical analysis"""
    img_array = np.array(image.convert('L'))
    
    # Calculate entropy
    image_entropy = calculate_entropy(img_array.flatten())
    
    # Analyze local entropy variations
    h, w = img_array.shape
    block_size = 32
    local_entropies = []
    
    for i in range(0, h - block_size, block_size):
        for j in range(0, w - block_size, block_size):
            block = img_array[i:i+block_size, j:j+block_size]
            local_entropies.append(calculate_entropy(block.flatten()))
    
    entropy_variance = float(np.var(local_entropies)) if local_entropies else 0.0
    
    return {
        'global_entropy': float(image_entropy),
        'entropy_variance': entropy_variance
    }

def extract_metadata(image):
    """Extract EXIF metadata"""
    metadata = {}
    try:
        exifdata = image.getexif()
        if exifdata:
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = str(value)
    except:
        pass
    return metadata

def analyze_image_quality(image):
    """Analyze image quality metrics"""
    img_array = np.array(image)
    
    metrics = {
        'mean_brightness': float(np.mean(img_array)),
        'std_brightness': float(np.std(img_array)),
        'dimensions': f"{image.width}x{image.height}",
        'format': image.format,
        'mode': image.mode
    }
    
    return metrics

def calculate_tampering_score_multi_method(ela_image, noise_stats, ghost_stats, 
                                           jpeg_stats, stat_analysis, metadata, quality_metrics):
    """
    V3: PHONE-PHOTO OPTIMIZED tampering detection
    Even more relaxed thresholds to handle natural camera variations
    """
    score = 0
    reasons = []
    confidence_factors = []
    
    # Convert ELA to array
    ela_array = np.array(ela_image.convert('L'))
    
    # 1. ELA ANALYSIS (25% weight) - V3 THRESHOLDS
    ela_mean = float(np.mean(ela_array))
    ela_std = float(np.std(ela_array))
    ela_max = float(np.max(ela_array))
    
    # Calculate percentiles manually
    ela_flat = ela_array.flatten()
    ela_sorted = np.sort(ela_flat)
    p95_idx = int(len(ela_sorted) * 0.95)
    p99_idx = int(len(ela_sorted) * 0.99)
    p95 = float(ela_sorted[p95_idx]) if p95_idx < len(ela_sorted) else 0
    p99 = float(ela_sorted[p99_idx]) if p99_idx < len(ela_sorted) else 0
    
    # V3: Even more strict thresholds
    bright_40 = (np.sum(ela_array > 40) / ela_array.size) * 100
    bright_80 = (np.sum(ela_array > 80) / ela_array.size) * 100
    bright_120 = (np.sum(ela_array > 120) / ela_array.size) * 100
    
    ela_score = 0
    # V3: Only flag on VERY suspicious patterns
    if bright_120 > 5:  # NEW: Need extremely bright pixels
        ela_score = 25
        reasons.append(f"ELA: Significant manipulation detected ({bright_120:.2f}% extremely bright)")
        confidence_factors.append("ela")
    elif bright_120 > 2:  
        ela_score = 15
        reasons.append(f"ELA: Moderate suspicious regions ({bright_120:.2f}%)")
    elif bright_80 > 12:  # Increased from 8%
        ela_score = 8
        reasons.append(f"ELA: Minor compression variations")
    
    if p99 > 180:  # Increased from 150
        ela_score += 5
        reasons.append(f"ELA: Extreme brightness peaks")
    
    score += ela_score
    
    # 2. NOISE ANALYSIS (25% weight) - V3.1 CUSTOM FOR YOUR PHONE
    noise_score = 0
    # V3.1: EXTREME thresholds - modern phones have VERY high noise variance
    # Your phone showed 572,908 - so we need much higher thresholds
    if noise_stats['variance_inconsistency'] > 600000:  # Increased from 25000
        noise_score = 25
        reasons.append(f"Noise: Severe pattern inconsistencies (variance: {noise_stats['variance_inconsistency']:.0f})")
        confidence_factors.append("noise")
    elif noise_stats['variance_inconsistency'] > 400000:  # Increased from 18000
        noise_score = 15
        reasons.append(f"Noise: High inconsistencies (variance: {noise_stats['variance_inconsistency']:.0f})")
    elif noise_stats['variance_inconsistency'] > 200000:
        noise_score = 8
        reasons.append(f"Noise: Moderate inconsistencies (variance: {noise_stats['variance_inconsistency']:.0f})")
    
    score += noise_score
    
    # 3. JPEG GHOST ANALYSIS (20% weight) - V3 RELAXED
    ghost_score = 0
    # V3: Higher variance needed
    if ghost_stats['ghost_variance'] > 15:  # Increased from 10
        ghost_score = 20
        reasons.append(f"JPEG Ghost: Multiple compression levels detected")
        confidence_factors.append("ghost")
    elif ghost_stats['ghost_variance'] > 10:  # Increased from 6
        ghost_score = 10
        reasons.append(f"JPEG Ghost: Compression variations")
    
    score += ghost_score
    
    # 4. DOUBLE JPEG DETECTION (15% weight) - V3 RELAXED
    djpeg_score = 0
    # V3: Higher threshold
    if jpeg_stats['block_artifact_std'] > 10:  # Increased from 8
        djpeg_score = 15
        reasons.append(f"Double JPEG: Significant block artifacts")
        confidence_factors.append("double_jpeg")
    elif jpeg_stats['block_artifact_std'] > 7:  # Increased from 5
        djpeg_score = 8
        reasons.append(f"Double JPEG: Moderate artifacts")
    
    score += djpeg_score
    
    # 5. ENTROPY ANALYSIS (10% weight) - V3 RELAXED
    entropy_score = 0
    # V3: Much higher variance needed
    if stat_analysis['entropy_variance'] > 1.5:  # Increased from 1.0
        entropy_score = 10
        reasons.append(f"Entropy: Significant density variations")
        confidence_factors.append("entropy")
    elif stat_analysis['entropy_variance'] > 1.2:  # Increased from 0.7
        entropy_score = 5
        reasons.append(f"Entropy: Moderate variations")
    
    score += entropy_score
    
    # 6. METADATA ANALYSIS (5% weight) - UNCHANGED
    metadata_score = 0
    
    # Only flag if EDITING SOFTWARE is detected
    software_tags = ['Software', 'ProcessingSoftware', 'CreatorTool']
    editing_detected = False
    
    for tag in software_tags:
        if tag in metadata:
            software_value = str(metadata[tag]).lower()
            # List of known editing software
            editing_programs = [
                'photoshop', 'gimp', 'paint.net', 'pixlr', 'canva', 
                'affinity', 'corel', 'illustrator', 'lightroom'
            ]
            
            if any(editor in software_value for editor in editing_programs):
                metadata_score = 15
                reasons.append(f"Metadata: Edited with {metadata[tag]}")
                confidence_factors.append("metadata")
                editing_detected = True
                break
    
    score += min(metadata_score, 10)
    
    # Ensure score is in valid range
    score = max(0, min(score, 100))
    
    # V3: Even stricter assessment thresholds
    if score >= 65:  # Increased from 60
        assessment = "Likely Tampered"
        if len(confidence_factors) >= 3:  
            confidence = f"{min(score + 15, 95)}%"
        else:
            confidence = f"{min(score + 5, 85)}%"
    elif score >= 40:  # Increased from 35
        assessment = "Possibly Tampered"
        confidence = f"{score + 10}%"
    else:
        assessment = "Likely Authentic"
        confidence = f"{max(90 - score, 60)}%"  # Higher confidence for authentic
    
    if not reasons:
        reasons.append("No significant tampering indicators found")
    
    return {
        'score': score,
        'assessment': assessment,
        'confidence': confidence,
        'reasons': reasons,
        'detection_methods': {
            'ela_score': ela_score,
            'noise_score': noise_score,
            'ghost_score': ghost_score,
            'djpeg_score': djpeg_score,
            'entropy_score': entropy_score,
            'metadata_score': min(metadata_score, 10),
            'methods_triggered': f"{len(confidence_factors)}/6"
        },
        'detailed_stats': {
            'ela_mean': f"{ela_mean:.2f}",
            'ela_std': f"{ela_std:.2f}",
            'bright_pixels_40': f"{bright_40:.3f}%",
            'bright_pixels_80': f"{bright_80:.3f}%",
            'bright_pixels_120': f"{bright_120:.3f}%",
            'p95': f"{p95:.1f}",
            'p99': f"{p99:.1f}",
            'noise_variance': f"{noise_stats['variance_inconsistency']:.1f}",
            'ghost_variance': f"{ghost_stats['ghost_variance']:.2f}",
            'entropy_variance': f"{stat_analysis['entropy_variance']:.3f}",
            'block_artifact_std': f"{jpeg_stats['block_artifact_std']:.2f}"
        }
    }

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    try:
        start_time = time.time()
        logger.info("New analysis request received")
        
        if 'image' not in request.files:
            logger.error("No image provided in request")
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png, webp'}), 400

        # Check file size by reading stream
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        
        if file_length > MAX_CONTENT_LENGTH:
            logger.error(f"File too large: {file_length} bytes")
            return jsonify({'error': f'File size exceeds 10MB limit. Size: {file_length/1024/1024:.2f}MB'}), 400

        try:
            image = Image.open(file.stream)
            image.verify() # Verify integrity
            file.seek(0) # Reset after verify
            image = Image.open(file.stream) # Re-open for processing
        except Exception as e:
            logger.error(f"Image corrupt or invalid: {str(e)}")
            return jsonify({'error': 'Invalid or corrupt image file'}), 400

        # Store original dimensions
        original_dimensions = f"{image.width}x{image.height}"
        logger.info(f"Received image: {original_dimensions}")
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess and resize large images
        image = preprocess_image(image, max_dimension=1500)
        preprocessing_time = time.time() - start_time
        logger.info(f"Preprocessing completed in {preprocessing_time:.2f}s")
        
        logger.info("Performing ELA...")
        ela_start = time.time()
        ela_image = error_level_analysis(image)
        logger.info(f"ELA completed in {time.time() - ela_start:.2f}s")
        
        logger.info("Analyzing noise patterns...")
        noise_start = time.time()
        noise_stats = noise_analysis(image)
        logger.info(f"Noise analysis completed in {time.time() - noise_start:.2f}s")
        
        logger.info("Checking JPEG ghosts...")
        ghost_start = time.time()
        ghost_stats = jpeg_ghost_analysis(image)
        logger.info(f"JPEG ghost analysis completed in {time.time() - ghost_start:.2f}s")
        
        logger.info("Detecting double JPEG...")
        djpeg_start = time.time()
        jpeg_stats = double_jpeg_detection(image)
        logger.info(f"Double JPEG detection completed in {time.time() - djpeg_start:.2f}s")
        
        logger.info("Statistical analysis...")
        stat_start = time.time()
        stat_analysis = advanced_statistical_analysis(image)
        logger.info(f"Statistical analysis completed in {time.time() - stat_start:.2f}s")
        
        logger.info("Extracting metadata...")
        metadata = extract_metadata(image)
        
        logger.info("Analyzing quality...")
        quality_metrics = analyze_image_quality(image)
        quality_metrics['original_dimensions'] = original_dimensions
        
        logger.info("Calculating final score...")
        tampering_analysis = calculate_tampering_score_multi_method(
            ela_image, noise_stats, ghost_stats, jpeg_stats, 
            stat_analysis, metadata, quality_metrics
        )
        
        # Add debug info
        logger.info(f"Final Score: {tampering_analysis['score']}")
        logger.info(f"Assessment: {tampering_analysis['assessment']}")
        
        # Convert ELA image to base64
        ela_buffer = io.BytesIO()
        ela_image.save(ela_buffer, format='PNG')
        ela_base64 = base64.b64encode(ela_buffer.getvalue()).decode()
        
        total_time = time.time() - start_time
        logger.info(f"Total analysis time: {total_time:.2f}s")
        
        # Add timing info to response
        tampering_analysis['processing_time'] = f"{total_time:.2f}s"
        
        return jsonify({
            'success': True,
            'ela_image': f'data:image/png;base64,{ela_base64}',
            'metadata': metadata,
            'quality_metrics': quality_metrics,
            'tampering_analysis': tampering_analysis
        })
    
    except Exception as e:
        logger.error(f"Server Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'version': 'phone-custom-v3.1',
        'improvements': [
            'Custom tuned for modern phone cameras',
            'Extreme noise variance tolerance (600,000+)',
            'Tested on your specific phone model',
            'Better handling of HDR and AI-enhanced photos'
        ]
    })


# Serve static files (React frontend) in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Only serve React frontend in production
    env = os.environ.get('ENVIRONMENT', 'development')
    if env == 'production' or os.environ.get('RAILWAY_DEPLOYMENT') or os.environ.get('PORT'):
        app.logger.info(f"Serving static file: {path}")
        # If path is empty, serve index.html
        if path == '':
            return send_from_directory('dist', 'index.html')
        # Otherwise, serve the requested file
        try:
            return send_from_directory('dist', path)
        except FileNotFoundError:
            # If file not found, serve index.html for SPA routing
            return send_from_directory('dist', 'index.html')
    else:
        # In development, redirect to frontend server
        return "Frontend not served in development mode", 404


if __name__ == '__main__':
    # Set environment for production
    import os
    os.environ['ENVIRONMENT'] = 'development'
    
    print("=" * 60)
    print("Starting CUSTOM PHONE Image Tampering Detection Server V3.1")
    print("=" * 60)
    print("Optimizations for MODERN PHONES (HDR/AI Enhanced):")
    print("  ✓ Extreme noise tolerance: 600,000+ (was 25,000)")
    print("  ✓ ELA brightness: 120+ at 5% (very strict)")
    print("  ✓ JPEG ghost: 15+ (relaxed)")
    print("  ✓ Tampering threshold: 65+ (strict)")
    print("  ✓ Tested on your phone (variance: 572,908)")
    print("=" * 60)
    
    # Determine port dynamically
    port = int(os.environ.get('PORT', 5000))
    print(f"Listening on http://localhost:{port}")
    print("=" * 60)
    
    # Run with debug=False for production environments
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)