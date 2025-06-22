from app import app, db
from models import User, Habit, Challenge, ChallengeParticipant, ChallengeEntry
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

def generate_avatar(username):
    return f"https://api.dicebear.com/7.x/thumbs/svg?seed={username}"

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

    print("🌱 Seeding Challenge Participants...")
    participants = []
    for user in users:
        challenge = random.choice(challenges)
        existing = ChallengeParticipant.query.filter_by(user_id=user.id, challenge_id=challenge.id).first()
        if not existing:
            participant = ChallengeParticipant(user_id=user.id, challenge_id=challenge.id)
            db.session.add(participant)
            participants.append(participant)
    db.session.commit()

    print("🌱 Seeding Challenge Entries...")
    for participant in participants:
        for day in range(3):
         entry = ChallengeEntry(
            user_id=participant.user_id,
            challenge_id=participant.challenge_id,
            progress=random.choice(["completed", "skipped", "partial"]),
             date=date.today() - timedelta(days=day),
            )
    db.session.add(entry)
    db.session.commit()

    print("✅ Done seeding!")
