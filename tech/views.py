from django.shortcuts import render, redirect, HttpResponse
from .forms import ProductForm, ImageForm
from .models import Image, Product
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')


def index(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'index.html', context)


def detail(request, id):
    product = Product.objects.get(id=id)
    images = Image.objects.filter(product=product)
    context = {"product": product, "images": images}
    return render(request, 'detail.html', context)


def create_product(request):
    productform = ProductForm()
    imageform = ImageForm()

    if request.method == 'POST':

        files = request.FILES.getlist('images')

        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
            product = productform.save(commit=False)
            product.vendor = request.user
            product.save()
            messages.success(request, "Product created successfully")

            for file in files:
                Image.objects.create(product=product, images=file)

            return redirect("index")

    context = {"p_form": productform, "i_form": imageform}
    return render(request, "create.html", context)


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')