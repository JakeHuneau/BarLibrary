import bcrypt
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from barlibrary.models.meta import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password_hash = Column(Text)
    permissions = Column(Integer, default=0)  # 0 can read, 1 can write, 2 can delete, 4 can change users

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False
