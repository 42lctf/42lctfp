import os
from dotenv import load_dotenv

load_dotenv()

# We can use 'openssl rand -hex 32'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes

ALGORITHM = "HS256"
