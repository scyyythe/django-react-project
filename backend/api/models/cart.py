
from mongoengine import Document, ReferenceField, IntField, DateTimeField
from datetime import datetime
from .users import User  
from .artwork import Art

class AddToCart(Document):
    user = ReferenceField(User)  
    art = ReferenceField(Art) 
    quantity = IntField(min_value=1, default=1) 
    added_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'carts'}
