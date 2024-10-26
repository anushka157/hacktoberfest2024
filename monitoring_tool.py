# Import necessary libraries
# Import psutil for system resource monitoring
import psutil
# Import smtplib for sending emails
import smtplib
# Import MIMEText for creating email content
from email.mime.text import MIMEText
# Import MIMEMultipart for handling email attachments
from email.mime.multipart import MIMEMultipart
# Import time for delay management
import time
# Import socket for network operations
import socket

# Define thresholds
# Set the CPU usage threshold
CPU_THRESHOLD = 80  # in percentage
# Set the memory usage threshold
MEMORY_THRESHOLD = 80  # in percentage
# Set the disk usage threshold
DISK_THRESHOLD = 80  # in percentage

# Email settings
# Set the email address to send alerts from
EMAIL_ADDRESS = 'your_email@example.com'
# Set the email password
EMAIL_PASSWORD = 'your_password'
# Set the recipient email address for alerts
ALERT_EMAIL = 'alert_recipient@example.com'
# Set the SMTP server for sending emails
SMTP_SERVER = 'smtp.gmail.com'  # Update to your SMTP server
# Set the SMTP server port
SMTP_PORT = 587

# Function to send an email alert
def send_alert(subject, body):
    # Create a multipart email message
    msg = MIMEMultipart()
    # Set the sender email address
    msg['From'] = EMAIL_ADDRESS
    # Set the recipient email address
    msg['To'] = ALERT_EMAIL
    # Set the email subject
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        # Start TLS for security
        server.starttls()
        # Log in to the SMTP server
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # Convert the message to a string
        text = msg.as_string()
        # Send the email
        server.sendmail(EMAIL_ADDRESS, ALERT_EMAIL, text)
        # Close the connection to the SMTP server
        server.quit()
        # Print success message
        print(f'Alert sent: {subject}')
    except Exception as e:
        # Print failure message
        print(f'Failed to send alert: {e}')

# Function to check CPU usage
def check_cpu_usage():
    # Get the current CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    # If CPU usage exceeds the threshold, send an alert
    if cpu_usage > CPU_THRESHOLD:
        send_alert('CPU Usage Alert', f'CPU usage is at {cpu_usage}%')
    # Return the current CPU usage
    return cpu_usage

# Function to check memory usage
def check_memory_usage():
    # Get memory usage information
    memory_info = psutil.virtual_memory()
    # Get the current memory usage percentage
    memory_usage = memory_info.percent
    # If memory usage exceeds the threshold, send an alert
    if memory_usage > MEMORY_THRESHOLD:
        send_alert('Memory Usage Alert', f'Memory usage is at {memory_usage}%')
    # Return the current memory usage
    return memory_usage

# Function to check disk usage
def check_disk_usage():
    # Get disk usage information
    disk_info = psutil.disk_usage('/')
    # Get the current disk usage percentage
    disk_usage = disk_info.percent
    # If disk usage exceeds the threshold, send an alert
    if disk_usage > DISK_THRESHOLD:
        send_alert('Disk Usage Alert', f'Disk usage is at {disk_usage}%')
    # Return the current disk usage
    return disk_usage

# Function to test DNS resolution
def test_dns_resolution(server):
    try:
        # Attempt to resolve the DNS for the given server
        socket.gethostbyname(server)
        # Print success message if DNS resolution is successful
        print(f'DNS resolution for {server} succeeded.')
    except socket.error as err:
        # Print failure message if DNS resolution fails
        print(f'DNS resolution for {server} failed: {err}')

# Main function to monitor system resources
def monitor_system(interval=60):
    # Test DNS resolution before starting the monitoring loop
    test_dns_resolution(SMTP_SERVER)
    
    # Continuously monitor system resources
    while True:
        # Check and log CPU usage
        cpu_usage = check_cpu_usage()
        # Check and log memory usage
        memory_usage = check_memory_usage()
        # Check and log disk usage
        disk_usage = check_disk_usage()
        
        # Print current usage statistics
        print(f'CPU usage: {cpu_usage}%, Memory usage: {memory_usage}%, Disk usage: {disk_usage}%')
        
        # Wait for the specified interval before checking again
        time.sleep(interval)

# Run the monitoring tool
if __name__ == '__main__':
    # Start monitoring system resources
    monitor_system()
