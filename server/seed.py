from app import app, db
from models import User, Habit, Challenge
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

with app.app_context():
    print("🌱 Seeding Users...")
    users = []
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash="password123"
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()  # commit USERS so they get IDs

    print("🌱 Seeding Habits...")
    habits = []
    for _ in range(3):
        habit = Habit(
            name=fake.word(),
            description=fake.sentence(),
            user_id=random.choice(users).id  # assign a valid user_id
        )
        db.session.add(habit)
        habits.append(habit)
    db.session.commit()  # commit HABITS if you use them later

    print("🌱 Seeding Challenges...")
    challenges = []
    for _ in range(2):
        start = date.today()
        end = start + timedelta(days=7)
        challenge = Challenge(
            name=fake.word(),
            description=fake.sentence(),
            created_by=random.choice(users).id,
            start_date=start,
            end_date=end
        )
        db.session.add(challenge)
        challenges.append(challenge)
    db.session.commit()

    print("✅ Done seeding!")
