from django.core.mail import send_mail


def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте активируйте свой аккаунт!',
        f'Чтобы активировать нужно перейти по ссылке: \n{full_link}',
        'bermetzarlyk@gmail.com',
        [user],
        fail_silently=False,
    )