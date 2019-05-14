from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from django.template import loader
import json

# Create your views here.
# def index(request):
#     context = None
#     return render(request, 'menu_backend/index.html', context)

def howdy(request):
    return JsonResponse({"pong": "Howdy"})

def index(request):
    # template = loader.get_template('menu_backend/index.html')
    # context = None
    return render(request, 'menu_backend/index.html', None, )

def checkIfValidAssociates(item_type, items):
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
        return JsonResponse({"error": "More than one item with the same name in the menu!"})
    
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

def getItem(request, itemName):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET allowed"})
    try:
        item = Item.objects.get(name=itemName)
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item does not exist in the menu yet"})  
    
    ret_item = get_item_dict(item)
    return JsonResponse(ret_item)

def getAllItems(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET allowed"})
    
    items = Item.objects.all()
    ret_items = []
    for item in items:
        #ret_item = get_item_dict(item)
        ret_item = item['name']
        ret_items.append(ret_item)
    return ret_items

    



    



    
        


    
