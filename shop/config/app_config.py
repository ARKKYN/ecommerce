import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "test":
    DATABASE_URL = "sqlite:///./test.db"
else:
    DATABASE_URL = "sqlite:///./database.db"

