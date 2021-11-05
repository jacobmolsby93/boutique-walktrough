from django.shortcuts import render, reverse, redirect, HttpResponse
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

    product = Product.objects.get(pk=item_id)
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
            else:
                bag[item_id]['items_by_size'][size] = quantity
            
        else: 
            bag[item_id] = {'items_by_size': {size: quantity}}
    else: 
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else: 
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')
    
    request.session['bag'] = bag  # Updates the bag varible to the updated version.
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of item in the shopping bag
    """
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST: 
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else: 
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id) 
    else: 
        if quantity > 0:
            bag[item_id] = quantity
        else: 
            bag.pop(item_id)
        
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the item from the shopping bag
    """
    try:
        size = None
        if 'product_size' in request.POST: 
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id) 
        else: 
            bag.pop(item_id)
            
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e, status=500)
