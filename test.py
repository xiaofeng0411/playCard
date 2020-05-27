import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(msg_text):
    msg = MIMEText(msg_text, _charset="utf-8")
    sender = "wxdlxs@126.com"
    sender_host = "smtp.126.com"
    password = "IBQDBEMGWHYWFQUB"
    revicer = ["824316775@qq.com"]
    msg["Subject"] = "打卡信息邮件"
    msg['From'] = Header("打卡脚本", "utf-8")
    msg["To"] = ','.join(revicer)
    smtp = smtplib.SMTP()
    smtp.connect(sender_host, 25)
    smtp.login(sender, password)
    smtp.sendmail(sender, revicer, msg.as_string())
    print("fasongchengsogng")


send_email("123")
