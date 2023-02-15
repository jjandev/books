from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from .models import Book, BookRank
from .serializers import BookSerializer, RankSerializer

from datetime import datetime, timedelta, timezone
import pytz


class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    def get_object(self, pk):
        book = get_object_or_404(Book, pk=pk)
        return book

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def patch(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookRankListView(APIView):
    def get(self, request):
        # /api/v1/ranks?categoryNumber=001&sellerId=Y&period=D&ymw=20230215
        category_number = request.GET.get('categoryNumber', '001')
        site = request.GET.get('sellerId', 'Y') # 판매자 식별자 Y:yes24 / K:교보 / A:Aladin
        
        # 기본적으로 첫 화면은 Daily 어제날짜
        period = request.GET.get('period', 'D') # D:daily, M:Monthly, Y:Yearly, W:Weekly
        KST = pytz.timezone('Asia/Seoul')
        time = (datetime.now(KST).date()- timedelta(1)).strftime("%Y%m%d")
    
        if period == 'W':
            tmp = datetime.now(KST).date().weekday()
            time = time[:6]+str(tmp)

        ymw = request.GET.get('ymw', time)
        
        if period == 'M': ymw = ymw[:6]
        elif period == 'Y': ymw = ymw[:4]
        elif period == 'W': ymw
        q=Q()
        q &= Q(book__category_number=category_number)
        q &= Q(site=site)
        q &= Q(period=period)
        q &= Q(rank_date__exact=ymw)


        ranks = BookRank.objects.filter(q)
        serializer = RankSerializer(ranks, many=True)


        return Response(serializer.data)

    def post(self, request):
        serializer = RankSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)