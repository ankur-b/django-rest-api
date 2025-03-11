from django.shortcuts import render
from django.http import JsonResponse

from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from watchlist_app.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from watchlist_app.throttling import ReviewCreateThrottle,ReviewListThrottle

from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,throttle_classes
from rest_framework import status
from rest_framework.exceptions import ValidationError

# Create your views here.
@api_view(['GET','PUT','DELETE'])
@throttle_classes([ReviewCreateThrottle])
@permission_classes([ReviewUserOrReadOnly])
def ReviewDetailFN(request,id):
    if request.method=='GET':
        try:
            review = Review.objects.get(id=id)
        except:
            return Response({'Error':' Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    if request.method=='PUT':
        review = Review.objects.get(id=id)
        serializer = ReviewSerializer(review,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE':
        movie = WatchList.objects.get(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@throttle_classes([ReviewListThrottle,AnonRateThrottle])
@permission_classes([IsAuthenticated])
def ReviewListFN(request,id):
    if request.method=='GET':
        reviews = Review.objects.filter(id=id)
        serializer = ReviewSerializer(reviews,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        print(id)
        watchlist = WatchList.objects.get(id=id)
        review_user = request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            if review_queryset.exists():
                raise ValidationError("You have already reviewed this movie")
            if watchlist.number_rating == 0:
                watchlist.avg_rating = serializer.validated_data['rating']
            else:
                watchlist.avg_rating = (watchlist.avg_rating+serializer.validated_data[rating])/2
            watchlist.number_rating = watchlist.number_rating + 1
            watchlist.save()
            serializer.save(watchlist=watchlist, review_user=review_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET','POST'])
@permission_classes([AdminOrReadOnly])
def WatchListFN(request):
    if request.method=='GET':
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET','PUT','DELETE'])
@permission_classes([AdminOrReadOnly])
def WatchDetail(request,id):
    if request.method=='GET':
        try:
            movie = WatchList.objects.get(id=id)
        except:
            return Response({'Error':' Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    if request.method=='PUT':
        movie = WatchList.objects.get(id=id)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE':
        movie = WatchList.objects.get(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@permission_classes([AdminOrReadOnly])
def StreamPlatformFN(request):
    if request.method=='GET':
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET','PUT','DELETE'])
@permission_classes([AdminOrReadOnly])
def StreamDetail(request,id):
    if request.method=='GET':
        try:
            movie = StreamPlatform.objects.get(id=id)
        except:
            return Response({'Error':' Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(movie)
        return Response(serializer.data)
    
    if request.method=='PUT':
        movie = StreamPlatform.objects.get(id=id)
        serializer = StreamPlatformSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE':
        movie = StreamPlatform.objects.get(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        