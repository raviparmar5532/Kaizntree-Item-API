from django.test import TestCase
from .models import Item, Tag
from django.contrib.auth.models import User

class TagModelTestCase(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(tag='tag1')
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.tag, 'tag1')

    def test_tag_str_representation(self):
        tag = Tag.objects.create(tag='tag1')
        self.assertEqual(str(tag), 'tag1')

class ItemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_create_item(self):
        item = Item.objects.create(
            SKU='ITEM1',
            name='Test Item',
            description='Test Description',
            category='BUN',
            in_stock=10,
            available_stock=10,
            user=self.user
        )
        item.tags.add(Tag.objects.create(tag='tag1'))
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(item.SKU, 'ITEM1')

    def test_item_str_representation(self):
        item = Item.objects.create(
            SKU='ITEM1',
            name='Test Item',
            description='Test Description',
            category='BUN',
            in_stock=10,
            available_stock=10,
            user=self.user
        )
        item.tags.add(Tag.objects.create(tag='tag1'))
        self.assertEqual(str(item), 'Test Item')

    def test_unique_sku_per_user(self):
        Item.objects.create(
            SKU='ITEM1',
            name='Test Item 1',
            description='Test Description 1',
            category='BUN',
            in_stock=10,
            available_stock=10,
            user=self.user
        )
        # Try to create another item with the same SKU for the same user
        with self.assertRaises(Exception):
            Item.objects.create(
                SKU='ITEM1',
                name='Test Item 2',
                description='Test Description 2',
                category='BUN',
                in_stock=5,
                available_stock=5,
                user=self.user
            )
