import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from geopy.distance import geodesic

# Email configuration
sender_email = 'adilforms@gmail.com'
sender_password = 'ogwq jyek krpt clkq'
recipient_email = '6268610264@att.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use 465 for SSL

# Define the target location (latitude and longitude)
target_location = (37.7749, -122.4194)  # Change to your desired coordinates

def send_email(subject, message):
    # Create a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    
    # Log in to your email account
    server.login(sender_email, sender_password)
    
    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Add the message body
    msg.attach(MIMEText(message, 'plain'))
    
    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())
    
    # Close the connection
    server.quit()

def main():
    # Simulate the car's location (latitude and longitude)
    car_location = (37.7750, -121.4193)  # Replace with actual car GPS data

    # Check if the car is within a specified radius (in meters)
    radius = 1000  # Adjust this as needed
    distance = geodesic(target_location, car_location).meters

    if distance <= radius:
        alert_subject = "Car has entered the target location"
        alert_message = "The car has entered the target location."
        send_email(alert_subject, alert_message)

if __name__ == "__main__":
    main()
