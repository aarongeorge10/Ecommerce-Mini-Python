from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, img_up, User_reg, Order, OrderItem
from django.contrib.auth import authenticate ,login as log,logout
# from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.core.mail import send_mail


# Create your views here.

def home(request):
    car = img_up.objects.all()
    return render(request, "home.html", {"car": car})

def register(request):
    return render(request,"register.html")

def login(request):
    return render(request,"login.html")

def get_current_user(request):
    user_id = request.session.get('id')
    if not user_id:
        return None
    return User_reg.objects.filter(id=user_id).first()

def userreg(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        username = request.POST.get('username')
        password = request.POST.get('password')
        User_reg(name=name,email=email,phonenumber=phonenumber,username=username,password=password).save()
    return render(request,'register.html')

def userlog(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        cr = User_reg.objects.filter(username=username,password=password)
        if cr:
            user_details = User_reg.objects.get(username=username,password=password)
            id=user_details.id
            name=user_details.name
            email=user_details.email

            request.session['id']=id
            request.session['name']=name
            request.session['email']=email

            send_mail(
                "Login", #subject
                "login successfully completed", #message
                "marzellousgaming@gmail.com",
                [email],
                fail_silently =False,
            )

            return redirect('userdashb')
        else:
            return render(request,'login.html',{'error':'Incorrect Username or Password'})       
    else:
        return render(request,'home.html')
    
def userdashb(request):
    user = get_current_user(request)

    if user:
        # logged-in → count from Cart table
        cart_count = Cart.objects.filter(user=user).aggregate(
            total=Sum('quantity')
        )['total'] or 0
    else:
        # anonymous → count from session
        session_cart = request.session.get('cart', {})
        cart_count = sum(session_cart.values())

    id = request.session.get('id')
    name = request.session.get('name')
    car = img_up.objects.all()

    return render(request, "userdashb.html", {
        'id': id,
        'name': name,
        'car': car,
        'cart_count': cart_count,
    })


def usercart(request, *args, **kwargs):
    items = []
    total_items = 0
    total_price = 0

    user = get_current_user(request)

    if user:
        # Logged-in User_reg → read from Cart table
        rows = Cart.objects.filter(user=user).select_related('product')
        for r in rows:
            product = getattr(r, 'product', None) or getattr(r, 'img_up', None)
            if not product:
                continue
            qty = int(getattr(r, 'quantity', 1) or 1)
            price = float(getattr(product, 'price', 0) or 0)
            subtotal = price * qty
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
            total_items += qty
            total_price += subtotal

    else:
        # Anonymous → session cart (keep your existing code here)
        session_cart = request.session.get('cart', {}) # expected {'1': 2, '4': 1}
        if session_cart:
            # safe parse ids
            try:
                ids = [int(k) for k in session_cart.keys()]
            except Exception:
                ids = []
            products = img_up.objects.filter(id__in=ids)
            prod_map = {p.id: p for p in products}
            for pid_str, qty in session_cart.items():
                try:
                    pid = int(pid_str)
                    qty = int(qty) or 0
                except Exception:
                    continue
                product = prod_map.get(pid)
                if not product:
                    continue
                price = float(getattr(product, 'price', 0) or 0)
                subtotal = price * qty
                items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
                total_items += qty
                total_price += subtotal

    return render(request, 'cart.html', {
        'cart_items': items,
        'total_items': total_items,
        'total_price': total_price,
    })

def userlogout(request):
    logout(request)
    return redirect('home')

def cart(request):
    return render(request,"cart.html")


def add_to_cart(request, product_id):
    product = get_object_or_404(img_up, id=product_id)
    user = get_current_user(request)  # your custom user, from session

    if user:
        # Logged-in user → store in Cart model
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': 0}  # start at 0, then increment below
        )

        # Increment in the database
        Cart.objects.filter(pk=cart_item.pk).update(
            quantity=F('quantity') + 1
        )

        # Optional: refresh the object in memory if you need the new value
        cart_item.refresh_from_db()

    else:
        # Anonymous user → session cart
        session_cart = request.session.get('cart', {})
        pid_str = str(product.id)
        session_cart[pid_str] = session_cart.get(pid_str, 0) + 1
        request.session['cart'] = session_cart

    return redirect(request.META.get('HTTP_REFERER', 'userdashb'))

def increase_qty(request, product_id):
    product = get_object_or_404(img_up, id=product_id)
    user = get_current_user(request)

    if not user:
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        return redirect('usercart')

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('usercart')

def decrease_qty(request, product_id):
    product = get_object_or_404(img_up, id=product_id)
    user = get_current_user(request)  # <-- use your custom user

    # anonymous user -> session cart
    if not user:
        cart = request.session.get('cart', {})
        key = str(product_id)
        if key in cart:
            if cart[key] > 1:
                cart[key] -= 1
            else:
                # remove key if qty would go to 0
                cart.pop(key)
            request.session['cart'] = cart
        return redirect('usercart')

    # logged-in user -> DB cart (Cart.user is a FK to User_reg)
    try:
        cart_item = Cart.objects.get(user=user, product=product)
    except Cart.DoesNotExist:
        # nothing to do
        return redirect('usercart')

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('usercart')


def remove_item(request, product_id):
    product = get_object_or_404(img_up, id=product_id)
    user = get_current_user(request)

    # anonymous user -> session cart
    if not user:
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        return redirect('usercart')

    # logged-in user -> DB cart
    Cart.objects.filter(user=user, product=product).delete()
    return redirect('usercart')



def checkout(request):
    user = get_current_user(request)  # your custom user (User_reg) or None

    items = []
    total_price = Decimal('0.00')

    if user:
        # ✅ Logged-in user → build items from Cart table
        rows = Cart.objects.filter(user=user).select_related('product')
        if not rows.exists():
            return redirect('usercart')  # nothing in DB cart

        for r in rows:
            product = getattr(r, 'product', None) or getattr(r, 'img_up', None)
            if not product:
                continue

            qty = int(getattr(r, 'quantity', 1) or 1)
            price = Decimal(str(getattr(product, 'price', 0) or 0))
            subtotal = price * qty

            items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal,
            })
            total_price += subtotal

    else:
        # ✅ Anonymous user → build items from session cart
        session_cart = request.session.get('cart', {})
        if not session_cart:
            return redirect('usercart')

        try:
            ids = [int(k) for k in session_cart.keys()]
        except Exception:
            ids = []

        products = img_up.objects.filter(id__in=ids)
        prod_map = {p.id: p for p in products}

        for pid_str, qty in session_cart.items():
            try:
                pid = int(pid_str)
                qty = int(qty) or 0
            except Exception:
                continue

            product = prod_map.get(pid)
            if not product:
                continue

            price = Decimal(str(product.price))
            subtotal = price * qty

            items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal,
            })
            total_price += subtotal

    # 🚦 Handle POST (placing the order)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            # re-render checkout with error
            return render(request, 'checkout.html', {
                'cart_items': items,
                'total_price': total_price,
                'error': 'Please select a payment method.',
            })

        # Create Order (user may be None if anonymous)
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            payment_method=payment_method,
        )

        # Create OrderItems
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=Decimal(str(item['product'].price)),
            )

        # 🧹 Clear cart after order
        if user:
            Cart.objects.filter(user=user).delete()  # clear DB cart
        else:
            request.session['cart'] = {}             # clear session cart

        # Go to invoice page
        return redirect('invoice', id=order.id)

    # GET → show checkout page
    return render(request, 'checkout.html', {
        'cart_items': items,
        'total_price': total_price,
    })

def invoice(request, id):
    # Get the logged-in User_reg from the session (same logic as checkout)
    user_obj = None
    user_id = request.session.get('id')
    if user_id:
        user_obj = User_reg.objects.filter(id=user_id).first()

    # Get the order by id
    order = get_object_or_404(Order, id=id)

    # (Optional but recommended) – ensure the order belongs to this user
    if user_obj and order.user_id != user_obj.id:
        return HttpResponseForbidden("You are not allowed to view this invoice.")

    # Get items for this order from OrderItem, NOT Cart
    items = OrderItem.objects.filter(order=order)

    # Calculate total from the order items
    
    grand_total = 0
    for item in items:
        item.row_total = item.price * item.quantity
        grand_total += item.row_total


    return render(request, "invoice.html", {
        "order": order,
        "items": items,
        "total": grand_total,
    })

def history(request):
    user = get_current_user(request)

    if not user:
        # no custom user logged in → send to login page
        return redirect('login')

    # fetch all orders for this user (latest first)
    orders = Order.objects.filter(user=user).order_by('-id')

    return render(request, "history.html", {
        "orders": orders,
    })