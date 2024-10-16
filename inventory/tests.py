from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item
from user import models
import logging
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger('django')

class ItemAPITestCase(APITestCase):

	def setUp(self):
		self.user = models.User.objects.create_user(email='testuser', password='testpassword')
		refresh = RefreshToken.for_user(self.user)
		self.access_token = str(refresh.access_token)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
		self.item_data = {'name': 'Item1', 'description': 'Item 1 description'}
		self.item = Item.objects.create(**self.item_data) 
		self.create_url = '/item/'
		self.detail_url = f'/item/{self.item.id}/'

	def test_create_item(self):
		response = self.client.post(self.create_url, self.item_data, format='json')
		logger.debug(f'Creating item response: {response.data}') 
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_read_item(self):
		response = self.client.get(self.detail_url)
		logger.debug(f'Reading item response: {response.data}') 
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], 'Item1') 

	def test_update_item(self):
		updated_data = {'name': 'Updated Item', 'description': 'Updated description'}
		response = self.client.put(self.detail_url, updated_data, format='json')
		logger.debug(f'Updating item response: {response.data}') 
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], 'Updated Item') 

	def test_delete_item(self):
		response = self.client.delete(self.detail_url)
		logger.debug(f'Deleting item response: {response.data}') 
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Item.objects.filter(id=self.item.id).exists())
