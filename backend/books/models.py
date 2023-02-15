from django.db import models

# Create your models here.
class Book(models.Model):
    """
    책 정보 모델
    - title        : 책 제목
    - desc         : 책 부제목
    - author       : 저자
    - publisher    : 출판사
    - price        : 가격
    - isbn         : isbn13
    - cover        : 표지 이미지 링크
    - publish_date : 출판일
    - toc          : 목차
    - desc_detail  : 소개 이미지, 글
    - page_count   : 쪽수
    """
    title = models.CharField(max_length=100)
    decs = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    price = models.FloatField()
    isbn = models.CharField(max_length=15, unique=True)
    cover = models.TextField()
    publish_date = models.DateField()
    toc = models.TextField()
    desc_detail = models.TextField()
    page_count = models.IntegerField()
    category_number = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.title}-{self.decs}'

class BookRank(models.Model):
    """
    책 랭크 제공
    - rank : 베스트셀러 순위
    - title : 베스트셀러 책 제목
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, to_field='isbn')
    rank = models.IntegerField()
    isbn = models.CharField(max_length=15, unique=True)
    site = models.CharField(max_length=4)
    period = models.CharField(max_length=4)
    create_date = models.DateField()
    rank_date = models.CharField(max_length=8)

    def __str__(self):
        return f'{self.book}-{self.rank}-{self.isbn}-{self.book.title}'

    
