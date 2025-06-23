from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import user_pb2

Base = declarative_base()

class UserModel(Base):
    __tablename__='users'
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String, default='')
    disabled = Column(Boolean, default=False)
    username = Column(String, default='')

class PostgresUserStore:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, name, email, password):
        from uuid import uuid4
        session = self.Session()
        if session.query(UserModel).filter_by(email=email).first():
            session.close()
            raise ValueError('Email already exists')
        user = UserModel(id=str(uuid4()), name=name, email=email, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user_pb2.User(id=user.id, name=user.name, email=user.email, password=user.password)
        
    def get_user(self, user_id):
        session = self.Session()
        user = session.query(UserModel).get(user_id)
        session.close()
        if user:
            return user_pb2.User(id=user.id, name=user.name, email=user.email, password=user.password)
        return None
    
    def get_user_email(self, email):
        print('get_user_email is called, email:', email)
        session = self.Session()
        user = session.query(UserModel).filter_by(email=email).first()
        session.close()
        if user:
            print("user is found, id:", user.id)
            return user_pb2.User(id=user.id, name=user.name, email=user.email, password=user.password)
        return None

    def list_users(self, skip:int = 0, limit: int = 10):
        session=self.Session()
        users = session.query(UserModel).offset(skip).limit(limit=limit).all()
        session.close()
        return [user_pb2.User(id=u.id, name=u.name, email=u.email) for u in users]
    
    def total_users(self):
        session=self.Session()
        total = session.query(UserModel).count()
        session.close()
        return total

    def update_user(self, user_id, name, email):
        session = self.Session()
        user = session.query(UserModel).get(user_id)
        if not user:
            session.close()
            return None
        user.name = name
        user.email = email
        session.commit()
        session.refresh(user)
        session.close()
        return user_pb2.User(id=user.id, name=user.name, email=user.email)

    def delete_user(self, user_id):
        session = self.Session()
        user = session.query(UserModel).get(user_id)
        if not user:
            session.close()
            return False
        # session.delete(user)
        user.disabled = True
        session.commit()
        session.refresh(user)
        session.close()
        return True

    
