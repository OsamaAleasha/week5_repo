from db import engine
from models import metadata, users, skills, user_skills, courses, course_vectors
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

metadata.create_all(engine)

def insert_user(username, email, password, phone, age, major):
    with engine.connect() as conn:
        try:
            query = insert(users).values(
                username = username,
                email = email,
                password = password,
                phone = phone,
                age = age,
                major = major
            )
            result = conn.execute(query)
            conn.commit()

            return result.inserted_primary_key[0]
        
        
        except SQLAlchemyError as e:
            conn.rollback()
            raise