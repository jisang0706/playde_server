from django.contrib import admin

# Register your models here.
from .models import User, UserComment, UserBlock, Meet, UserWishlist, Boss, Cafe, CafeWorktime, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent

admin.site.register(User)
admin.site.register(UserComment)
admin.site.register(UserBlock)
admin.site.register(Meet)
admin.site.register(UserWishlist)
admin.site.register(Boss)
admin.site.register(Cafe)
admin.site.register(CafeWorktime)
admin.site.register(CafeGame)
admin.site.register(UserCafe)
admin.site.register(CafeBook)
admin.site.register(CafeBookWantGame)
admin.site.register(CafeSales)
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(GameGenre)
admin.site.register(PlaySystem)
admin.site.register(GamePlaySystem)
admin.site.register(GameImage)
admin.site.register(GameComment)
admin.site.register(Funding)
admin.site.register(FundingSchedule)
admin.site.register(UserFriend)
admin.site.register(UserRecent)