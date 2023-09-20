import smtplib
from email.mime.text import MIMEText
from geopy.distance import geodesic
import json
# Email configuration
sender_email = 'adilforms@gmail.com'
sender_password = 'asd asdfasd asd fas dvafsd v'
recipient_phone = '7703137797'  # Replace with the recipient's phone number
recipient_carrier_domain = 'vtext.com'  # Replace with the recipient's carrier's email domain

# Define the target location (latitude and longitude)
target_location = (37.7749, -122.4194)  # Change to your desired coordinates

def send_alert_email(subject, message):
    # Create a connection to the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Log in to your Gmail account
    server.login(sender_email, sender_password)

    # Create an email message
    msg = MIMEText(message)
    msg['From'] = sender_email
    msg['To'] = f"{recipient_phone}@{recipient_carrier_domain}"
    msg['Subject'] = subject

    # Send the email
    server.sendmail(sender_email, f"{recipient_phone}@{recipient_carrier_domain}", msg.as_string())

    # Close the connection
    server.quit()

def read_target_location():
    try:
        with open('vehicllocation.json', 'r') as file:
            data = json.load(file)
            return data["latitude"], data["longitude"]
    except FileNotFoundError:
        print("vehicllocation.json file not found.")
        return None

def main():
    target_location = read_target_location()

    if target_location:
        # Simulate the car's location (latitude and longitude)
        car_location = (37.7750, -122.4193)  # Replace with actual car GPS data

        # Check if the car is within a specified radius (in meters)
        radius = 100  # Adjust this as needed
        distance = geodesic(target_location, car_location).meters

        if distance <= radius:
            alert_subject = "Car has entered the target location"
            alert_message = "The car has entered the target location."
            send_alert_email(alert_subject, alert_message)

if __name__ == "__main__":
    main()
