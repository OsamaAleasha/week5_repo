from app.db import engine
from app.models import metadata, users, skills, user_skills, courses, course_vectors
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

metadata.create_all(engine)


def insert_user(conn, username, email, password, phone, age, major):
    query = insert(users).values(
        username = username,
        email = email,
        password = password,
        phone = phone,
        age = age,
        major = major
    )
       
    result = conn.execute(query)

    return result.inserted_primary_key[0]


def add_user_skills(conn, user_id, skill_ids):
    for skill_id in skill_ids:
        conn.execute(
            insert(user_skills).values(
                user_id=user_id,
                skill_id=skill_id,
                proficiency_level=1
            )
        )