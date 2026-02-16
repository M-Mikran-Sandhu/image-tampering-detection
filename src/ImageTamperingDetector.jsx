import React, { useState } from 'react';
import { Upload, Image as ImageIcon, AlertCircle, CheckCircle, Info, X } from 'lucide-react';

export default function ImageTamperingDetector() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    setError(null); // Clear previous errors

    if (file) {
      // Validate file type
      const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
      if (!validTypes.includes(file.type)) {
        setError('Invalid file type. Please upload a JPG, PNG, or WebP image.');
        setSelectedImage(null);
        setPreviewUrl(null);
        return;
      }

      // Validate file size (10MB)
      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        setError('File is too large. Maximum size is 10MB.');
        setSelectedImage(null);
        setPreviewUrl(null);
        return;
      }

      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResults(null);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setResults(data);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure the Python backend is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResults(null);
    setError(null);
  };

  const getAssessmentColor = (assessment) => {
    if (assessment === 'Likely Authentic') return 'text-green-600 bg-green-50 border-green-200';
    if (assessment === 'Possibly Tampered') return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getAssessmentIcon = (assessment) => {
    if (assessment === 'Likely Authentic') return <CheckCircle className="w-6 h-6" />;
    return <AlertCircle className="w-6 h-6" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            Image Tampering Detector
          </h1>
          <p className="text-lg text-gray-600">
            Upload an image to analyze for potential digital manipulation
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
              <Upload className="w-6 h-6 mr-2" />
              Upload Image
            </h2>

            {!previewUrl ? (
              <label className="flex flex-col items-center justify-center w-full h-96 border-4 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-indigo-500 hover:bg-indigo-50 transition-all">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <ImageIcon className="w-16 h-16 text-gray-400 mb-4" />
                  <p className="mb-2 text-lg font-semibold text-gray-600">
                    Click to upload
                  </p>
                  <p className="text-sm text-gray-500">PNG, JPG, JPEG</p>
                </div>
                <input
                  type="file"
                  className="hidden"
                  accept="image/*"
                  onChange={handleImageSelect}
                />
              </label>
            ) : (
              <div className="space-y-4">
                <div className="relative">
                  <img
                    src={previewUrl}
                    alt="Selected"
                    className="w-full h-96 object-contain bg-gray-100 rounded-xl"
                  />
                  <button
                    onClick={reset}
                    className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <button
                  onClick={analyzeImage}
                  disabled={loading}
                  className="w-full bg-indigo-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                      Analyzing...
                    </>
                  ) : (
                    'Analyze Image'
                  )}
                </button>
              </div>
            )}

            {error && (
              <div className="mt-6 bg-red-50 border border-red-200 rounded-xl p-4 flex items-start">
                <AlertCircle className="w-5 h-5 text-red-600 mr-3 mt-0.5 flex-shrink-0" />
                <p className="text-red-800">{error}</p>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
              <Info className="w-6 h-6 mr-2" />
              Analysis Results
            </h2>

            {!results ? (
              <div className="flex items-center justify-center h-96 text-gray-400">
                <div className="text-center">
                  <ImageIcon className="w-24 h-24 mx-auto mb-4 opacity-50" />
                  <p className="text-lg">Upload and analyze an image to see results</p>
                </div>
              </div>
            ) : (
              <div className="space-y-6 overflow-y-auto max-h-[600px]">
                {/* Assessment */}
                <div className={`border-2 rounded-xl p-6 ${getAssessmentColor(results.tampering_analysis.assessment)}`}>
                  <div className="flex items-center mb-3">
                    {getAssessmentIcon(results.tampering_analysis.assessment)}
                    <h3 className="text-2xl font-bold ml-3">
                      {results.tampering_analysis.assessment}
                    </h3>
                  </div>
                  <p className="text-lg font-semibold">
                    Confidence: {results.tampering_analysis.confidence}
                  </p>
                  <p className="text-sm mt-2 opacity-80">
                    Tampering Score: {results.tampering_analysis.score}/100
                  </p>
                </div>

                {/* Reasons */}
                <div className="bg-gray-50 rounded-xl p-6">
                  <h4 className="font-semibold text-lg mb-3 text-gray-800">Analysis Findings</h4>
                  <ul className="space-y-2">
                    {results.tampering_analysis.reasons.map((reason, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-indigo-600 mr-2">•</span>
                        <span className="text-gray-700">{reason}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* ELA Image */}
                <div className="border border-gray-200 rounded-xl p-6">
                  <h4 className="font-semibold text-lg mb-3 text-gray-800">
                    Error Level Analysis (ELA)
                  </h4>
                  <img
                    src={results.ela_image}
                    alt="ELA Result"
                    className="w-full rounded-lg bg-gray-100"
                  />
                  <p className="text-sm text-gray-600 mt-3">
                    Bright areas indicate potential tampering or recent edits
                  </p>
                </div>

                {/* Image Metadata */}
                {Object.keys(results.metadata).length > 0 && (
                  <div className="border border-gray-200 rounded-xl p-6">
                    <h4 className="font-semibold text-lg mb-3 text-gray-800">Metadata</h4>
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                      {Object.entries(results.metadata).slice(0, 10).map(([key, value]) => (
                        <div key={key} className="text-sm">
                          <span className="font-medium text-gray-700">{key}:</span>
                          <span className="text-gray-600 ml-2 break-all">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Quality Metrics */}
                <div className="border border-gray-200 rounded-xl p-6">
                  <h4 className="font-semibold text-lg mb-3 text-gray-800">Image Properties</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">Dimensions:</span>
                      <p className="text-gray-600">{results.quality_metrics.dimensions}</p>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Format:</span>
                      <p className="text-gray-600">{results.quality_metrics.format}</p>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Mode:</span>
                      <p className="text-gray-600">{results.quality_metrics.mode}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-12 bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-gray-700">
            <div>
              <h4 className="font-semibold text-lg mb-2 text-indigo-600">Error Level Analysis</h4>
              <p className="text-sm">
                Detects inconsistencies in compression levels across the image. Tampered areas often show different error levels.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-lg mb-2 text-indigo-600">Metadata Inspection</h4>
              <p className="text-sm">
                Examines EXIF data for signs of editing software or missing information typical of manipulated images.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-lg mb-2 text-indigo-600">Quality Analysis</h4>
              <p className="text-sm">
                Analyzes image properties and statistical patterns that may indicate digital tampering.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
