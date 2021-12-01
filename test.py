# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from ecommerce.models import Product
from ecommerce.models import User


class EcommerceTestCase(TestCase):

    def setUp(self):

        # Creamos un usuario y generamos el acceso a la api para hacer pruebas de forma general
        user = User(
            email='jhonrambo@hotmail.com',
            first_name='Jhon',
            last_name='Rambo',
            username='jhonrambo'
        )
        user.set_password('Heroe77')
        user.save()

        client = APIClient()
        response = client.post(
                '/ecommerce/login/client/', {
                'email': 'jhonrambo@hotmail.com',
                'password': 'Heroe77',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['token']
        self.user = user


    def test_create_product(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        test_product = {
            "name": "PC Dell Dimension XP",
            "price": "6290000",
            "quantity": "16",
            "tax": "14",
            "image": "imagen2.jpg",
            "description": "ninguna2"
        }

        response = client.post(
            '/ecommerce/create/product/', 
            test_product,
            format='json'
        )

        #result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_update_product(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        # Creamos un objeto en la base de datos para trabajar con datos
        prod = Product.objects.create(
             pk="60",
             name="PC HP Pavilion",
             price="3500000",
             quantity="23",
             tax="16",
             image="imagen5.jpg",
             description="ninguna5"
        )

        test_product_update = {
            "name": "PC ASUS Rog",
            "price": "7290000",
            "quantity": "26",
            "tax": "14",
            "image": "imagen8.jpg",
            "description": "ninguna8"
        }

        response = client.put(
            f'/ecommerce/update/product/{prod.pk}/', 
            test_product_update,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_delete_product(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        # Creamos un objeto en la base de datos para trabajar con datos
        prod = Product.objects.create(
             pk="60",
             name="PC HP Pavilion",
             price="3500000",
             quantity="23",
             tax="16",
             image="imagen5.jpg",
             description="ninguna5"
        )

        response = client.delete(
            f'/ecommerce/delete/product/{prod.pk}/', 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        prod_exists = Product.objects.filter(pk=prod.pk)
        self.assertFalse(prod_exists)