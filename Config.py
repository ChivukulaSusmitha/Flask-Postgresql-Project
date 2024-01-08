class Config:
    SECRET_KEY = 'your_secret_key'  # Change this to a random secret key
    SQLALCHEMY_DATABASE_URI = 'postgresql://your_postgres_user:your_postgres_password@localhost:5432/your_postgres_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
