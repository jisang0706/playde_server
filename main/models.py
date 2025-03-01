from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as auth_user

# Create your models here.
class User(models.Model):
    token = models.TextField(default="", blank=True)
    password = models.TextField(default="", blank=True)
    name = models.CharField(max_length=100, default='', blank=True)
    nickname = models.CharField(max_length=100, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    age = models.IntegerField(default=0, blank=True)
    image = models.TextField(default="", blank=True)
    push_token = models.TextField(default="", blank=True)
    is_boss = models.BooleanField(default=False, blank=True)
    platform = models.IntegerField(default=0, blank=True)

class UserComment(models.Model):
    his_id = models.IntegerField()
    my_id = models.IntegerField()
    score = models.IntegerField(default=0, blank=True)
    comment = models.TextField(default="", blank=True)
    written_date = models.DateTimeField(auto_now_add=True)

class UserBlock(models.Model):
    user_id = models.IntegerField()
    user_id_blocked = models.IntegerField()

# class Meet(models.Model):
#     user_id = models.IntegerField()
#     latitude = models.FloatField(default=0.0, blank=True)
#     longitude = models.FloatField(default=0.0, blank=True)
#     area1 = models.CharField(max_length=20, default="", blank=True)
#     area2 = models.CharField(max_length=20, default="", blank=True)
#     area3 = models.CharField(max_length=20, default="", blank=True)

class Community(models.Model):
    user_id = models.IntegerField()
    content = models.TextField()
    tag = models.TextField(default="", blank=True)
    visit = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    temp = models.IntegerField(default=False, blank=True)

class CommunityImage(models.Model):
    board_id = models.IntegerField()
    order = models.IntegerField()
    image = models.TextField(default="", blank=True)

class CommunityLike(models.Model):
    user_id = models.IntegerField()
    board_id = models.IntegerField()

class Comment(models.Model):
    user_id = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    board_id = models.IntegerField()

class CommentReply(models.Model):
    user_id = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment_id = models.IntegerField()
    board_id = models.IntegerField(default=0, blank=True)

class UserWishlist(models.Model):
    user_id = models.IntegerField()
    game_id = models.IntegerField()

class UserFriend(models.Model):
    user_id = models.IntegerField()
    his_id = models.IntegerField()

class UserRecent(models.Model):
    user_id = models.IntegerField()
    his_id = models.IntegerField()

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
    content = models.TextField(default="", blank=True)
    table_cnt = models.IntegerField(default=0, blank=True)
    book_price = models.IntegerField(default=0, blank=True)

class CafeImage(models.Model):
    cafe_id = models.IntegerField()
    order = models.IntegerField()
    content_image = models.TextField(default="", blank=True)

class CafeWorktime(models.Model):
    cafe_id = models.IntegerField()
    weekday = models.IntegerField(default=0)
    open = models.TimeField(default=0)
    close = models.TimeField(default=0)

class CafeGame(models.Model):
    cafe_id = models.IntegerField()
    game_id = models.IntegerField()

class UserCafe(models.Model):
    user_id = models.IntegerField()
    cafe_id = models.IntegerField()

class UserPlayde(models.Model):
    user_id = models.IntegerField()
    game_id = models.IntegerField()

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
    kor_name = models.CharField(max_length=100)
    eng_name = models.CharField(max_length=100, default='', blank=True)
    age = models.IntegerField(default=0, blank=True)
    min_user = models.IntegerField(default=1, blank=True)
    max_user = models.IntegerField(default=1, blank=True)
    small_image = models.TextField(default="", blank=True)
    content = models.TextField(default="", blank=True)
    interest = models.IntegerField(default=0, blank=True)
    level = models.IntegerField(default=0, blank=True)

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
    content_image = models.TextField()

class GameComment(models.Model):
    game_id = models.IntegerField()
    user_id = models.IntegerField()
    content = models.TextField()

class UserMessage(models.Model):
    first_user_id = models.IntegerField()
    second_user_id = models.IntegerField()
    message_stack = models.IntegerField(default=0, blank=True)

def unique_rand():
    while True:
        room_token = auth_user.objects.make_random_password(length=8)
        if not Room.objects.filter(room_token=room_token).exists():
            return room_token

class Room(models.Model):
    room_token = models.CharField(max_length=8, unique=True, default=unique_rand)

class UserRoom(models.Model):
    room_id = models.IntegerField()
    user_id = models.IntegerField()

class CommunityReport(models.Model):
    board_id = models.IntegerField()
    user_id = models.IntegerField()
    content = models.TextField()
    kind = models.IntegerField()

class UserFriendRequest(models.Model):
    user_id = models.IntegerField()
    his_id = models.IntegerField()

class Funding(models.Model):
    name = models.TextField()
    content = models.TextField()
    user_id = models.IntegerField()
    goal = models.IntegerField()
    goal_date = models.DateField()
    upload_date = models.DateTimeField(auto_now_add=True)
    link = models.TextField()
    image = models.TextField(default="")

class FundingTag(models.Model):
    tag = models.TextField()
    funding_id = models.IntegerField()

class FundingImage(models.Model):
    funding_id = models.IntegerField()
    image = models.TextField()

class FundingNews(models.Model):
    funding_id = models.IntegerField()
    writer_id = models.IntegerField()
    title = models.TextField()
    image = models.TextField()
    content = models.TextField()
    written_date = models.DateTimeField(auto_now_add=True)

class FundingCommunity(models.Model):
    funding_id = models.IntegerField()
    content = models.TextField()
    writer_id = models.IntegerField()
    tag = models.TextField()
    written_date = models.DateTimeField(auto_now_add=True)
    parent_id = models.IntegerField(default=0, blank=True)
    secret = models.IntegerField(default=0, blank=True)

class FundingSchedule(models.Model):
    funding_id = models.IntegerField()
    writer_id = models.IntegerField()
    date = models.DateTimeField()
    content = models.TextField()

class FundingFav(models.Model):
    funding_id = models.IntegerField()
    user_id = models.IntegerField()