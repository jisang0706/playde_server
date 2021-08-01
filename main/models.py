from django.db import models

# Create your models here.
class User(models.Model):
    token = models.IntegerField()
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    age = models.IntegerField(default=0, blank=True)
    location = models.CharField(max_length=100, default="", blank=True)
    address = models.CharField(max_length=100, default="", blank=True)
    big_image = models.ImageField(upload_to='userimages/', default="", blank=True)
    small_image = models.ImageField(upload_to='userimages/', default="", blank=True)
    is_boss = models.BooleanField(default=False, blank=True)


class UserComment(models.Model):
    his_id = models.IntegerField()
    my_id = models.IntegerField()
    score = models.IntegerField(default=0, blank=True)
    comment = models.TextField(default="", blank=True)
    written_date = models.DateTimeField(auto_now=True)


class UserBlock(models.Model):
    user_id = models.IntegerField()
    user_id_blocked = models.IntegerField()


class Meet(models.Model):
    user_id = models.IntegerField()


class UserWishlist(models.Model):
    user_id = models.IntegerField()
    game_id = models.IntegerField()


class Boss(models.Model):
    boss_id = models.IntegerField()
    cafe_id = models.IntegerField()


class Cafe(models.Model):
    boss_id = models.IntegerField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=100)
    big_image = models.ImageField(upload_to='cafeimages/', default="", blank=True)
    small_image = models.ImageField(upload_to='cafeimages/', default="", blank=True)
    intro = models.TextField(default="", blank=True)


class CafeWorktime(models.Model):
    cafe_id = models.IntegerField()
    weekday_open = models.CharField(max_length=5)
    weekday_close = models.CharField(max_length=5)
    saturday_open = models.CharField(max_length=5)
    saturday_close = models.CharField(max_length=5)
    sunday_open = models.CharField(max_length=5)
    sunday_close = models.CharField(max_length=5)


class CafeGame(models.Model):
    cafe_id = models.IntegerField()
    game_id = models.IntegerField()


class UserCafe(models.Model):
    user_id = models.IntegerField()
    cafe_id = models.IntegerField()


class CafeBook(models.Model):
    user_id = models.IntegerField()
    cafe_id = models.IntegerField()
    begin = models.CharField(max_length=5)
    end = models.CharField(max_length=5)
    count_people = models.IntegerField(default=1, blank=True)
    question = models.TextField(default="", blank=True)


class CafeBookWantGame(models.Model):
    book_id = models.IntegerField()
    game_id = models.IntegerField()


class CafeSales(models.Model):
    cafe_id = models.IntegerField()
    sales = models.IntegerField()
    sales_date = models.DateTimeField(auto_now_add=True)


class Game(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0, blank=True)
    min_user = models.IntegerField(default=1, blank=True)
    max_user = models.IntegerField(default=1, blank=True)
    small_image = models.ImageField(upload_to='gameimages/', default="", blank=True)
    content = models.TextField(default="", blank=True)
    exist = models.BooleanField(default=True, blank=True)
    interest = models.IntegerField(default=0, blank=True)


"""더이상 사용하지 않는 테이블"""


# class Tutorial(models.Model):
#     game_id = models.IntegerField()
#     link = models.TextField()

# class TutorialTimeLine(models.Model):
#     tutorial_id = models.IntegerField()
#     number = models.IntegerField()
#     check_point = models.CharField(max_length=20)
#     thumbnail = models.ImageField(upload_to='thumbnails/', default="", blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=10)


class GameGenre(models.Model):
    game_id = models.IntegerField()
    genre_id = models.IntegerField()


class PlaySystem(models.Model):
    name = models.CharField(max_length=15)


class GamePlaySystem(models.Model):
    game_id = models.IntegerField()
    playsystem_id = models.IntegerField()


class GameImage(models.Model):
    game_id = models.IntegerField()
    order = models.IntegerField()
    content_image = models.ImageField(upload_to='gamecontentimages/', default="", blank=True)


class GameComment(models.Model):
    game_id = models.IntegerField()
    user_id = models.IntegerField()
    content = models.TextField()


class Funding(models.Model):
    game_id = models.IntegerField()
    user_id = models.IntegerField()
    now_amount = models.IntegerField()
    target_amount = models.IntegerField(default=0, blank=True)


class FundingSchedule(models.Model):
    funding_id = models.IntegerField()
    schedule = models.DateTimeField()
    content = models.TextField()