from django.contrib import admin

# Register your models here.
from .models import User, UserComment, UserBlock, UserWishlist, Boss, Cafe, CafeWorktime, CafeGame, UserCafe,\
    CafeBook, CafeBookWantGame, CafeSales, CafeImage, Game, Genre, GameGenre, PlaySystem, GamePlaySystem, GameImage, GameComment,\
    Funding, FundingSchedule, UserFriend, UserRecent, UserPlayde, Community, CommunityLike, Comment, CommentReply

admin.site.register(User)
admin.site.register(UserComment)
admin.site.register(UserBlock)
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
admin.site.register(UserPlayde)
admin.site.register(Community)
admin.site.register(CommunityLike)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(CafeImage)