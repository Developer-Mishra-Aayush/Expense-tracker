from django.shortcuts import render,redirect
from .models import UserProfile
from django.contrib.auth import authenticate
from django.contrib import messages
import random
from django.core.mail import send_mail
import logging
from django.views.decorators.cache import never_cache
from django.db import IntegrityError

# Create your views here.
def register(request):
    if request.method =='POST':
        print(request.method)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            UserProfile.objects.create(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "A user with this email already exists.")
            return render(request, 'accounts/signup.html')
        
    return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f" and {email} and {password}")
        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            messages.error(request, "User with this email is not registered.")
            return redirect('login')  # or wherever you want to redirect
        if not email or email!=user.email:
            messages.info("Email is not registered")
            return render(request,'accounts/signup.html')
        # Now Check the Authentication
        # if username!=user.username:
        #     messages.info("Username is incorrect")
        #     return redirect('/')
        if password!=user.password:
            messages.info(request,'Passowrd is incorrect')
            return redirect('/login')
        otp = generate_otp()
        request.session['otp'] = otp
        request.session['email'] = email
        send_mail(
            subject='🔑 Your OTP for Expense Tracker',
            message=f"""
                Hello {email},

                Welcome to Expense Tracker! Your One-Time Password (OTP) is:

                        {otp}

                Please enter this OTP on the verification page to complete your login.

                If you did not request this, please ignore this email.

                Thanks,
                The Expense Tracker Team
                """,
            from_email='aayush.mishra@drcsystems.com',
            recipient_list=[email],
            fail_silently=False
        )

        return render(request,'accounts/verification.html')
    print("Get is called")
    return render(request,'accounts/login.html')

def otp_verification(request):
    if request.method == 'GET':
        return redirect('login')
    if request.method=='POST':
        entered_otp = ''.join([
            request.POST.get('otp1', ''),
            request.POST.get('otp2', ''),
            request.POST.get('otp3', ''),
            request.POST.get('otp4', ''),
        ])
        session_otp = str(request.session.get('otp'))
        email = request.session.get('email')

        if not session_otp or not email:
            messages.error(request,"Session expired. Please login again.")
            return redirect('login')
        
        if entered_otp==session_otp:
            messages.success(request, "OTP verified successfully!")
            user = UserProfile.objects.get(email=email)  # fetch user from DB
            request.session['user_id'] = str(user.uuid)
            print("Logged in user:", request.session['user_id'])
            return redirect('calculate:index')
        else:
            print("Wrong otp")
            messages.error(request, "Incorrect OTP. Try again.")
            return render(request,'accounts/verification.html')
    return redirect('login')


def generate_otp():
    return random.randint(1000, 9999)
