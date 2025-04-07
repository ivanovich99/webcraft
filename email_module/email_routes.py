import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from extensions import mail  # Import the `mail` instance

email_bp = Blueprint('email', __name__)

# Environment variables for email credentials
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
print(os.environ.get('EMAIL_USER'))

# Predefined recipient email
RECIPIENT_EMAIL = "ivanovich.chiu@cetys.edu.mx"

@email_bp.route('/email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not subject or not message:
            flash("Subject and message are required!", "error")
            return redirect(url_for('email.send_email'))

        try:
            # Create the email
            msg = Message(subject=subject,
                          sender=os.environ.get('EMAIL_USER'),
                          recipients=["ivanovich.chiu@cetys.edu.mx"])
            msg.body = message
            msg.html = f"<h1>{subject}</h1><p>{message}</p>"

            # Send the email
            mail.send(msg)
            flash("Email sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to send email: {e}", "error")

        return redirect(url_for('email.send_email'))

    return render_template('email.html')