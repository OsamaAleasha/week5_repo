from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import engine
from models import users, skills, user_skills
from main import insert_user
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


@app.route("/api/auth/register", methods=["POST"])
def register():

    # Get JSON data
    data = request.get_json()

    # Extract fields
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    age = data.get("age")
    major = data.get("major")

    skill_list = data.get("skills", [])

    # Hash the password
    hashed_password = bcrypt.hash(password)

    # Store to DB
    user_id = insert_user(username, email, password, phone, age, major)
    














@app.route("/", methods=['GET'])
def index():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)