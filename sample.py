from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os

# Initialize Flask app
app = Flask(__name__)

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder where files will be stored temporarily
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'jpg', 'png', 'jpeg'}  # Allowed file extensions
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size (16MB)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return redirect(url_for('upload_file'))

# Route for uploading files
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        # If no file is selected
        if file.filename == '':
            return redirect(request.url)
        
        # If file is allowed, save it
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')  # Render upload.html

# Route for displaying uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the file from the 'uploads' folder
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route for downloading the file
@app.route('/download/<filename>')
def download_file(filename):
    # Send the file for download
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Route to list all uploaded files
@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])  # List all files in the upload folder
    return render_template('files.html', files=files)

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
