from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField,EmbeddedDocument
from datetime import datetime
from .users import User  # Assuming User is a MongoEngine document

class Art(Document):
    title = StringField(max_length=100)
    artist = ReferenceField(User) 
    category = StringField(max_length=100)
    art_status = StringField(max_length=100)
    price = IntField()
    description = StringField(required=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'art'}

    def save(self, *args, **kwargs):
        print("DEBUG: Saving Art Object =", self.to_json())  # Print before saving
        super().save(*args, **kwargs)
        print("DEBUG: Art Saved Successfully")  # Confirm save
        
