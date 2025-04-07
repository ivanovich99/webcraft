from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from video.stream import video_bp
from email_module.email_routes import email_bp  # Import the email blueprint
from extensions import mail  # Import the `mail` instance
import os
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.secret_key = config.SECRET_KEY  # Use the secret key from config.py

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Your email
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Your email password

# Initialize the `mail` instance with the app
mail.init_app(app)

# Register blueprints
app.register_blueprint(video_bp)
app.register_blueprint(email_bp)  # Register the email blueprint


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            return redirect(url_for('files'))
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print(">>> Starting WebCraft...")
    app.run(host='0.0.0.0', port=5050, debug=True)
