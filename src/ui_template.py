"""
HTML template for Cancer Detection API UI
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cancer Detection API</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 900px;
            width: 100%;
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
            margin-bottom: 5px;
        }

        .accuracy-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
        }

        .content {
            padding: 40px 30px;
        }

        .section {
            margin-bottom: 40px;
        }

        .section-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-title::before {
            content: '';
            width: 4px;
            height: 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .feature-input {
            display: flex;
            flex-direction: column;
        }

        .feature-input label {
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
            font-weight: 500;
        }

        .feature-input input {
            padding: 10px 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 0.95em;
            transition: border-color 0.3s;
        }

        .feature-input input:focus {
            outline: none;
            border-color: #667eea;
            background: #f9f9ff;
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        button {
            flex: 1;
            padding: 12px 20px;
            font-size: 1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }

        .btn-predict {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-predict:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }

        .btn-predict:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .btn-clear {
            background: #f0f0f0;
            color: #333;
        }

        .btn-clear:hover {
            background: #e0e0e0;
        }

        .btn-sample {
            background: #4CAF50;
            color: white;
        }

        .btn-sample:hover {
            background: #45a049;
        }

        .result {
            background: #f9f9ff;
            padding: 25px;
            border-radius: 12px;
            margin-top: 30px;
            display: none;
            border-left: 5px solid #667eea;
        }

        .result.show {
            display: block;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .result-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
        }

        .prediction-box {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        .prediction-item {
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        .prediction-benign {
            background: #E8F5E9;
            border: 2px solid #4CAF50;
        }

        .prediction-malignant {
            background: #FFEBEE;
            border: 2px solid #f44336;
        }

        .prediction-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .prediction-value {
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .benign-label { color: #2E7D32; }
        .malignant-label { color: #C62828; }

        .confidence-bar {
            background: #e0e0e0;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin: 15px 0;
        }

        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.5s ease-out;
        }

        .confidence-text {
            font-size: 0.85em;
            color: #666;
            text-align: center;
        }

        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
            animation: slideIn 0.3s ease-out;
        }

        .alert.show {
            display: block;
        }

        .alert-error {
            background: #FFEBEE;
            color: #C62828;
            border-left: 4px solid #f44336;
        }

        .alert-success {
            background: #E8F5E9;
            color: #2E7D32;
            border-left: 4px solid #4CAF50;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .info-box {
            background: #f0f7ff;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2196F3;
            font-size: 0.9em;
            color: #555;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 0.85em;
            border-top: 1px solid #f0f0f0;
            background: #fafafa;
        }

        @media (max-width: 600px) {
            .header h1 {
                font-size: 1.8em;
            }

            .features-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .prediction-box {
                grid-template-columns: 1fr;
            }

            .button-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔬 Cancer Detection API</h1>
            <p>AI-Powered Breast Cancer Analysis</p>
            <div class="accuracy-badge">📊 98.77% Accuracy | ROC AUC: 0.9954</div>
        </div>

        <div class="content">
            <div class="info-box">
                📋 Enter 30 medical features below to get a prediction. Use the sample data to test or load your own values.
            </div>

            <div class="alert alert-error" id="errorAlert"></div>
            <div class="alert alert-success" id="successAlert"></div>

            <form id="predictionForm">
                <div class="section">
                    <div class="section-title">Input Features</div>
                    <div class="features-grid" id="featuresContainer"></div>
                </div>

                <div class="button-group">
                    <button type="button" class="btn-sample" onclick="loadSampleData()">📊 Load Sample Data</button>
                    <button type="button" class="btn-clear" onclick="clearForm()">🔄 Clear All</button>
                    <button type="submit" class="btn-predict">🚀 Get Prediction</button>
                </div>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyzing features...</p>
            </div>

            <div class="result" id="result">
                <div class="result-title">📈 Prediction Result</div>
                <div class="prediction-box" id="predictionBox"></div>
                <div class="confidence-bar">
                    <div class="confidence-fill" id="confidenceFill"></div>
                </div>
                <div class="confidence-text" id="confidenceText"></div>
            </div>
        </div>

        <div class="footer">
            🏥 Developed for healthcare decision support | Not for clinical diagnosis
        </div>
    </div>

    <script>
        const FEATURE_COUNT = 30;
        const FEATURE_NAMES = [
            "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
            "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
            "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
            "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
            "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
            "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
        ];

        // Sample benign data
        const SAMPLE_DATA = [13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766, 0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023, 15.11, 19.26, 102.7, 704.4, 0.1073, 0.2070, 0.2566, 0.1083, 0.1637, 0.08206];

        // Initialize form
        function initializeForm() {
            const container = document.getElementById('featuresContainer');
            for (let i = 0; i < FEATURE_COUNT; i++) {
                const input = document.createElement('div');
                input.className = 'feature-input';
                input.innerHTML = `
                    <label for="feature${i}">${i + 1}. ${FEATURE_NAMES[i]}</label>
                    <input type="number" id="feature${i}" placeholder="0.0" step="0.01" required>
                `;
                container.appendChild(input);
            }
        }

        function loadSampleData() {
            for (let i = 0; i < FEATURE_COUNT; i++) {
                document.getElementById(`feature${i}`).value = SAMPLE_DATA[i].toFixed(4);
            }
            showAlert('Sample data loaded!', 'success');
        }

        function clearForm() {
            document.getElementById('predictionForm').reset();
            document.getElementById('result').classList.remove('show');
            hideAlerts();
        }

        function showAlert(message, type) {
            hideAlerts();
            const alert = document.getElementById(`${type}Alert`);
            alert.textContent = message;
            alert.classList.add('show');
            setTimeout(() => alert.classList.remove('show'), 5000);
        }

        function hideAlerts() {
            document.getElementById('errorAlert').classList.remove('show');
            document.getElementById('successAlert').classList.remove('show');
        }

        function getFormData() {
            const features = [];
            for (let i = 0; i < FEATURE_COUNT; i++) {
                const value = document.getElementById(`feature${i}`).value;
                if (!value) {
                    throw new Error(`Feature ${i + 1} (${FEATURE_NAMES[i]}) is required`);
                }
                features.push(parseFloat(value));
            }
            return features;
        }

        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlerts();

            try {
                const features = getFormData();
                const loading = document.getElementById('loading');
                loading.classList.add('show');

                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ features })
                });

                loading.classList.remove('show');

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Prediction failed');
                }

                const result = await response.json();
                displayResult(result);

            } catch (error) {
                document.getElementById('loading').classList.remove('show');
                showAlert('❌ ' + error.message, 'error');
            }
        });

        function displayResult(result) {
            const prediction = result.prediction;
            const confidence = result.probability || result.confidence || 0.5;

            const predictionBox = document.getElementById('predictionBox');
            const isPredicted = prediction === 1;
            const diagnosisLabel = isPredicted ? 'Malignant' : 'Benign';
            const classname = isPredicted ? 'prediction-malignant' : 'prediction-benign';
            const labelClass = isPredicted ? 'malignant-label' : 'benign-label';

            predictionBox.innerHTML = `
                <div class="prediction-item ${classname}">
                    <div class="prediction-label">Prediction</div>
                    <div class="prediction-value ${labelClass}">${diagnosisLabel}</div>
                </div>
                <div class="prediction-item ${classname}">
                    <div class="prediction-label">Confidence</div>
                    <div class="prediction-value" style="color: inherit;">${(confidence * 100).toFixed(1)}%</div>
                </div>
            `;

            const confidenceFill = document.getElementById('confidenceFill');
            confidenceFill.style.width = '0%';
            setTimeout(() => {
                confidenceFill.style.width = (confidence * 100) + '%';
            }, 100);

            document.getElementById('confidenceText').textContent = 
                `Model confidence: ${(confidence * 100).toFixed(2)}% | Status: ${isPredicted ? '⚠️ Potential Malignancy' : '✅ Likely Benign'}`;

            document.getElementById('result').classList.add('show');
            showAlert(`Prediction complete: ${diagnosisLabel} (${(confidence * 100).toFixed(1)}% confidence)`, 'success');
        }

        // Initialize on page load
        window.addEventListener('load', initializeForm);
    </script>
</body>
</html>
"""
