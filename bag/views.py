from django.shortcuts import render, redirect

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
    quantity = int(request.POST.get('quantity')) # get the quantity as a string, converts it to an int
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {}) # trying to get the varible if it already exists, if not assign to an empty dictionary

    if item_id in list(bag.keys()): # Add item to bag if it does not exist, or add quantity of item if it exists in the bag
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
    
    request.session['bag'] = bag # Updates the bag varible to the updated version.
    print(request.session['bag'])
    return redirect(redirect_url)