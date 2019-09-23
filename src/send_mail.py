import smtplib
from email.mime import multipart, text, application
from config.config import config
from static.phrases import phrases


def get_message(email, file, cfg):
    msg = multipart.MIMEMultipart()
    msg['Subject'] = phrases["subject"]
    msg['From'] = cfg["login"]
    msg['To'] = email

    body = text.MIMEText(phrases["text"])
    msg.attach(body)

    fp = open(file, 'rb')
    pdf = application.MIMEApplication(fp.read(), _subtype="pdf")
    fp.close()
    pdf.add_header('Content-Disposition', 'attachment', filename=file)
    msg.attach(pdf)

    return msg


def login_and_send(email, msg, cfg):
    s = smtplib.SMTP(cfg["host"], cfg["port"])
    s.starttls()
    s.login(cfg["login"], cfg["password"])
    s.sendmail(cfg["login"], [email], msg.as_string())
    s.quit()


def send_mail(email, files):
    cfg = config["email_config"]
    if not cfg["to_mail"]:
        return "E-mail not sent due to settings of config"
    msg = get_message(email, files[0], cfg)
    login_and_send(email, msg, cfg)

    return "E-mail sent successfully"


def send_to_chat(bot, peer, file):
    cfg = config["email_config"]
    if cfg["to_chat"]:
        bot.messaging.send_file(peer, file)
        return "File sent to chat"
    return "File not sent due to settings of config"
