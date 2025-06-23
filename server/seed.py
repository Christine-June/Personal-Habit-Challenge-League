from app import app
from models import db, User, Habit, UserHabit, HabitEntry, Challenge, ChallengeParticipant, ChallengeEntry
from datetime import date, timedelta
from faker import Faker
import random

fake = Faker()

with app.app_context():
    print("🧨 Dropping and creating all tables...")
    db.drop_all()
    db.create_all()

    print("👤 Seeding users...")
    users = []
    for _ in range(30):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            avatar_url=fake.image_url(width=100, height=100)
        )
        user.set_password("password123")
        db.session.add(user)
        users.append(user)
    db.session.commit()
    print(f"✅ Seeded {len(users)} users.")

    print("🔥 Seeding habits...")
    frequencies = ["daily", "weekly", "monthly"]
    habits = []
    for _ in range(40):
        habit = Habit(
            name=fake.word().capitalize(),
            description=fake.sentence(),
            frequency=random.choice(frequencies),
            user=random.choice(users)
        )
        db.session.add(habit)
        habits.append(habit)
    db.session.commit()
    print(f"✅ Seeded {len(habits)} habits.")
    habits = Habit.query.all()  # 🧠 Re-fetch to rebind session

    print("📈 Seeding habit entries...")
    unique_keys = set()
    habit_entries = []
    attempts = 0
    while len(habit_entries) < 100 and attempts < 500:
        habit = random.choice(habits)
        user_id = habit.user_id
        habit_id = habit.id
        entry_date = date.today() - timedelta(days=random.randint(0, 30))
        key = (user_id, habit_id, entry_date)

        if key not in unique_keys:
            entry = HabitEntry(
                user_id=user_id,
                habit_id=habit_id,
                progress=random.choice(['completed', 'skipped', 'partial']),
                notes=fake.sentence(),
                date=entry_date
            )
            habit_entries.append(entry)
            unique_keys.add(key)
        attempts += 1

    db.session.add_all(habit_entries)
    db.session.commit()
    print(f"✅ Seeded {len(habit_entries)} habit entries.")

    print("🏆 Seeding challenges...")
    challenges = []
    for _ in range(10):
        creator = random.choice(users)
        start = date.today() - timedelta(days=random.randint(5, 20))
        end = start + timedelta(days=random.randint(7, 30))
        challenge = Challenge(
            name=fake.catch_phrase(),
            description=fake.text(100),
            created_by=creator.id,
            start_date=start,
            end_date=end
        )
        db.session.add(challenge)
        challenges.append(challenge)
    db.session.commit()
    print(f"✅ Seeded {len(challenges)} challenges.")

    print("🤝 Seeding challenge participants...")
    for challenge in challenges:
        participants = random.sample(users, k=random.randint(5, 15))
        for user in participants:
            cp = ChallengeParticipant(
                challenge_id=challenge.id,
                user_id=user.id,
                reason=fake.sentence()
            )
            db.session.add(cp)
    db.session.commit()
    print("✅ Seeded challenge participants.")

    print("📆 Seeding challenge entries...")
    challenge_entries = []
    used_keys = set()
    attempts = 0
    while len(challenge_entries) < 50 and attempts < 300:
        challenge = random.choice(challenges)
        user = random.choice(users)
        entry_date = date.today() - timedelta(days=random.randint(0, 20))
        key = (user.id, challenge.id, entry_date)

        if key not in used_keys:
            participant = ChallengeParticipant.query.filter_by(user_id=user.id, challenge_id=challenge.id).first()
            if participant:
                entry = ChallengeEntry(
                    user_id=user.id,
                    challenge_id=challenge.id,
                    progress=random.choice(['completed', 'in-progress', 'skipped']),
                    date=entry_date
                )
                challenge_entries.append(entry)
                used_keys.add(key)
        attempts += 1

    db.session.add_all(challenge_entries)
    db.session.commit()
    print(f"✅ Seeded {len(challenge_entries)} challenge entries.")

    print("🎉 Done seeding your Personal Habit Challenge League data!")
