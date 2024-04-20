import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
class Mail():
    def send_to_mail(self, email, message, image_path):
        my_email = "hmr778993@gmail.com"
        password = "xpmx vyvl aalh lthy" 

        msg = MIMEMultipart()
        msg['From'] = my_email
        msg['To'] = email
        msg['Subject'] = "Community Message"
        msg.attach(MIMEText(message, 'plain'))

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            image_mime = MIMEImage(image_data, name='image.jpg')
            msg.attach(image_mime)

        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_email, password=password)

        connection.send_message(msg)


        connection.quit()
    def send_to_all(self,message,data):
        my_email="hmr778993@gmail.com"
        password="xpmx vyvl aalh lthy"
        for user in data:
            connection=smtplib.SMTP("smtp.gmail.com",587)
            connection.starttls()
            connection.login(user=my_email,password=password)
            connection.sendmail(from_addr=my_email,to_addrs=user.Email,msg=f"Subject:Community Message\n\n{message}")
        connection.close()