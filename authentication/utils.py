from django.core.mail import EmailMessage
from django.utils.translation import gettext as _


def send_sms_code(email, code):
    message = EmailMessage(
        to=[email],
        subject=_('Код для регистрации на сайте LAVKA.QUES.KG'),
        body=_(f'Ваш код для регистрации {code}.\nНикому не говорите ваш код'),
        from_email='sino0on@sino0on.ru'
    )

    message.send()
    return True


def send_sms_code_for_reset(email, code):
    message = EmailMessage(
        to=[email],
        subject=_('Код для сброса на сайте LAVKA.QUES.KG'),
        body=_(f'Ваш код для сброса {code}.\nНикому не говорите ваш код'),
        from_email='sino0on@sino0on.ru'
    )

    message.send()
    return True