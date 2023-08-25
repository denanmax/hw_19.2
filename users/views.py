from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

def confirm_user_email(request, user):
    user.save()

    current_site = get_current_site(request)
    message = render_to_string('users/confirm_email_message.html', {
        'domain': current_site.domain,
    })
    send_mail(
        subject='Подтверждение почты',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )
# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


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