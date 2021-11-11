from django.core.checks import messages
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def about(request):
    return render(request, 'about.html')

def SignUp(request):
    return render(request, 'signup.html')

class myIndexView(View):
    def get(self, request):
        products = Product.objects.all()
        print(products)
        context = {
            'products': products,

        }
        return render(request, 'index.html', context)


class myDashboardView(View):
    def get(self, request):
        customers = Customer.objects.all()
        products = Product.objects.all()
        item_types = ProductType.objects.all()
        customerCount = customers.count()
        productCount = products.count()
        typeCount = item_types.count()
        orders = CartItem.objects.all()
        sales = sum(orders.values_list('total_price', flat=True))
        print(sales)
            

        context = {
            'customers': customers,
            'products': products,
            'item_types': item_types,
            'customerCount': customerCount,
            'productCount': productCount,
            'typeCount': typeCount,
            'sales': sales,
        }
        return render(request, 'dashboard.html', context)

    def post(self, request):
        username = request.POST.get("username")
        user = Customer.objects.filter(username=username).delete()
        return redirect('Lokalapp:my_dashboard_view')


class myCartView(View):
    def get(self, request):
        return render(request, 'cart.html', {})


class myContactView(View):
    def get(self, request):
        return render(request, 'page-contact.html', {})


class myShopView(View):
    def get(self, request):
        return render(request, 'shop.html', {})


class myContactUsView(View):
    def get(self, request):
        return render(request, 'contact.html', {})


#class myAboutView(View):
 #   def get(self, request):
  #      return render(request, 'about.html', {})


class myFeatureView(View):
    def get(self, request):
        return render(request, 'features.html', {})


class myAddUserView(View):
    def get(self, request):
        return render(request, 'add/addUser.html', {})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.POST.get("username")
            pword = request.POST.get("password")
            first = request.POST.get("firstname")
            last = request.POST.get("lastname")
            number = request.POST.get("phonenumber")
            st = request.POST.get("street")
            ct = request.POST.get("city")
            ctry = request.POST.get("country")
            if Customer.objects.filter(username=user).exists():
                    messages.error(request, 'Username already exists')
                    return redirect('RBApp:my_dashboard_view')

           # form = Customer(username = user, password = pword, firstname = first, lastname = last, phonenumber = number, street = st, city = ct, country = ctry)
            # form.save()
            customer = Customer.objects.create_user(
                username=user,  first_name=first, last_name=last, phone_number=number, street=st, city=ct, country=ctry, password=pword)
            return redirect('Lokalapp:my_dashboard_view')
        else:
            print(form.errors)
            return HttpResponse('not valid')


class myAddProductView(View):
    def get(self, request):
        return render(request, 'add/addProduct.html', {})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            nme = request.POST.get("name")
            prce = request.POST.get("price")
            dscrptn = request.POST.get("description")
            form = Product(name=nme, price=prce, description=dscrptn)
            form.save()
            # return render(request, 'forms/user-form.html', {})
            return redirect('Lokalapp:my_dashboard_view')


class myAddTypeView(View):
    def get(self, request):
        return render(request, 'add/addType.html', {})

    def post(self, request):
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            nme = request.POST.get("name")
            dscrptn = request.POST.get("description")
            form = ProductType(name=nme, description=dscrptn)
            form.save()

            return redirect('Lokalapp:my_dashboard_view')
        else:
            messages.error(request, "Error")


def delete_customer(request, username):
    obj = Customer.objects.get(username=username)
    obj.delete()
    return redirect('Lokalapp:my_dashboard_view')


def delete_product(request, item_code):
    product = Product.objects.get(item_code=item_code)
    product.delete()
    return redirect('Lokalapp:my_dashboard_view')


def delete_product_type(request, type_code):
    type = ProductType.objects.get(type_code=type_code)
    type.delete()
    return redirect('Lokalapp:my_dashboard_view')


def edit_customer(request, username):
    template = 'add/editCustomer.html'
    customer = Customer.objects.get(username=username)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        user = request.POST.get("username")
        pword = request.POST.get("password")
        first = request.POST.get("firstname")
        last = request.POST.get("lastname")
        number = request.POST.get("phonenumber")
        st = request.POST.get("street")
        ct = request.POST.get("city")
        ctry = request.POST.get("country")
        try:
            # update_customer = Customer.objects.filter(username = username).update(password = pword, firstname = first, lastname = last, phonenumber = number, street = st, city = ct, country = ctry)
            # print(update_customer)
            customer = Customer.objects.update_user(
                username=user,  first_name=first, last_name=last, phone_number=number, street=st, city=ct, country=ctry, password=pword)
            messages.success(request, 'User has been updated.')

        except Exception as e:
            messages.warning(
                request, 'User was not saved due to error: {}'.format(e))

        return redirect('Lokalapp:my_dashboard_view')

    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'customer': customer,
    }

    return render(request, template, context)


