from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Company, Product, Invoice, Settings
from .forms import CompanyForm, ProductForm, InvoiceForm, SettingsForm, CompanySelectForm
from random import randint
from uuid import uuid4

# Create your views here.
def main(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('main')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username    
            return redirect('home')
        else:
            messages.error(request, "Invalid Password")
            return redirect('main')

    # Render the login page template (GET request)
    return render(request, 'main.html')

def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        if User.objects.filter(username=username).exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('register')

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Account created successfully!")
        return redirect('main')

    # Render the registration page template (GET request)
    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    request.session.flush() 
    return redirect('main')

def sess_login(request):
    if 'username' in request.session:
        return render(request, 'home.html', {'username': request.session['username']})
    else:
        return redirect('main')

def change_pass(request):
    if request.method == "POST":
        username = request.POST.get('username')
        print(f"Received username: {username}")  # Debug print

        try:
            user = User.objects.get(username=username)
            request.session['username'] = username
            print(f"User found: {user}")  # Debug print
            return redirect('postPass')
        except User.DoesNotExist:
            messages.error(request, 'Invalid Username')
            print("User does not exist")  # Debug print
            return redirect('changePass')
    
    return render(request, 'changePass.html')



def postchangePass(request):
    if request.method == "POST":
        if 'username' in request.session:
            username = request.session['username']
            password = request.POST.get('password')

            if not password:
                messages.error(request, 'Password cannot be empty.')
                return redirect('postNewPass')

            try:
                user = User.objects.get(username=username)
                user.password = make_password(password)
                user.save()
                messages.success(request, 'Password updated successfully!')
                return redirect('main')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('main')
        else:
            return redirect('main')
    else:
        return render(request, 'postchangePass.html')

@login_required(login_url='main')
def home(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'home.html')

@login_required(login_url='main')
def dashboard(request):
    context ={}
    return render(request,'dashboard.html', context)

@login_required(login_url='main')
def invoice(request):
    context ={}
    invoices = Invoice.objects.all()
    context ['invoices'] = invoices
    return render(request,'invoices.html', context)

@login_required(login_url='main')
def product(request):
    context ={}
    products = Product.objects.all()
    context['products'] = products
    return render(request,'products.html', context)

@login_required(login_url='main')
def company(request):
    context = {}
    companies = Company.objects.all()  
    context['companies'] = companies  

    if request.method == 'GET':
        form = CompanyForm()
        context['form'] = form
        return render(request, 'company.html', context)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'New Company Added')
            return redirect('company')
        else:
            messages.error(request, 'Problem processing your request')
            context['form'] = form
            return render(request, 'company.html', context)

    return render(request, 'company.html', context)


@login_required(login_url='main')
def createInvoice(request):

    number = 'INV-'+str(uuid4()).split('-')[4]
    newInvoice = Invoice.objects.create(number = number)
    newInvoice.save()

    inv = Invoice.objects.get(number=number)
    return redirect('create-build-invoice', slug = inv.slug)

@login_required(login_url='main')    
def createBuildInvoice(request, slug):

    try: 
        invoice = Invoice.objects.get(slug = slug)
        pass
    except:
        messages.error(request, 'nothing happened')
        return redirect('invoice')

    products = Product.objects.filter(invoice=invoice)

    context = {}  
    context['invoice'] = invoice 
    context['products'] = products 

    if request.method == 'GET':
        prod_form = ProductForm()
        inv_form = InvoiceForm(instance=invoice)
        company_form= CompanySelectForm(initial_company=invoice.company)
        context ['prod_form'] = prod_form
        context ['inv_form'] = inv_form
        context ['company_form'] = company_form
        return render(request, 'create_invoice.html', context)

    if request.method == 'POST':
        prod_form = ProductForm(request.POST)
        inv_form = InvoiceForm(request.POST, instance=invoice)
        company_form= CompanySelectForm(request.POST, initial_company=invoice.company, instance=invoice)


        if prod_form.is_valid():
            obj = prod_form.save(commit=False)
            obj.invoice = invoice
            obj.save()

            messages.success(request, "Invoice product added succesfully")
            return redirect('create-build-invoice', slug = slug)
        elif inv_form.is_valid and 'paymentTerms' in request.POST:
            inv_form.save()

            messages.success(request, "Invoice updated succesfully")
            return redirect('create-build-invoice', slug = slug)
        elif company_form.is_valid() and 'company' in request.POST:
            
            company_form.save()
            messages.success(request, "Client added to invoice succesfully")
            return redirect('create-build-invoice', slug = slug)
        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            context ['company_form'] = company_form
            messages.error(request,"Problem processing your request")
            return render(request, 'create_invoice.html', context)


    return render(request, 'create_invoice.html', context)
