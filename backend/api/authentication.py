from api.models.users import User
from bson import ObjectId

class MongoEngineBackend:
    def authenticate(self, request, username=None, password=None):
        user = User.objects(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            if ObjectId.is_valid(user_id):
                return User.objects(id=ObjectId(user_id)).first()
        except:
            return None
