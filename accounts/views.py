from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
# imported to show alerts error and messages 
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)

        # cleaned_data--> in django used to fetch value from 'post-request'

        if form.is_valid():

            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            # fetching user data from account model and giving it to user
            user = Account.objects.create_user(first_name=first_name, last_name=last_name ,username=username, email=email, password=password)
            # we give user-> field this way  as accounts model don't have phone number field
            user.phone_number = phone_number
            user.save()
            # after we click on register button will show below message (django alerts)
            messages.success(request,'Registration Successful.')
            return redirect('register')

    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
        }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            # messages.success(request, 'you are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out.')
    return redirect('login')










