from app.main import get_password_hash
from app.main import verify_password

password = "1234"
hashed_password = get_password_hash(password)
verify_password(password, hashed_password)

