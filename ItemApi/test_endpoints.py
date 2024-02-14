from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from django.contrib.auth.models import User
from .models import Item
from django.urls import reverse

class ItemAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='xyz')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
    def test_create_item(self):
        data = {
            'SKU': 'ITEM1',
            'name': 'Item',
            'description': 'Testing',
            'category': 'BUN',
            'in_stock': 10,
            'available_stock': 5,
            'tags': [{'tag': 'tag1'},{'tag': 'tag4'}]
        }
        response = self.client.post(reverse('item-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_with_invalid_tag(self):
        data = {
            'SKU': 'ITEM1',
            'name': 'Item',
            'description': 'Testing',
            'category': 'BUN',
            'in_stock': 10,
            'available_stock': 5,
            'tags': [{'tag': 'tag1'},{'tag': 'tag5'}]
        }
        response = self.client.post(reverse('item-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_items(self):
        Item.objects.create(
            SKU='ITEM1',
            name='Test Item',
            description='Test Description',
            category='BUN',
            in_stock=10,
            available_stock=10,
            user=self.user
        )
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_item(self):
        item = Item.objects.create(
            SKU='ITEM1',
            name='Test Item',
            description='Test Description',
            category='BUN',
            in_stock=10,
            available_stock=10,
            user=self.user
        )
        response = self.client.get(reverse('item-detail', args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_update_item(self):
        item = Item.objects.create(
            SKU='ITEM1',
            name='Test Item',
            description='Test Description',
            category='BUN',
            in_stock=10,
            available_stock=10,
            user=self.user
        )
        data = {
            'name': 'Updated Item',
            'tags': [{'tag': 'tag1'}]
        }
        response = self.client.patch(reverse('item-detail', args=[item.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=item.id).name, 'Updated Item')

    def test_delete_item(self):
        item = Item.objects.create(
            SKU='ITEM1',
            name='Test Item',
            description='Test Description',
            category='BUN',
            in_stock=10,
            available_stock=10,
            user=self.user
        )
        self.assertEqual(Item.objects.count(), 1)
        response = self.client.delete(reverse('item-detail', args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
