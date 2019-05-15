from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from django.template import loader
import json
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.

def index(request):
    all_items = getAllItems()
    all_items = all_items['items']
    paginator = Paginator(all_items, 2)
    if not 'page' in request.GET:
        page_num = 1
    else:
        page_num = int(request.GET.get('page'))
    return render(request, 'menu_backend/index.html', {'items':paginator.get_page(page_num)})

def item(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET allowed"})
    try:
        item = Item.objects.get(name=request.GET.get('name'))
    except Item.DoesNotExist:
        raise Http404("Item does not exist on the menu")
    
    ret_item = get_item_dict(item)
    print(ret_item)
    return render(request, 'menu_backend/item.html', {'item': ret_item})
    
def updateView(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET allowed"})
    try:
        item = Item.objects.get(name=request.GET.get('name'))
    except Item.DoesNotExist:
        raise Http404("Item does not exist on the menu")
    
    ret_item = get_item_dict(item)
    well_with = to_arr(Drink.objects.all().values_list('item__name', flat=True)) if hasattr(item, 'snack') else \
        to_arr(Snack.objects.all().values_list('item__name', flat=True))
    context = {
        'item': ret_item, 
        'well_with': well_with, 
        'title': 'Coffee Cart Update Item',
        'button_val': 'Update Item',
        'form_type': 'update-form'
        }
    return render(request, 'menu_backend/editItem.html', context)

def addView(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET allowed"})
    ret_item = {
        "name": "",
        "type": request.GET.get('type'),
        "ingredients": [],
        "goes_well_with": []
    }
    
    well_with = to_arr(Drink.objects.all().values_list('item__name', flat=True)) if request.GET.get('type') == 'snack' else \
        to_arr(Snack.objects.all().values_list('item__name', flat=True))
    context = {
        'item': ret_item, 
        'well_with': well_with, 
        'title': 'Coffee Cart Add Item',
        'button_val': 'Add to menu',
        'form_type': 'add-form'
        }
    return render(request, 'menu_backend/editItem.html', context)

def checkIfValidAssociates(item_type, items):
    if not items:
        return True
    if item_type == "snack":
        if not Drink.objects.filter(item__name__in=items).exists():
            return False
    elif item_type == "drink":
        if not Snack.objects.filter(item__name__in=items).exists():
            return False
    else:
        return False
    return True

def addWellWith(snack_or_drink, well_with, _type):
    if _type == 'snack':
        snack_or_drink.addDrinks(well_with)
    else:
        snack_or_drink.addSnacks(well_with)
    return

def addItem(request):

    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"})
    print("Here")
    print(request.body)
    rbody = json.loads(request.body)
    print(rbody)
    item = Item.objects.filter(name=rbody['name'])

    if item.exists():
        return JsonResponse({"error": "Item with the same name already in the menu!"})
    
    if rbody['type'] not in ["snack", "drink"]:
        return JsonResponse({"error": "Item must be either a snack or a drink"})
    elif 'well_with' in rbody.keys() and not checkIfValidAssociates(rbody['type'], rbody['well_with']):
        return JsonResponse({"error": "Invalid associated items"})

    
    item = Item(name=rbody['name'], ingredients=rbody['ingredients'])
    item.save()
    if(rbody['type'] == "snack"):
        snack = Snack(item=item)
        snack.save()
        addWellWith(snack, rbody['well_with'], 'snack')
    else:
        drink = Drink(item=item)
        drink.save()
        addWellWith(drink, rbody['well_with'], 'drink')

    return JsonResponse({"success": True})

def deleteItem(request, itemName):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"})
    try:
        item = Item.objects.filter(name=itemName)
        item.delete()
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item to be deleted does not exist"})
    
    return JsonResponse({"success": True})

def updateItem(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"})
    
    rbody = json.loads(request.body)
    try:
        item = Item.objects.get(name=rbody['name'])
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item does not exist in the menu yet"})        
    

    if rbody['type'] not in ["snack", "drink"]:
        return JsonResponse({"error": "Item must be either a snack or a drink"})
    elif 'well_with' in rbody.keys() and not checkIfValidAssociates(rbody['type'], rbody['well_with']):
        return JsonResponse({"error": "Invalid associated items"})
    
    item.delete()
    item = Item(name=rbody['name'], ingredients=rbody['ingredients'])
    item.save()
    if(rbody['type'] == "snack"):
        snack = Snack(item=item)
        snack.save()
        addWellWith(snack, rbody['well_with'], 'snack')
    else:
        drink = Drink(item=item)
        drink.save()
        addWellWith(drink, rbody['well_with'], 'drink')

    return JsonResponse({"success": True})

def to_arr(qs):
    ret = []
    for q in qs:
        ret.append(q)
    return ret

def get_item_dict(item):
    ret_item = {
        "name": item.name,
        "type": "snack" if hasattr(item, 'snack') else "drink",
        "ingredients": item.ingredients,
        "goes_well_with": to_arr(item.snack.drinks.all().values_list('item__name', flat=True)) if hasattr(item, 'snack') else \
            to_arr(item.drink.snack_set.all().values_list('item__name', flat=True))

    }
    return ret_item

def getAllItems():
    # if request.method != 'GET':
    #     return JsonResponse({"error": "Only GET allowed"})
    
    items = Item.objects.all().order_by('name')
    ret_items = []
    for item in items:
        #ret_item = get_item_dict(item)
        ret_item = item.name
        ret_items.append(ret_item)
    return {"items": ret_items}

    



    



    
        


    