def edit_product(request, item_code):
    template = 'add/editProduct.html'
    product = Product.objects.get(item_code=item_code)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        nme = request.POST.get("name")
        prce = request.POST.get("price")
        dscrptn = request.POST.get("description")
        try:
            update_product = Product.objects.filter(item_code=item_code).update(
                name=nme, price=prce, description=dscrptn)
            print(update_product)
            messages.success(request, 'User has been updated.')

        except Exception as e:
            messages.warning(
                request, 'User was not saved due to error: {}'.format(e))

        return redirect('Lokalapp:my_dashboard_view')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def edit_product_type(request, type_code):
    template = 'add/editType.html'
    type = ProductType.objects.get(type_code=type_code)
    if request.method == "POST":
        form = ProductTypeForm(request.POST, instance=type)
        nme = request.POST.get("name")
        dscrptn = request.POST.get("description")
        try:
            update_type = ProductType.objects.filter(
                type_code=type_code).update(name=nme, description=dscrptn)
            messages.success(request, 'User has been updated.')

        except Exception as e:
            messages.warning(
                request, 'User was not saved due to error: {}'.format(e))

        return redirect('Lokalapp:my_dashboard_view')
    else:
        form = ProductTypeForm(instance=type)

    context = {
        'form': form,
        'type': type,
    }

    return render(request, template, context)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        uname = request.POST.get("username")
        pword = request.POST.get("password")
        customer = authenticate(request, username = uname, password = pword)
        print(customer)
        
        if customer is not None:
            login(request, customer)
            return redirect('Lokalapp:my_index_view')
        else:
            messages.error(request, 'Username or Password do not match')
            return redirect('Lokalapp:my_login_view')

def logout_view(request):
    logout(request)
    return redirect('Lokalapp:my_login_view')

class mySignUpView(View):
    def get(self, request):
        return render(request, 'signup.html', {})

    def post(self, request):
        crt = CartForm(request.POST)
        uname = request.POST.get("username")
        pNumber = request.POST.get("phone_number")
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        pword = request.POST.get("password")
        strt = request.POST.get("street")
        cty = request.POST.get("city")
        cntry = request.POST.get("country")
        prce = 0.0
        if Customer.objects.filter(username = uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('RBApp:my_signup_view')
        else:
            if str.isnumeric(pNumber):
                user = Customer.objects.create_user(username = uname,  firstname = fname, lastname = lname, phonenumber = pNumber, street = strt, city = cty, country = cntry, password = pword)
                crt = Cart(username = uname, total_price = prce)
                crt.save()
                messages.success(request, "User successfully created.")
                return redirect('Lokalapp:my_login_view')
            else:
                messages.error(request, 'Phone number must contain numbers only')
                return redirect('Lokalapp:my_signup_view')

def add_to_cart(request, item_code):
    form = CartItemForm(request.POST)
    if request.user.is_authenticated:
        user = request.user.username
        user_cart = Cart.objects.get(username = user)
        cart_id = user_cart.cart_id
        exists =  CartItem.objects.filter(cart_id = cart_id, item_code = item_code)
        if exists.exists():
            messages.error(request, "The product is already in your cart.")
            return redirect('Lokalapp:my_index_view')
        else:
            query = Product.objects.get(item_code = item_code)
            price = query.price
            form = CartItem(item_code = Product.objects.get(item_code = item_code), quantity = 1, total_price = price, cart_id = cart_id)
            form.save()
            
            return redirect('Lokalapp:my_cart_view')



def remove_to_cart(request, item_code):
    if request.user.is_authenticated:
        user = request.user.username
        user_cart = Cart.objects.get(username = user)
        cartItems = CartItem.objects.get(cart_id = user_cart.cart_id, item_code = item_code)
        cartItems.delete()
        
        return redirect('Lokalapp:my_cart_view')


class myCartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user.username
            user_cart = Cart.objects.get(username = user)
            cartItems = CartItem.objects.filter(cart_id = user_cart.cart_id)
            products = Product.objects.all()
            totalPrice = 0
            count = 0

            for item in cartItems:
                totalPrice += item.total_price
                count += 1
            
            context = {
                'cartItems': cartItems,
                'totalPrice': totalPrice,
                'products': products,
                'count': count,
            }
            return render(request, 'cart.html', context)

def qtyCounter(request, item_code):
    if request.user.is_authenticated:
        user = request.user.username
        user_cart = Cart.objects.get(username = user)
        cartItems = CartItem.objects.get(cart_id = user_cart.cart_id,item_code = item_code)
        item = Product.objects.get(item_code = item_code)
        quantity = cartItems.quantity
       

        if request.POST.get('add'):
       
            quantity = cartItems.quantity + 1
            price =  item.price * quantity
            update = CartItem.objects.filter(cart_id = user_cart.cart_id, item_code = item_code).update(quantity = quantity)
            update2 = CartItem.objects.filter(cart_id = user_cart.cart_id, item_code = item_code).update(total_price = price)
            # print("DISH: " + str(dish.price))
            # print("Quantity: " + str(cartItems.quantity))
            # print("Quantity var: " + str(quantity))
            # print("TOTAL: " + str(price))
         

            return redirect('Lokalapp:my_cart_view') 

        elif request.POST.get('minus'):

            if cartItems.quantity != 1:
                quantity = cartItems.quantity - 1
                price =  item.price * quantity
                update = CartItem.objects.filter(cart_id = user_cart.cart_id, item_code = item_code).update(quantity = quantity)
                update2 = CartItem.objects.filter(cart_id = user_cart.cart_id,item_code = item_code).update(total_price = price)
           

            return redirect('Lokalapp:my_cart_view') 
        
        return redirect('Lokalapp:my_index_view') 


    