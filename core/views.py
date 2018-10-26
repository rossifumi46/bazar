from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Request, Tag
from .serializers import RequestSerializer, FeedbackSerializer, SellerSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import User, Category, Request
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance

# Create your views here.

def dashboard(request):
    return render(request, '')


@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def request_list(request):
    """
    List ...
    """
    if request.method == 'GET':
        category = request.GET['category']
        print(category)
        requests = Request.objects.filter(category__name__iexact=category)
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def request_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Request.objects.get(pk=pk)
    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RequestSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RequestSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def rate(request):
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(profile=request.user)
        serializer.save(sender=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def seller_list(request):
    if request.method == 'GET':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'PUT':
    #     serializer = RequestSerializer(snippet, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def seller_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        seller = Seller.objects.get(pk=pk)
    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(profile=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def category():
#     t = []
#     a = Category.objects.root_nodes()
#     for i in a:
#         Category.objects.filter(parent=i.id)
#             # b =
#
#
#
#
#
#         # d = {}
#         # q = Category.objects.filter(parent=i.id)
#         # t = []
#         # for j in q:
#         #     t.append(j.name)
#         # d[i.name] = t
#         # a.append(d)
#         # print(i.get_descendants(True))
#
#     # return a

# @api_view(['GET'])
def search(request):
    # query = request.GET.get('query', None)
    query = request
    tags = Tag.objects.annotate(distance=TrigramDistance('name', query), sim=TrigramSimilarity('name', query))\
                         .filter(distance__lt=0.9, sim__gt=0.2)\
                         .order_by('distance')[:5]
    return tags

from .models import Seller, Tag

def sellers():

    tags = Tag.objects.all()
    sellers = Seller.objects.filter(tag__in=tags).distinct()
    return sellers
    # cats = Category.objects.filter(id__in=[1,2])
    # requests = Request.objects.filter(category__in=cats)
    # return requests

