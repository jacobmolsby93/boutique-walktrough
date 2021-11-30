from django.shortcuts import (
    render,
    reverse,
    redirect,
    HttpResponse,
    get_object_or_404
)
from django.contrib import messages 

from products.models import Product
# Create your views here.

def view_bag(request):
    """
    A view to renders the bag content page
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add quantity of specified product to the shopping bag 
    """

    product = get_object_or_404(Product, pk=item_id)    
    quantity = int(request.POST.get('quantity')) # get the quantity as a string, converts it to an int
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST: 
        size = request.POST['product_size']
    bag = request.session.get('bag', {}) # trying to get the varible if it already exists, if not assign to an empty dictionary

    if size:
        if item_id in list(bag.keys()): # Add item to bag if it does not exist, or add quantity of item if it exists in the bag
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f"Updated Size: {size.upper()} - {product.name} quantity to {bag[item_id]['items_by_size'][size]}")
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added Size: {size.upper()} - {product.name} to your bag')
        else: 
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added Size: {size.upper()} - {product.name} to your bag')
    else: 
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else: 
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')
    
    request.session['bag'] = bag  # Updates the bag varible to the updated version.
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of item in the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST: 
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f"Updated Size: {size.upper()} - {product.name} quantity to {bag[item_id]['items_by_size'][size]}")
        else: 
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed Size: {size.upper()} - {product.name} from your bag')
    else: 
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else: 
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
        
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the item from the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)    
    try:
        size = None
        if 'product_size' in request.POST: 
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed Size: {size.upper()} - {product.name} from your bag')
        else: 
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
            
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
