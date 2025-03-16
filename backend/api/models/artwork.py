from mongoengine import Document, StringField, ReferenceField, FloatField, DateTimeField,IntField
from datetime import datetime
from api.models.users import User  # Import the User model

class Art(Document):
    title = StringField(max_length=100)
    artist = ReferenceField(User) 
    category = StringField(max_length=100)
    art_status = StringField(max_length=100)
    price = IntField()
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'artworks'}

    def save(self, *args, **kwargs):
        print("DEBUG: Saving Art Object =", self.to_json())  # Print before saving
        super().save(*args, **kwargs)
        print("DEBUG: Art Saved Successfully")  # Confirm save
