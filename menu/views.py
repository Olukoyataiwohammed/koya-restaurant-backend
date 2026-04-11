from django.shortcuts import render
from .models import Category, MenuItem
from rest_framework.decorators import api_view,permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status,permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .serializer import CategorySerializer,MenuItemSerializer


# Create your views here.

@api_view(http_method_names=["GET"])
@permission_classes([permissions.AllowAny]) 
def categoryView(request):
    categories = Category.objects.all().prefetch_related('menu_items')

    # serialize categories
    serializer = CategorySerializer(instance=categories,many=True)

   

    return Response(data=serializer.data,status=status.HTTP_200_OK)
 

@api_view(http_method_names=["POST"]) 
@permission_classes([permissions.AllowAny])  
def add_category(request):
    data = request.data
    serializer = CategorySerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        response = {
            "message":"Item  Created",
            "data":request.data
        }

        return Response(data=response,status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
   
@api_view(http_method_names=["GET"])
@permission_classes([permissions.AllowAny])
def list_menu_item(request):
    menu_item = MenuItem.objects.all()
    category_id = request.query_params.get('categories', None)

    if category_id is not None:
        menu_item = menu_item.filter(category_id=category_id)
    



    # serialize items
    serializer = MenuItemSerializer(instance=menu_item, many=True)
    

    return Response(
        data= serializer.data,
        status=status.HTTP_200_OK
    )


    

   # response = {
   #     "message":"menu_item",
   #     "data": serializer.data
    #}

   # return Response(data=response,status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"]) 
@permission_classes([permissions.AllowAny])  
def add_item(request):
    data = request.data
    serializer = MenuItemSerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        response = {
            "message":"Item  Created",
            "data":request.data
        }

        return Response(data=response,status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


    
@api_view(http_method_names=["DELETE"])
def delete_product(request,menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    menu_item.delete()
    response = {
        "message":"menu item delected"
    }
    return Response(data=response,status=status.HTTP_200_OK)
