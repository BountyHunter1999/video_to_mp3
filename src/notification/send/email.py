import smtplib
import os
import json

from email.message import EmailMessage

def notification(message):
    try:
        message = json.loads(message)
        # apply this setting
        # authorize non gmail or non google application
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        # user associated with the jwt
        receiver_address = message["username"]
        
        msg = EmailMessage()
        # receiver of this email can take this id and download from
        # the download endpoint
        msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
        msg["Subject"] = "MP3 Download"
        msg["FROM"] = sender_address
        msg["To"] = receiver_address
        
        # connect to google's SMTP server
        session = smtplib.SMTP("smtp.gmail.com")
        
        # put the connection to the SMTP server into TLS mode
        # TLS: Transport Layer Security which makes sure our
        # communication betn the SMTP server is encrypted
        # we do this to secure our packets in transit
        session.starttls()
        
        # and login into our gmail account
        session.login(sender_address, sender_password)
        
        # and then send the email
        session.send_message(msg, sender_address, receiver_address)
        
        # close the session
        session.quit()
        
        print("Mail Sent")
    except Exception as err:
        print(err)
        return err