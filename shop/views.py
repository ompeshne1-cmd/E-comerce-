import json
import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import Category, Product, Cart, CartItem, Order, OrderItem

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart

def home(request):
    cart = get_or_create_cart(request)
    products = Product.objects.all().order_by('-is_featured', 'id')
    featured_product = Product.objects.filter(is_featured=True).first() or products.first()
    categories = Category.objects.all()

    context = {
        'cart': cart,
        'cart_items_count': cart.total_items(),
        'products': products,
        'featured_product': featured_product,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)

@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        pack_size = data.get('pack_size', '12-Pack Case')
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)

        # Multiplier pricing based on pack size
        unit_price = product.price
        if pack_size == '4-Pack':
            unit_price = Decimal(str(round(float(product.price) * 0.45, 2)))
        elif pack_size == '24-Pack Party Pack':
            unit_price = Decimal(str(round(float(product.price) * 1.85, 2)))

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            pack_size=pack_size,
            defaults={'quantity': quantity, 'unit_price': unit_price}
        )
        if not created:
            item.quantity += quantity
            item.save()

        items_list = []
        for i in cart.items.select_related('product'):
            items_list.append({
                'id': i.id,
                'product_id': i.product.id,
                'name': i.product.name,
                'pack_size': i.pack_size,
                'quantity': i.quantity,
                'unit_price': float(i.unit_price),
                'subtotal': float(i.subtotal()),
                'image_url': i.product.image_url,
                'primary_color': i.product.primary_color,
            })

        subtotal = float(cart.total_price())
        shipping = 0.0 if subtotal >= 35.0 or subtotal == 0 else 5.99
        total = round(subtotal + shipping, 2)
        needed_for_free_ship = max(0.0, round(35.0 - subtotal, 2))
        progress_pct = min(100, int((subtotal / 35.0) * 100))

        return JsonResponse({
            'success': True,
            'message': f'Added {product.name} to cart!',
            'total_items': cart.total_items(),
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'needed_for_free_ship': needed_for_free_ship,
            'progress_pct': progress_pct,
            'items': items_list
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_POST
def update_cart_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action') # 'increase', 'decrease', 'remove'

        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if action == 'increase':
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        elif action == 'remove':
            item.delete()

        items_list = []
        for i in cart.items.select_related('product'):
            items_list.append({
                'id': i.id,
                'product_id': i.product.id,
                'name': i.product.name,
                'pack_size': i.pack_size,
                'quantity': i.quantity,
                'unit_price': float(i.unit_price),
                'subtotal': float(i.subtotal()),
                'image_url': i.product.image_url,
                'primary_color': i.product.primary_color,
            })

        subtotal = float(cart.total_price())
        shipping = 0.0 if subtotal >= 35.0 or subtotal == 0 else 5.99
        total = round(subtotal + shipping, 2)
        needed_for_free_ship = max(0.0, round(35.0 - subtotal, 2))
        progress_pct = min(100, int((subtotal / 35.0) * 100))

        return JsonResponse({
            'success': True,
            'total_items': cart.total_items(),
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'needed_for_free_ship': needed_for_free_ship,
            'progress_pct': progress_pct,
            'items': items_list
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_GET
def get_cart_data(request):
    cart = get_or_create_cart(request)
    items_list = []
    for i in cart.items.select_related('product'):
        items_list.append({
            'id': i.id,
            'product_id': i.product.id,
            'name': i.product.name,
            'pack_size': i.pack_size,
            'quantity': i.quantity,
            'unit_price': float(i.unit_price),
            'subtotal': float(i.subtotal()),
            'image_url': i.product.image_url,
            'primary_color': i.product.primary_color,
        })

    subtotal = float(cart.total_price())
    shipping = 0.0 if subtotal >= 35.0 or subtotal == 0 else 5.99
    total = round(subtotal + shipping, 2)
    needed_for_free_ship = max(0.0, round(35.0 - subtotal, 2))
    progress_pct = min(100, int((subtotal / 35.0) * 100))

    return JsonResponse({
        'total_items': cart.total_items(),
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'needed_for_free_ship': needed_for_free_ship,
        'progress_pct': progress_pct,
        'items': items_list
    })

@require_POST
def checkout(request):
    try:
        data = json.loads(request.body)
        cart = get_or_create_cart(request)
        
        if cart.items.count() == 0:
            return JsonResponse({'success': False, 'error': 'Your cart is empty!'}, status=400)

        subtotal = cart.total_price()
        shipping = Decimal('0.00') if subtotal >= 35.0 else Decimal('5.99')
        total = subtotal + shipping

        order_num = f"HD-{uuid.uuid4().hex[:6].upper()}"
        order = Order.objects.create(
            order_number=order_num,
            customer_name=data.get('name', 'Hedlum Member'),
            customer_email=data.get('email', 'member@hedlum.com'),
            customer_phone=data.get('phone', ''),
            address=data.get('address', '123 Wild Mountain Rd'),
            city=data.get('city', 'Denver'),
            postal_code=data.get('postal_code', '80202'),
            subtotal_amount=subtotal,
            shipping_fee=shipping,
            total_amount=total,
            status='PAID'
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                pack_size=item.pack_size,
                unit_price=item.unit_price,
                quantity=item.quantity
            )

        # Clear cart items after successful purchase
        cart.items.all().delete()

        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'customer_name': order.customer_name,
            'total': float(order.total_amount),
            'message': 'Order successfully placed! Thank you for choosing Hedlum.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
