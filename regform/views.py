from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from regform.forms import RegistrationForm
from regform.models import UserTable
from django.contrib.auth.views import login
from django.http.response import HttpResponse
# from django.csrf import csrf_exempt
#from regform.utils import email_to_username

#def login_page(request, _next="/home/"):
#    if not request.user.is_anonymous():
#        return redirect('/home/')
#    
#    if request.method == "POST":
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            login(request, form.get_user())
#            return redirect(_next)
#    else:
#        form = LoginForm()
        
#    return render(
#                  request,
#                  'registration/login.html',
#                  {'form': form, 'next': _next, 'title': "Please Login"}
#                  )
def login_page(request):
    if request.user.is_anonymous():
        return login(request)
    else:
        return redirect('/home/')
    

@csrf_exempt
def register(request):
    
    if not request.user.is_anonymous():
        return redirect('/home/')
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        title = "Update Profile"
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create(username=user_name)
                                      
            user.set_password(password)
            user.save()
            usertable = UserTable.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                mobile_no=form.cleaned_data['mobile_no'],
                alternate_mobile_no=form.cleaned_data['alternate_mobile_no'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                ethnicity=form.cleaned_data['ethnicity'],
                country=form.cleaned_data['country'],
                languages_known=form.cleaned_data['languages_known'],
                email=form.cleaned_data['email']
            )
            return redirect('/register/success/')
    else:
        title = "Create New Profile"
        form = RegistrationForm()  

    return render(
                  request,
                  'registration/register.html',
                  {'form': form, 'title': title}
                  )
    
@login_required
def edit(request):
    curr_user = request.user
    if request.method == 'POST':
        form = RegistrationForm(request.POST, user=curr_user)
        
        if form.is_valid():
            curr_user.usertable.first_name = form.cleaned_data['first_name']
            curr_user.usertable.middle_name = form.cleaned_data['middle_name']
            curr_user.usertable.last_name = form.cleaned_data['last_name']
            curr_user.usertable.mobile_no = form.cleaned_data['mobile_no']
            curr_user.usertable.alternate_mobile_no = form.cleaned_data['alternate_mobile_no']
            curr_user.usertable.date_of_birth = form.cleaned_data['date_of_birth']
            curr_user.usertable.gender = form.cleaned_data['gender']
            curr_user.usertable.ethnicity = form.cleaned_data['ethnicity']
            curr_user.usertable.country = form.cleaned_data['country']
            curr_user.usertable.languages_known = form.cleaned_data['languages_known']
            curr_user.usertable.save()
            
            return redirect('/register/success/')
    else:
        form = RegistrationForm(user=curr_user)
   
    return render(
                  request,
                  'registration/register.html',
                  {'form': form, 'title': 'Update Profile'}
                  )


def register_success(request):
    return render(
                  request, 
                  'registration/success.html',
                  )

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    curr_user = request.user
    return render(
                  request,
                  'registration/home.html',
                  {'user': curr_user }
                  )

