from mongoengine import Document, StringField

class User(Document):
    username = StringField(required=True, unique=True, max_length=150)
    password = StringField(required=True)  # Store hashed password
    email = StringField(required=True, unique=True)
    first_name = StringField(max_length=100)
    last_name = StringField(max_length=100)

    def set_password(self, raw_password):
        """ Hash password before storing """
        import bcrypt
        self.password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, raw_password):
        """ Verify password """
        import bcrypt
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password.encode("utf-8"))
