"""Database configuration and models for the school activities management system."""

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pathlib import Path

# Use SQLite database stored in the workspace
DB_PATH = Path(__file__).parent.parent / "school_activities.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Association table for many-to-many relationship between activities and participants
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('email', String, ForeignKey('participants.email'), primary_key=True)
)


class Activity(Base):
    """Activity model representing an extracurricular activity."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)

    # Relationship to participants (many-to-many)
    participants = relationship(
        "Participant",
        secondary=activity_participants,
        back_populates="activities"
    )


class Participant(Base):
    """Participant model representing a student signed up for activities."""
    __tablename__ = "participants"

    email = Column(String, primary_key=True, index=True)

    # Relationship to activities (many-to-many)
    activities = relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )


def init_db():
    """Initialize the database with schema and seed data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Seed initial activities if database is empty
    db = SessionLocal()
    try:
        if db.query(Activity).count() == 0:
            initial_activities = [
                Activity(
                    name="Chess Club",
                    description="Learn strategies and compete in chess tournaments",
                    schedule="Fridays, 3:30 PM - 5:00 PM",
                    max_participants=12,
                ),
                Activity(
                    name="Programming Class",
                    description="Learn programming fundamentals and build software projects",
                    schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                    max_participants=20,
                ),
                Activity(
                    name="Gym Class",
                    description="Physical education and sports activities",
                    schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                    max_participants=30,
                ),
                Activity(
                    name="Soccer Team",
                    description="Join the school soccer team and compete in matches",
                    schedule="Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                    max_participants=22,
                ),
                Activity(
                    name="Basketball Team",
                    description="Practice and play basketball with the school team",
                    schedule="Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                    max_participants=15,
                ),
                Activity(
                    name="Art Club",
                    description="Explore your creativity through painting and drawing",
                    schedule="Thursdays, 3:30 PM - 5:00 PM",
                    max_participants=15,
                ),
                Activity(
                    name="Drama Club",
                    description="Act, direct, and produce plays and performances",
                    schedule="Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                    max_participants=20,
                ),
                Activity(
                    name="Math Club",
                    description="Solve challenging problems and participate in math competitions",
                    schedule="Tuesdays, 3:30 PM - 4:30 PM",
                    max_participants=10,
                ),
                Activity(
                    name="Debate Team",
                    description="Develop public speaking and argumentation skills",
                    schedule="Fridays, 4:00 PM - 5:30 PM",
                    max_participants=12,
                ),
            ]

            db.add_all(initial_activities)
            db.commit()

            # Add initial participants to match the original in-memory data
            initial_participants = [
                ("michael@mergington.edu", ["Chess Club"]),
                ("daniel@mergington.edu", ["Chess Club"]),
                ("emma@mergington.edu", ["Programming Class"]),
                ("sophia@mergington.edu", ["Programming Class"]),
                ("john@mergington.edu", ["Gym Class"]),
                ("olivia@mergington.edu", ["Gym Class"]),
                ("liam@mergington.edu", ["Soccer Team"]),
                ("noah@mergington.edu", ["Soccer Team"]),
                ("ava@mergington.edu", ["Basketball Team"]),
                ("mia@mergington.edu", ["Basketball Team"]),
                ("amelia@mergington.edu", ["Art Club"]),
                ("harper@mergington.edu", ["Art Club"]),
                ("ella@mergington.edu", ["Drama Club"]),
                ("scarlett@mergington.edu", ["Drama Club"]),
                ("james@mergington.edu", ["Math Club"]),
                ("benjamin@mergington.edu", ["Math Club"]),
                ("charlotte@mergington.edu", ["Debate Team"]),
                ("henry@mergington.edu", ["Debate Team"]),
            ]

            for email, activity_names in initial_participants:
                participant = Participant(email=email)
                for activity_name in activity_names:
                    activity = db.query(Activity).filter(
                        Activity.name == activity_name
                    ).first()
                    if activity:
                        participant.activities.append(activity)
                db.add(participant)

            db.commit()
    finally:
        db.close()


def get_db():
    """Dependency for getting a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
