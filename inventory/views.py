from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ViewSet):
	
	permission_classes = [IsAuthenticated]

	def retrieve(self, request, pk=None):
		item = cache.get(f'item_{pk}')
		if item is None:
			item = get_object_or_404(Item, pk=pk)
			cache.set(f'item_{pk}', item)
		serializer = ItemSerializer(item)
		return Response(serializer.data)

	def create(self, request):
		serializer = ItemSerializer(data=request.data)
		if Item.objects.filter(name=request.data.get('name')).exists():
			return Response({'data': 'Item with this name already exists.'}, status=status.HTTP_201_CREATED)
		if serializer.is_valid():
			serializer.save()
			return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)
		return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
	

	def update(self, request, pk=None):
		item = get_object_or_404(Item, pk=pk)
		serializer = ItemSerializer(item, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			cache.set(f'item_{pk}', item)
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def destroy(self, request, pk=None):
		item = get_object_or_404(Item, pk=pk)
		cache.delete(f'item_{pk}')
		item.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
