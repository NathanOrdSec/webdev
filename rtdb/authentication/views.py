from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import login, authenticate, logout
# Create your views here.
def register(request):
  template = loader.get_template('registration/register.html')
  if request.method=="GET":
    rForm=RegisterForm()
    context={
      'register': rForm,
    }
    return HttpResponse(template.render(context,request))
  if request.method == 'POST':
        rForm = RegisterForm(request.POST) 
        if rForm.is_valid():
            user = rForm.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/register.html', {'register': rForm})
