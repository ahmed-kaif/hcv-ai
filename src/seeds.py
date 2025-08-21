from sqlalchemy.orm import Session
from src import models, database, utils
from src.core.config import Config

db: Session = database.SessionLocal()

# Create admin user
def create_admin():
    admin_email = Config.DEFAULT_ADMIN_EMAIL
    admin_password = Config.DEFAULT_ADMIN_PASSWORD
    existing_admin = db.query(models.User).filter(models.User.email == admin_email).first()

    if not existing_admin:
        hashed_password = utils.hash_password(admin_password)
        admin = models.User(
            name="Admin User",
            email=admin_email,
            password=hashed_password,
            is_admin=True,
            auth_provider="email"
        )
        db.add(admin)
        print("✅ Admin user created.")
    else:
        print("Admin user already exists.")

# Seed results
def seed_results():
    existing = db.query(models.Result).count()
    if existing == 0:
        results = [
            models.Result(id=0, label="Blood Donor"),
            models.Result(id=1, label="Suspect Blood Donor"),
            models.Result(id=2, label="Hepatitis"),
            models.Result(id=3, label="Fibrosis"),
            models.Result(id=4, label="Cirrhosis"),
        ]
        db.add_all(results)
        db.commit()
        print("✅ Results seeded.")
        results = [
            models.Result(id=0, label="Negative"),
            models.Result(id=1, label="Hepatitis"),
            models.Result(id=2, label="Fibrosis"),
            models.Result(id=3, label="Cirrhosis"),
        ]
        db.add_all(results)
        print("✅ Results seeded.")
    else:
        print("Results already seeded.")


# Run seeding
def run():
    create_admin()
    seed_results()
    db.commit()
    db.close()

if __name__ == "__main__":
    run()
