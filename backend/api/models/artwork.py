from mongoengine import Document, StringField, IntField, ImageField, DateTimeField, ReferenceField
from datetime import datetime
from .users import User

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
