from django.shortcuts import render, redirect
from .forms import ProfileForm
# Create your views here.
def dashboard(request):
    return render (request, 'dashboard.html')

def tables(request):
    return render(request, 'tables.html')

def profile(request):
    if request.method == 'POST':
        profile = ProfileForm(request.POST, request.FILES)
        if profile.is_valid():
            new_profile = profile.cleaned_data
            print(new_profile)
            #new_profile.save()  #Guarda en la bsae de datos 
        return redirect('profile')
    else:
        print('No esta mostrando los datos')
        
        
    return render(request, 'profile.html')

#--------------------------------------------------------------------------------
def sign_in(request):
    return render(request, 'sign-in.html')
def sign_up(request):
    return render(request, 'sign-up.html')
