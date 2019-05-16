from django.test import TestCase, Client
from django.core.paginator import Paginator
import random
import math
from .models import *

# Create your tests here.

class MyTests(TestCase):

    ingr = ['ingr' + str(i) for i in range(1,41)]
    
    ########## Helper Functions ##############
    def setup(self):
        self.client = Client()
        return

    
    def addItem(self, name, _type, ingr, well_with=None):
        item = {'name': name, 'type': _type, 'ingredients': ingr}
        if well_with:
            item['well_with'] = well_with
        res = self.client.post('/api/v1/menu/addItem/', item, content_type='application/json')
        assert('success' in res.json())
        assert(res.status_code == 200)
        return
    
    def updateItem(self, name, oldname, _type, ingr, well_with=None):
        item = {'name': name, 'type': _type, 'ingredients': ingr, 'oldname':oldname}
        if well_with:
            item['well_with'] = well_with
        res = self.client.post('/api/v1/menu/updateItem/', item, content_type='application/json')
        assert('success' in res.json())
        assert(res.status_code == 200)
        return

    def deleteItem(self, name):
        res = self.client.post('/api/v1/menu/deleteItem/', {'name': name})
        self.assertRedirects(res, '/api/v1/menu/')
        return

    def checkMenu(self, num_items):
        res = self.client.get('/api/v1/menu/')
        assert(len(res.templates) == 1)
        for template in res.templates:
            assert(template.name == 'menu_backend/index.html')
        assert('items' in res.context)
        num_pages = math.ceil(num_items / 20.0) if math.ceil(num_items / 20.0) is not 0 else 1
        assert(res.context['items'].paginator.num_pages == num_pages)
        assert(res.context['items'].paginator.count == num_items)
        return

    
    def insertAndCheckItems(self, num_items):
        print('2:Inserting and checking menu')
        for i in range(num_items):
            self.addItem('initial_' + str(i), random.choice(['snack', 'drink']), random.sample(self.ingr, 3))

        print('2:Making menu request')
        self.checkMenu(num_items)
        return
    
    def addItemsWithSides(self, numItems):
        print("3: getting sides lists")
        drinks = list(Drink.objects.all().values_list('item__name', flat=True))
        snacks = list(Snack.objects.all().values_list('item__name', flat=True))
        #print(snacks)
        print("3: adding items with sides")
        for i in range(numItems):
            _type = random.choice(['snack', 'drink'])
            if _type == 'snack':
                well_with = random.sample(drinks, 3)
            else:
                well_with = random.sample(snacks, 3)
            self.addItem('withsides_' + str(i), _type, random.sample(self.ingr, 3), well_with=well_with)
        return
    
    def checkSides(self):
        items = Item.objects.all()
        for item in items:
            if hasattr(item, 'snack'):
                drinks = item.snack.drinks.all()
                for drink in drinks:
                    assert(item.name in list(drink.snack_set.all().values_list('item__name', flat=True)))

            else:
                snacks = item.drink.snack_set.all()
                for snack in snacks:
                    assert(item.name in list(snack.drinks.all().values_list('item__name', flat=True)))

        return
    
    ############ Test Cases ###############

    def test_getEmptyMenu(self):
        self.setup()
        print('1:Getting empty menu')
        self.checkMenu(0)
        return
    
    def test_insertAndCheckItems(self):
        self.insertAndCheckItems(100)
        return
    
    def test_addSidesAndCheckMenu(self):
        self.setup()
        print('3:Adding items without sides')
        for i in range(100):
            self.addItem('initial_' + str(i), random.choice(['snack', 'drink']), random.sample(self.ingr, 3))
        print("3: Adding items with sides and checking menu")
        self.addItemsWithSides(100)
        print("3: Checking menu")
        self.checkMenu(200)
        print("3:Checking sides")
        self.checkSides()
        return
    
    def test_updateItem(self):
        self.setup()
        print('4: Adding item')
        self.addItem('testing_update', 'snack', ['ingr1', 'ingr2'])
        print('4: Updating item')
        self.updateItem('testing_update', 'testing_update', 'snack', ['ingr1', 'ingr2', 'ingr3', 'ingr4'])
        self.updateItem('testing_update_new', 'testing_update', 'snack', ['ingr1', 'ingr2', 'ingr3', 'ingr4'])
        print('4: Checking menu')
        self.checkMenu(1)
        return
    
    def test_deleteItem(self):
        self.setup()
        print("5: Adding item")
        self.addItem('testing_delete', 'snack', ['ingr1', 'ingr2'])
        print("5: Deleting item")
        self.deleteItem('testing_delete')
        print("5: Checking if in DB")
        item = Item.objects.filter(name='testing_delete')
        if not item:
            return
        else:
            raise AssertionError("Item still exists")
        return

        


