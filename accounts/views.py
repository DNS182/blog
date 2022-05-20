from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .forms import UserRegForm, UserEditForm , ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from . token import account_activation_token 
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.contrib import messages




# Create your views here.
def register(request):
    if request.method=='POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            current_site = get_current_site(request)  
            mail_subject = 'CLICK ON THE ACTIVATION LINK BELOW : '  
            message = render_to_string('account/active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send() 
            messages.info(request, 'NEED TO ACTIVATE TO USE THIS SERVICE.PLEASE CHECK EMAIL')
            return redirect("login")    
    else:
        form = UserRegForm()
    return render(request , 'account/reg.html' , {'form':form})


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request ,'account/acc_confirm.html')  
    else:  
        return render(request ,'account/acc_error.html') 

    

@login_required
def profile(request):
    return render(request , 'account/profile.html')

@login_required
def profile_edit(request):
    
    if request.method == 'POST':
        u_form = UserEditForm(request.POST , instance = request.user)
        p_form = ProfileForm(request.POST , request.FILES ,  instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('/account/profile')
    else:
        u_form = UserEditForm(instance = request.user)
        p_form = ProfileForm(instance = request.user.profile)


    return render(request , 'account/profileedit.html' , {'u_form':u_form , 'p_form' :p_form})


    