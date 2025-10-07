"""
Flask web application for legal document analyzer.
"""

import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from legal_analyzer import LegalDocumentAnalyzer

app = Flask(__name__)
app.secret_key = 'legal-doc-analyzer-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize analyzer
analyzer = LegalDocumentAnalyzer()


def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['pdf', 'docx', 'txt']


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Unsupported file format. Supported formats: PDF, DOCX, TXT'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Analyze document
            results = analyzer.analyze_document(file_path)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return jsonify(results)
            
        except ValueError as e:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'success': False, 'error': str(e)}), 400
            
        except Exception as e:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'success': False, 'error': f'Error analyzing document: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/search', methods=['POST'])
def search():
    """Handle keyword search in uploaded document."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check if keywords were provided
        keywords_str = request.form.get('keywords', '')
        if not keywords_str:
            return jsonify({'success': False, 'error': 'No keywords provided'}), 400
        
        keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
        
        if not keywords:
            return jsonify({'success': False, 'error': 'No valid keywords provided'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Unsupported file format. Supported formats: PDF, DOCX, TXT'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Search document
            results = analyzer.search_document(file_path, keywords)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return jsonify(results)
            
        except Exception as e:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'success': False, 'error': f'Error searching document: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'supported_formats': analyzer.get_supported_formats()})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
