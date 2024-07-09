from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from admin_material.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from store.models import DailyMetrics
from datetime import date
# Create your views here.

# Pages
def index(request):
  today = date.today()
  metrics = DailyMetrics.objects.filter(date=today).first()

  if not metrics:
    metrics = DailyMetrics.objects.create(
      money=0, users=0, new_clients=0, sales=0,
      website_views=0, daily_sales=0, completed_tasks=0
    )

  context = {
    'today_money': metrics.money,
    'today_users': metrics.users,
    'new_clients': metrics.new_clients,
    'sales': metrics.sales,
    'website_views': metrics.website_views,
    'daily_sales': metrics.daily_sales,
    'completed_tasks': metrics.completed_tasks
  }

  return render(request, 'pages/index.html', context)

def billing(request):
  return render(request, 'pages/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'pages/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def notification(request):
  return render(request, 'pages/notifications.html', { 'segment': 'notification' })

def profile(request):
  return render(request, 'pages/profile.html', { 'segment': 'profile' })


# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm