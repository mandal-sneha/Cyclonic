# main.py
import os
from flask import Flask, render_template, request, send_from_directory, url_for, jsonify
from werkzeug.utils import secure_filename
from map_generator import generate_map
from cyclone_analysis import analyze_cyclone_file
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('trajectories', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/path_predictor')
def path_predictor():
    return render_template('PathPredictor.html')

@app.route('/generate_map')
def generate_cyclone_map():
    try:
        # Get and validate parameters
        try:
            latitude = float(request.args.get('latitude', 0))
            longitude = float(request.args.get('longitude', 0))
            speed = float(request.args.get('speed', 0))
            direction = float(request.args.get('direction', 0))
        except ValueError as e:
            logger.error(f"Parameter validation error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Invalid parameters provided'
            }), 400

        logger.info(f"Received parameters: lat={latitude}, lon={longitude}, speed={speed}, dir={direction}")

        # Delete existing file if it exists
        trajectory_file = os.path.join('trajectories', 'cyclone_trajectory.png')
        if os.path.exists(trajectory_file):
            try:
                os.remove(trajectory_file)
            except OSError as e:
                logger.warning(f"Error removing existing file: {str(e)}")

        # Generate map with error handling
        try:
            generate_map(latitude, longitude, speed, direction)
        except Exception as e:
            logger.error(f"Map generation error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Error generating map'
            }), 500

        # Verify file exists
        if not os.path.exists(trajectory_file):
            logger.error("Generated file not found")
            return jsonify({
                'success': False,
                'error': 'Generated file not found'
            }), 500

        return jsonify({
            'success': True,
            'image_url': url_for('get_trajectory_image', filename='cyclone_trajectory.png')
        })

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/trajectories/<filename>')
def get_trajectory_image(filename):
    if not os.path.exists(os.path.join('trajectories', filename)):
        logger.error(f"File not found: {filename}")
        return "File not found", 404
    return send_from_directory('trajectories', filename)

@app.route('/intensity_predictor')
def intensity_predictor():
    return render_template('IntensityPredictor.html')

@app.route('/ml_model')
def ml_model():
    return render_template('IntensityPredictor.html')

@app.route('/historical_cyclones')
def historical_cyclones():
    return render_template('HistoricalCyclones.html')

@app.route('/news')
def news():
    return render_template('News.html')

@app.route('/analyze_cyclone', methods=['POST'])
def analyze_cyclone():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            analysis_results = analyze_cyclone_file(file_path)
            return jsonify({
                "image_url": url_for('uploaded_file', filename=filename),
                "analysis": analysis_results
            })
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return jsonify({"error": "Error analyzing file"}), 500
    
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Set environment variable to handle OpenMP error
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    app.run(debug=True, threaded=True)