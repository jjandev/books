from django.db import models
import uuid
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
    isbn = models.CharField(max_length=15, primary_key=True)
    title = models.CharField(max_length=128)
    # decs = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=256)
    publisher = models.CharField(max_length=256)
    price = models.IntegerField(null=True)
    cover = models.TextField(null=True)
    toc = models.TextField(null=True)
    category = models.CharField(max_length=64, null=True)
    detail = models.TextField(null=True)
    publish_date = models.DateField(null=True)
    create_date = models.DateTimeField(null=True)


    def __str__(self):
        return f'{self.title}-{self.decs}'

class BookRank(models.Model):
    """
    책 랭크 제공
    - rank : 베스트셀러 순위
    - title : 베스트셀러 책 제목
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rank = models.IntegerField()
    isbn = models.CharField(max_length=15, unique=True)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE, to_field='isbn')
    review_count = models.IntegerField()
    review_rating = models.DecimalField(max_digits=4, decimal_places=2)
    site = models.CharField(max_length=1)
    period = models.CharField(max_length=11)
    rank_date = models.CharField(max_length=8)
    create_date = models.DateTimeField(null=True)


    def __str__(self):
        return f'{self.book}-{self.rank}-{self.isbn}-{self.book.title}'

