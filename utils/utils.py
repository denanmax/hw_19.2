import secrets
import string

from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from users.models import User


def generate_secret_key(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key


def confirm_user_email(request, user):
    secret_key = generate_secret_key(30)
    user.email_confirm_key = secret_key
    user.save()

    current_site = get_current_site(request)
    message = render_to_string('users/confirm_email_message.html', {
        'domain': current_site.domain,
        'key': secret_key,
    })
    send_mail(
        subject='Подтверждение почты',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )

def confirm_email(request):
    confirm_user_email(request, request.user)
    return redirect(reverse('users:profile'))


def activate_email(request, key):
    print(request.user.email_confirm_key, key, sep='\n')
    if request.user.email_confirm_key == key:
        request.user.email_is_confirmed = True
        request.user.email_confirm_key = None
        request.user.save()
    else:
        print('Ключ не актуален')
    return redirect('/')

def generate_password(request):
    new_password = generate_secret_key(12)
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        subject='Вы сменили пароль',
        message=f'Новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse_lazy('users:login'))


def password_reset(request):
    """Сгенерировать новый пароль для пользователя если пароль забыли"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_secret_key(12)
            user.set_password(new_password)
            user.save()
            login(request, user)


            send_mail(
                subject='Вы сменили пароль',
                message=f'Новый пароль {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email]
            )

            return redirect(reverse("users:login"))  # Перенаправление на страницу входа
        except User.DoesNotExist:
            return render(request, 'users/password_reset_form.html',
                          {'error_message': 'User not found'})
    return render(request, 'users/password_reset_form.html')