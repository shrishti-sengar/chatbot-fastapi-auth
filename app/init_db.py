# app/init_db.py
from app import models, database
import sys

def main():
    print("Initializing DB schemas...")
    models.Base.metadata.create_all(bind=database.engine)
    print("DB initialization complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
