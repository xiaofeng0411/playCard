import smtplib
from email.mime.text import MIMEText
import setting


def send_email(host, username, passwd, send_to, subject, content):
    msg = MIMEText(content)
    my_email = username + "<" + username + ">"
    msg['From'] = my_email
    msg['Subject'] = subject
    msg['To'] = ",".join(send_to)
    try:
        server = smtplib.SMTP_SSL(host, 465)
        server.ehlo()
        server.login(username, passwd)
        server.sendmail(username, send_to, msg.as_string())
        server.close()
        print('sucessfully')
    except Exception as e:
        print('Exception: send email failed',e)

if __name__ == '__main__':
    host = "smtp.126.com"
    username = "wxdlxs@126.com"
    passwd = "IBQDBEMGWHYWFQUB"
    to_list = [setting.receive]
    subject = "123"
    content = "23223423"
    send_email(host, username, passwd, to_list, subject, content)
