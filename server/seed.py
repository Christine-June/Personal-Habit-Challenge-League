from app import app, bcrypt
from models import db, User, Habit, Challenge, ChallengeParticipant, Comment
from datetime import datetime, timedelta

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create users
    user1 = User(
        username="JaneDoe",
        email="jane@example.com",
        password_hash=bcrypt.generate_password_hash("password").decode("utf-8"),
        avatar_url="https://static.vecteezy.com/system/resources/thumbnails/004/899/680/small/beautiful-blonde-woman-with-makeup-avatar-for-a-beauty-salon-illustration-in-the-cartoon-style-vector.jpg",
        bio="Building better habits every day!"
    )
    user2 = User(
        username="Alex",
        email="alex@example.com",
        password_hash=bcrypt.generate_password_hash("password").decode("utf-8"),
        avatar_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTx7sLJbdmCKh3Ko5fv9ahJsMGSZnIiRbz9Qg&s",
        bio="Runner and reader."
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create habits
    habit1 = Habit(name="Drink Water", description="8 glasses a day", user_id=user1.id)
    habit2 = Habit(name="Morning Run", description="5km run", user_id=user1.id)
    habit3 = Habit(name="Read Books", description="Read 10 pages", user_id=user2.id)

    db.session.add_all([habit1, habit2, habit3])
    db.session.commit()

    # Create challenges
    now = datetime.utcnow()
    challenge1 = Challenge(
        name="No Sugar Week",
        description="Avoid sugar for 7 days",
        created_by=user1.id,
        start_date=now,
        end_date=now + timedelta(days=7)
    )
    challenge2 = Challenge(
        name="Read Daily",
        description="Read 10 pages every day",
        created_by=user2.id,
        start_date=now,
        end_date=now + timedelta(days=30)
    )

    db.session.add_all([challenge1, challenge2])
    db.session.commit()

    # Add challenge participants
    cp1 = ChallengeParticipant(user_id=user1.id, challenge_id=challenge1.id)
    cp2 = ChallengeParticipant(user_id=user2.id, challenge_id=challenge2.id)
    db.session.add_all([cp1, cp2])
    db.session.commit()

    # Add comments to habits
    comment1 = Comment(content="Great habit!", user_id=user2.id, habit_id=habit1.id)
    comment2 = Comment(content="Keep it up!", user_id=user1.id, habit_id=habit3.id)

    # Add comments to challenges
    comment3 = Comment(content="I'm joining this challenge!", user_id=user2.id, challenge_id=challenge1.id)
    comment4 = Comment(content="Let's do this together!", user_id=user1.id, challenge_id=challenge2.id)

    db.session.add_all([comment1, comment2, comment3, comment4])
    db.session.commit()

    print("Database seeded with users, habits, challenges, and comments!")