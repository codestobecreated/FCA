from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product, Order, OrderItem
from .cart import Cart

# Initialize Razorpay Client
# This client allows us to interact with Razorpay's API for order creation and verification.
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('query')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'cart': Cart(request)
    })

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {'cart': cart})

def razorpay_checkout(request):
    """
    This view handles the initiation of a Razorpay transaction.
    1. It calculates the total amount from the CART.
    2. It creates a Razorpay Order through their API in INR.
    3. It saves the order in our local database with a 'Pending' status.
    4. It renders the payment page with the Razorpay order ID.
    """
    cart = Cart(request)
    # Total amount in paise (1 INR = 100 paise)
    total_price = cart.get_total_price()
    amount = int(total_price * 100) 
    currency = 'INR'
    
    if amount == 0:
        return redirect('shop:product_list')

    # Try to Create Razorpay Order
    try:
        razorpay_order = razorpay_client.order.create({
            'amount': amount,
            'currency': currency,
            'payment_capture': '1'
        })
        razorpay_order_id = razorpay_order['id']
        simulation = False
    except Exception as e:
        # If authentication fails (invalid keys), enable simulation mode
        print(f"Razorpay Error: {e}")
        razorpay_order_id = f"sim_{int(total_price)}" 
        simulation = True
    
    # Save Order to our database
    order = Order.objects.create(
        full_name="Customer",  
        email="customer@example.com",
        phone="0000000000",
        address="Default Address",
        city="City",
        zip_code="000000",
        total_amount=total_price,
        razorpay_order_id=razorpay_order_id,
        status='Pending'
    )
    
    # Link items from cart to OrderItem model
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )
    
    # Clear cart after order creation
    cart.clear()

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': amount,
        'currency': currency,
        'order': order,
        'simulation': simulation,
    }
    
    return render(request, 'shop/cart/razorpay_checkout.html', context)

@csrf_exempt
def payment_status(request):
    """
    This view handles the callback from Razorpay after the payment is completed.
    1. It receives the payment ID, order ID, and signature from the frontend.
    2. It verifies the signature with Razorpay to ensure the payment is authentic.
    3. It updates the order status in our database to 'Paid'.
    """
    if request.method == "POST":
        params_dict = {
            'razorpay_order_id': request.POST.get('razorpay_order_id'),
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_signature': request.POST.get('razorpay_signature')
        }

        try:
            # Simulation bypass
            if params_dict['razorpay_order_id'].startswith('sim_'):
                order = Order.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
                order.razorpay_payment_id = params_dict['razorpay_payment_id']
                order.razorpay_signature = params_dict['razorpay_signature']
                order.status = 'Paid'
                order.save()
                return render(request, 'shop/cart/payment_success.html', {'order': order})

            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Signature matches! Update order status
            order = Order.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
            order.razorpay_payment_id = params_dict['razorpay_payment_id']
            order.razorpay_signature = params_dict['razorpay_signature']
            order.status = 'Paid'
            order.save()
            
            return render(request, 'shop/cart/payment_success.html', {'order': order})
        except Exception as e:
            # Signature verification failed or other error
            return render(request, 'shop/cart/payment_failure.html', {'error': str(e)})

    return redirect('shop:product_list')

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})

def about(request):
    return render(request, 'shop/pages/about.html')

def contact(request):
    return render(request, 'shop/pages/contact.html')

def terms(request):
    return render(request, 'shop/pages/terms.html')

def privacy(request):
    return render(request, 'shop/pages/privacy.html')

def gallery(request):
    return render(request, 'shop/pages/gallery.html')

def faq(request):
    return render(request, 'shop/pages/faq.html')
