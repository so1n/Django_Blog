from random import Random


from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from django_project.settings import EMAIL_FROM
from django_project.celery import app


@app.task
def send_register_email(email, send_type="register", num=16):
    """
    发送注册邮件时的链接
    :param email: email
    :param send_type: 'register'or'forget'
    :return: 
    """
    email_record = EmailVerifyRecord()
    code_str = random_str(num)
    email_record.code = code_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code_str)

        send_mail(email_title, email_body, EMAIL_FROM, [email])

    elif send_type == 'forget':
        email_title = "重置密码链接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code_str)

        send_mail(email_title, email_body, EMAIL_FROM, [email])

    elif send_type == 'update_email':
        email_title = "邮箱修改验证码"
        email_body = "验证码为：{0}".format(code_str)

        send_mail(email_title, email_body, EMAIL_FROM, [email])

    else:
        pass


def random_str(random_length=8):
    """
    随机字符串生成
    :param random_length: 生成字符串长度(init)
    :return: 返回字符串(str)
    """
    code_str = ''
    generate_random_str = [chr(i) for i in range(65, 91)] + \
                          [chr(i) for i in range(97, 123)] + \
                          [str(i) for i in range(10)]
    chars = ''.join(generate_random_str)
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        code_str += chars[random.randint(0, length)]
    return code_str

