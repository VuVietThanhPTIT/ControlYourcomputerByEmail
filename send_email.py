import smtplib
from io import BytesIO
from email.message import EmailMessage
from config import *

class Send:
    def __init__(self, subject = "cmd" , sender = email_sender  ):
        self.subject = subject 
        self.sender = sender

    def send(self , subject , message  ):
        self.subject = subject 
        self.message = message 
        text = f"Subject:{subject }\n\n{message}"
        # use \n\n to split header and body part 
        server = smtplib.SMTP("smtp.gmail.com", 587, local_hostname="localhost")
        server.starttls()
        # turn on security 
        server.login( email_sender , key  )
        server.sendmail(email_sender , email_receiver ,text)

    def send_image(self, subject, image, filename="screenshot.png", body="Screenshot attached"):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = email_sender
        msg["To"] = email_receiver
        msg.set_content(body)

        img_buffer = BytesIO()
        image.save(img_buffer, format="PNG")
        msg.add_attachment(
            img_buffer.getvalue(),
            maintype="image",
            subtype="png",
            filename=filename,
        )

        with smtplib.SMTP("smtp.gmail.com", 587, local_hostname="localhost") as server:
            server.starttls()
            server.login(email_sender, key)
            server.send_message(msg)
        



