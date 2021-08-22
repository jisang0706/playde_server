from main.models import User

def exist_nickname(nickname):
    return bool(len(User.objects.filter(nickname=nickname)))