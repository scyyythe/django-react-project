from mongoengine import Document, StringField, ReferenceField, IntField, DateTimeField
from datetime import datetime
from .users import User  
from .artwork import Art  


class Comment(Document):
    content = StringField()
    user = ReferenceField(User)  
    art = ReferenceField(Art) 
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'comments'}


class Like(Document):
    user = ReferenceField(User)  
    art = ReferenceField(Art) 
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'likes'}

