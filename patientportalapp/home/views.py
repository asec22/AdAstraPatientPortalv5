from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

# Create your views here.

def home(request):
    return render(request,"main/home.html",{})

def about(request):
    return render(request,"main/about.html",{})

def services(request):
    return render(request,"main/services.html",{})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email to you
            send_mail(
                'New Contact Form Submission',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                'howard@med-staffing.org',  # Your email
                ['howard@med-staffing.org'],  # Your email
                fail_silently=False
            )

            # Redirect to success page or handle success differently
            return render(request,'contact/success.html')  # Assuming you have a success view

    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})