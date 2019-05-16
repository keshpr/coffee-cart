from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from .models import *
import json
from django.core.paginator import Paginator
from django.http import Http404

##################### Views ######################
#### The checkReqArgs function checks if the required args
#### are in the request object. 


def index(request):
    try:
        all_items = getAllItems()
    except Exception as e:
        print(e)
        return HttpResponseServerError()
    
    all_items = all_items['items']
    paginator = Paginator(all_items, 20)
    if not 'page' in request.GET:
        page_num = 1
    else:
        page_num = int(request.GET.get('page'))
    return render(request, 'menu_backend/index.html', {'items':paginator.get_page(page_num)})

def item(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    
    #### args ####
    if not checkReqArgs(['name'], request.GET):
        return HttpResponseBadRequest('Need name')
    try:
        item = Item.objects.get(name=request.GET.get('name').lower())
    except Item.DoesNotExist:
        raise Http404("Item does not exist on the menu")
    
    ret_item = get_item_dict(item)
    return render(request, 'menu_backend/item.html', {'item': ret_item})
    
def updateView(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    
    #### args ####
    if not checkReqArgs(['name'], request.GET):
        return HttpResponseBadRequest('Need name')
    
    try:
        item = Item.objects.get(name=request.GET.get('name').lower())
    except Item.DoesNotExist:
        raise HttpResponseNotFound("Item does not exist on the menu")
    
    ret_item = get_item_dict(item)
    well_with = list(Drink.objects.all().values_list('item__name', flat=True)) if hasattr(item, 'snack') else \
        list(Snack.objects.all().values_list('item__name', flat=True))
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
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    
    #### args ####
    if not checkReqArgs(['type'], request.GET):
        return HttpResponseBadRequest('Need type')
    
    ret_item = {
        "name": "",
        "type": request.GET.get('type'),
        "ingredients": [],
        "goes_well_with": []
    }
    
    try:
        well_with = list(Drink.objects.all().values_list('item__name', flat=True)) if request.GET.get('type') == 'snack' else \
            list(Snack.objects.all().values_list('item__name', flat=True))
    except Exception as e:
        print(e)
        well_with = []
    
    context = {
        'item': ret_item, 
        'well_with': well_with, 
        'title': 'Coffee Cart Add Item',
        'button_val': 'Add to menu',
        'form_type': 'add-form'
        }
    return render(request, 'menu_backend/editItem.html', context)


def addItem(request):

    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    
    rbody = json.loads(request.body)

    #### args ####
    if not checkReqArgs(['name', 'type', 'ingredients'], rbody):
        return JsonResponse({"error":'Need name, type and ingredients'}, status=400)

    rbody['name'] = rbody['name'].lower()
    try:
        item = Item.objects.filter(name=rbody['name'])
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Something went wrong while trying to add the item"}, status=500)

    if item.exists():
        return JsonResponse({"error": "Item with the same name already in the menu!"}, status=409)
    
    if rbody['type'] not in ["snack", "drink"]:
        return JsonResponse({"error": "Item must be either a snack or a drink"}, status=400)
    if 'well_with' in rbody.keys():
        rbody['well_with'] = getUnique(rbody['well_with'])
    if 'well_with' in rbody.keys() and not checkIfValidAssociates(rbody['type'], rbody['well_with']):
        return JsonResponse({"error": "Invalid associated items"}, status=409)

    rbody['ingredients'] = getUnique(rbody['ingredients'])
    item = Item(name=rbody['name'], ingredients=rbody['ingredients'])
    item.save()
    if(rbody['type'] == "snack"):
        snack = Snack(item=item)
        snack.save()
        if 'well_with' in rbody.keys():
            addWellWith(snack, rbody['well_with'], 'snack')
    else:
        drink = Drink(item=item)
        drink.save()
        if 'well_with' in rbody.keys():
            addWellWith(drink, rbody['well_with'], 'drink')

    return JsonResponse({"success": True})

def deleteItem(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    #### args ####
    if not checkReqArgs(['name'], request.POST):
        return JsonResponse({"error":'Need name'}, status=400)
    
    try:
        item = Item.objects.filter(name=request.POST.get('name').lower())
        item.delete()
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item to be deleted does not exist"}, status=409)
    
    return redirect('index')


def updateItem(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    
    rbody = json.loads(request.body)

    #### args ####
    if not checkReqArgs(['name', 'oldname', 'type', 'ingredients'], rbody):
        return JsonResponse({"error":'Need name, oldname, type and ingredients'}, status=400)

    rbody['name'] = rbody['name'].lower()
    rbody['oldname'] = rbody['oldname'].lower()
    try:
        item = Item.objects.get(name=rbody['oldname'])
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item does not exist in the menu yet"}, status=409)        
    
    if not hasattr(item, rbody['type'] ):
        return JsonResponse({"error": "Cannot change item type, please add a new item in that case"}, status=409)

    if 'well_with' in rbody.keys():
        rbody['well_with'] = getUnique(rbody['well_with'])
    if 'well_with' in rbody.keys() and not checkIfValidAssociates(rbody['type'], rbody['well_with']):
        return JsonResponse({"error": "Invalid side items"}, status=409)
    
    item.delete()
    rbody['ingredients'] = getUnique(rbody['ingredients'])
    item = Item(name=rbody['name'], ingredients=rbody['ingredients'])
    item.save()
    if(rbody['type'] == "snack"):
        snack = Snack(item=item)
        snack.save()
        if 'well_with' in rbody.keys():
            addWellWith(snack, rbody['well_with'], 'snack')
    else:
        drink = Drink(item=item)
        drink.save()
        if 'well_with' in rbody.keys():
            addWellWith(drink, rbody['well_with'], 'drink')

    return JsonResponse({"success": True})

################## Helper Functions #######################

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

def getUnique(things):
    un = dict()
    for thing in things:
        if thing:
            un[thing.lower()] = True
    return list(un.keys())

def checkReqArgs(args, req):
    for key in args:
        if not key in req:
            return False
    return True

def addWellWith(snack_or_drink, well_with, _type):
    if _type == 'snack':
        snack_or_drink.addDrinks(well_with)
    else:
        snack_or_drink.addSnacks(well_with)
    return

def get_item_dict(item):
    ret_item = {
        "name": item.name,
        "type": "snack" if hasattr(item, 'snack') else "drink",
        "ingredients": item.ingredients,
        "goes_well_with": list(item.snack.drinks.all().values_list('item__name', flat=True)) if hasattr(item, 'snack') else \
            list(item.drink.snack_set.all().values_list('item__name', flat=True))

    }
    return ret_item

def getAllItems():    
    items = Item.objects.all().order_by('name')
    ret_items = []
    for item in items:
        #ret_item = get_item_dict(item)
        ret_item = item.name
        ret_items.append(ret_item)
    return {"items": ret_items}

    



    



    
        


    
