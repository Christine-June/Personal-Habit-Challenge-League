from app import app, db
from models import User, Habit, Challenge, HabitEntry
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()
with app.app_context():
    print("🧨 Dropping and recreating all tables...")
    db.drop_all()
    db.create_all()
    print("✅ Tables recreated successfully!")

with app.app_context():
    print("🧨 Dropping and recreating all tables...")
    db.drop_all()
    db.create_all()

    print("🌱 Seeding Users...")
    users = []
    for _ in range(5):
        username = fake.user_name()
        user = User(
            username=username,
            email=fake.email(),
            avatar_url=generate_avatar(username)  # Avatar added here
        )
        user.set_password("password123")  # Uses real hashing
        db.session.add(user)
        users.append(user)
    db.session.commit()

    print("🌱 Seeding Habits...")
    habits = []
    for _ in range(3):
        habit = Habit(
        name=fake.word(),
        description=fake.sentence(),
        frequency="daily",
        user_id=random.choice(users).id  # ✅ add this
    )
    db.session.add(habit)
    habits.append(habit)
    db.session.commit()
    print("🌱 Seeding Challenges...")
    challenges = []
    for _ in range(2):
        start = date.today()
        end = start + timedelta(days=7)
        challenge = Challenge(
            name=fake.catch_phrase(),  
            description=fake.text(max_nb_chars=80),
            created_by=random.choice(users).id,
            start_date=start,
            end_date=end
        )
        db.session.add(challenge)
        challenges.append(challenge)
    db.session.commit()
    print("🌱 Seeding Habit Entries...")
    entries = []
    for user in users:
        for habit in habits:
            entry = HabitEntry(
                user_id=user.id,
                habit_id=habit.id,
                progress=random.choice(['completed', 'skipped', 'partial']),
                notes=fake.sentence(),
                date=date.today()
            )
            db.session.add(entry)
            entries.append(entry)
    db.session.commit()
    print("✅ Done seeding Habit Entries!")
    print("✅ Done seeding!")
