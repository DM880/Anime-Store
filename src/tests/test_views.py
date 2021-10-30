from django.test import TestCase
from django.shortcuts import reverse


from store.interfaces.appsite.views import pages
from store.data.user.models import CustomUser as User


class SignUpTest(TestCase):


    def user_data(self):

        user_info = {
            'fname':'name',
            'lname':'surname',
            'username':'usernameunique',
            'email':'test11@gmail.com',
            'birth': '2012-12-12',
            'password1':'XAazypass123411614941',
            'password2':'C1razypass123452+5++++',
        }

        return user_info


    def test_form(self):

        data = {
            'fname':'name',
            'lname':'surname',
            'username':'usernameunique',
            'email':'test11@gmail.com',
            'birth': '2012-12-12',
            'password1':'XAazypass123411614941',
            'password2':'XAazypass123411614941',
            }
        response = self.client.post('/signup/', data)

        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)