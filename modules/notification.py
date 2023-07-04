import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def mail(destinatario, ident):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) #this is for the google mail server, it could be different if you are using another one
    server.ehlo()
# load the email password:
    pathToPassword = 'json_keys/mail_password.json'
    with open(pathToPassword, 'r') as f:
        password = json.load(f)

    remitente = "your@email.com"
    subject = "transcripción completada"
    fecha = datetime.now().strftime("%Y-%m-%d") # year, month, day config
    hora = datetime.now().strftime("%H:%M") # hour, minutes config

# here you can add and html for the email:
    message = ''' 
    <html>
        <body>
            <h1>Transcripción completada</h1>
            <div>
                <span>id: {}</span>
                <span>Fecha: {}</span>
                <span>Finalizado a las: {}</span>
                <p>
                    la transcipcion habla de...    
                </p>
            </div>
        </body>
    </html>
    '''.format(ident, fecha, hora)

    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'html', _charset='utf-8'))

    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = subject

    with open(pathToPassword, 'r') as f:
        password = json.load(f)

    server.login(remitente, password['password']) # the login is required

    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()
    print("correo enviado exitosamente")
