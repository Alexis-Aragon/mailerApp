from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app
)
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search') # obtenemos los parametros de la url
    db, c = get_db()
    if search is None:
        c.execute("SELECT * FROM email")
    else: # implementación de la barra de búsqueda
        c.execute("SELECT * FROM email WHERE content LIKE %s", ('%' + search + '%',))
    mails = c.fetchall()
   
    return render_template('mails/index.html', mails=mails)

@bp.route('/create', methods= ['GET', 'POST'])
def create():
    if request.method == 'POST':
        email =  request.form.get('email')
        subject =  request.form.get('subject')
        content =  request.form.get('content')
        errors = []

        if not email:
            errors.append('Email es obligatorio')
        if not subject:
            errors.append('Asunto es obligatorio')
        if not content:
            errors.append('Contenido es obligatorio')
        
        if len(errors) == 0:
            send(email, subject, content)
            db, c = get_db()
            c.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (email, subject, content,))
            db.commit()
            
            return redirect(url_for('mail.index'))
        else:
            for error in errors:
                flash(error)
    return render_template('mails/create.html')

def send(to, subject, content):
    sg = sib_api_v3_sdk.Configuration()
    sg.api_key['api-key'] = current_app.config['SENDINBLUE_KEY']
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(sg))
    from_email = current_app.config['FROM_EMAIL']
    sender = {"name":"Alexis Aragon","email":from_email}
    replyTo = {"name":"Alexis Aragon","email":from_email}
    to = [{"email":to}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=replyTo, text_content=content, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
