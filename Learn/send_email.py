import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = 'smtp.qq.com'
mail_user = '739843128@qq.com'
mail_password = 'lzsvrljywmegbbeh'

sender = '739843128@qq.com'
receiver = ['739843128@qq.com']

message = MIMEText("用python发送邮件，tonyma",'plain','utf-8')
message['From'] = Header("daddy",'utf-8')
message['To'] = Header("son",'utf-8')
message['Subject'] = Header("TONY MOM" , 'utf-8')

smtpObj = smtplib.SMTP()
smtpObj.connect( mail_host , 25 )
smtpObj.starttls()
smtpObj.login( mail_user , mail_password )
smtpObj.sendmail(sender,receiver,message.as_string())
print('发送成功')
smtpObj.quit()

