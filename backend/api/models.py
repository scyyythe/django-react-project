from mongoengine import Document, StringField, IntField, ImageField, DateTimeField, ReferenceField, EmailField
import bcrypt
from datetime import datetime


class User(Document):
    username = StringField(max_length=150, unique=True, required=True)
    password = StringField(required=True)
    email = EmailField(unique=True, required=True)
    first_name = StringField(max_length=100, required=False)
    last_name = StringField(max_length=100, required=False)
    role = StringField(max_length=100, default="User")
    user_status = StringField(max_length=100, default="Active")
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        """Hash and set password."""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check password hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Art(Document):
    title = StringField(max_length=100)
    artist = ReferenceField(User) 
    category = StringField(max_length=100)
    art_status = StringField(max_length=100)
    price = IntField()
    description = StringField()
    # image = ImageField(upload_to="artworks/") 
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)


    meta = {
        'collection': 'artworks'  
    }

    def __str__(self):
        return self.title

