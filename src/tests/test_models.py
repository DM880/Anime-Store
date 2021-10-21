from django.test import TestCase

from store.data.item.models import Item , ItemReview
from store.data.user.models import CustomUser as User


class ItemTest(TestCase):

    def create_item(self):

        item_data = {
            'item_name': "Test Item",
            'item_description': "This is a test description",
            'price': 20.20,
            'category': "ANIME",
        }

        return Item.objects.create(**item_data)


    def test_item_creation(self):
        item_ex = self.create_item()
        self.assertTrue(isinstance(item_ex, Item))


class UserTest(TestCase):

    def create_user(self):

        user_info = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'Test',
            'date_of_birth': '2021-10-21',
            'email': 'thisisatest@test.com',
            'password': 'test12345',
        }

        return User.objects.create(**user_info)


    def test_user_create(self):
        user_ex = self.create_user()
        self.assertTrue(isinstance(user_ex, User))