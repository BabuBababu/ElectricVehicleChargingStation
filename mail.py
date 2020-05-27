import smtplib
from email.mime.text import MIMEText




s = smtplib.SMTP('smtp.gmail.com', 587)

s.starttls()

s.login('poryou66@gmail.com', 'ftpzebchlgswtqzh')

msg = MIMEText('내용 : 본문내용 테스트입니다!!! 확인해보자!')

msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'

s.sendmail("poryou66@gmail.com", "whalstn77@naver.com", msg.as_string())


s.quit()