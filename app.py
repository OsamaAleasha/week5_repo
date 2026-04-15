from flask import Flask, render_template, request, redirect, url_for, jsonify
from app.db import engine
from app.models import users, skills, user_skills, courses
from app.main import insert_user, add_user_skills
from sqlalchemy import select
from passlib.hash import bcrypt
import jwt, datetime, os
from dotenv import load_dotenv

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")

def create_token(user_id):

    # Create a payload
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    # Create token
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_user_id_from_token():
    # Get authorization header
    auth_header = request.headers.get("Authorization")

    # Check if header exists
    if not auth_header:
        return None
    
    try:
        # Extract token
        token = auth_header.split(" ")[1]

        # Decode token
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data["user_id"]
    
    except:
        return None

def get_user_profile(user_id):
    with engine.connect() as conn:
        query = select(users).where(users.c.id == user_id)
        user = conn.execute(query).fetchone()

        skills_data = conn.execute(
            select(skills.c.name, user_skills.c.proficiency_level)
            .join(user_skills, skills.c.id == user_skills.c.skill_id)
            .where(user_skills.c.user_id == user_id)
        ).fetchall()

        return user, skills_data


@app.route("/api/auth/register", methods=["POST"])
def register():

    # Get request data
    data = request.get_json()

    # Extract fields
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    age = data.get("age")
    major = data.get("major")
    skill_ids = data.get("skills", [])

    # Hash the password
    hashed_password = bcrypt.hash(password[:72])

    # Store to DB
    try:
        with engine.begin() as conn:
            user_id = insert_user(conn, username, email, hashed_password, phone, age, major)

            add_user_skills(conn, user_id, skill_ids)

            token = create_token(user_id)

            return jsonify({
                "user": {
                    "id": user_id,
                    "username": username,
                    "email": email
                },
                "token": token
            }), 201
        
        
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/auth/login", methods=["POST"])
def login():

    # Get request data
    data = request.get_json()

    # Extract fields
    email = data.get("email")
    password = data.get("password")

    # Find user in DB
    with engine.connect() as conn:
        query = select(users).where(users.c.email == email)
        user = conn.execute(query).fetchone()

    # Check if user exists
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Verify password
    if not bcrypt.verify(password, user.password):
        return jsonify({"error": "Invalid password"}), 401
    
    # Generate token
    token = create_token(user.id)

    # Return response
    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "token": token
    })


@app.route("/api/users/me", methods=["GET"])
def get_me():

    # Get user id from token
    user_id = get_user_id_from_token()

    # Check authentication
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Get user and skills
    user, skills_data = get_user_profile(user_id)

    # return JSON response
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "age": user.age,
        "major": user.major,
        "skills": [
            {"name": s.name, "level": s.proficiency_level}
            for s in skills_data
        ]
    })


@app.route("/api/courses", methods=["GET"])
def get_courses():

    # Get query parameters
    q = request.args.get("q")
    skill = request.args.get("skill")
    instructor = request.args.get("instructor")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    # Pagination
    offset = (page - 1) * limit

    # Start query
    query = select(courses)

    # Search
    if q:
        query = query.where(courses.c.title.ilike(f"%{q}%"))

    # Filter by skill
    if skill:
        query = query.where(courses.c.skill_requirements.ilike(f"%{skill}%"))

    # Filter by instructor
    if instructor:
        query = query.where(courses.c.instructor.ilike(f"%{instructor}%"))

    # Pagination
    query = query.limit(limit).offset(offset)

    # Execute query
    with engine.connect() as conn:
        results = conn.execute(query).fetchall()

    # Convert to JSON
    return jsonify([
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "instructor": c.instructor
        }
        for c in results
    ])

@app.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):

    with engine.connect() as conn:
        query = select(courses).where(courses.c.id == id)
        course = conn.execute(query).fetchone()

    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "instructor": course.instructor,
        "skills": course.skill_requirements  # text for now
    })


@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/courses")
def courses_page():
    return render_template("courses.html")

@app.route("/course/<int:id>")
def course_details(id):
    return render_template("course-detail.html")

@app.route("/recommendations")
def recommendations():
    return render_template("recommendations.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)