from fastapi import FastAPI, HTTPException, Depends, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator, Field
from typing import Optional, Annotated
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from contextlib import asynccontextmanager
# from database import get_db, create_tables
from database.database import get_db, create_tables
from datetime import datetime
import sqlite3

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn_generator = get_db()
    conn = next(conn_generator)
    create_tables(conn)
    yield

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(lifespan=lifespan)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# SECRET_KEY = "f88d1f37937f71bf812a4b7b0b813863356224690b17928ab7c641559319d9b4"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = {
#     "johndoe": {
#         "username": "ranjit",
#         "full_name": "Ranjit Marathay",
#         "email": "rmarathay@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
#     "ranjit": {
#         "username": "ranjit",
#         "full_name": "Ranjit Marathay",
#         "email": "rmarathay@example.com",
#         "hashed_password": "fakehashedsecret3",
#         "disabled": False,
#     }
# }

# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: Optional[str] = None

# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     password: str
#     disabled: Optional[bool] = None


# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str
#     full_name: str
#     def hash_password(self):
#         global pwd_context  # Ensure you have access to the CryptContext instance
#         self.password = pwd_context.hash(self.password)


# class UserInDB(User):
#     hashed_password: str
#     def __hash__(self):
#         # Typically, you might hash on immutable and unique attributes like username
#         return hash((self.username,))


class Property(BaseModel):
  title: str
  address: str
  unit: Optional[str] = None
  property_value: int
  year_built: str
  bed: int
  bath: int
  sleeps: int
  sqft: int
  lot_size: int
  description: str
  image_url: str
  url: str
  last_updated: datetime = Field(default_factory=datetime.now)
  nightly_rate: float
  property_type: str

class UpdateProperty(BaseModel):
    title: Optional[str] = None
    address: Optional[str] = None
    unit: Optional[str] = None
    property_value: Optional[int] = None
    year_built: Optional[str] = None
    bed: Optional[int] = None
    bath: Optional[int] = None
    sleeps: Optional[int] = None
    sqft: Optional[int] = None
    lot_size: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    url: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.now)
    nightly_rate: Optional[int] = None
    property_type: Optional[str] = None

@field_validator('year_built', 'price', 'sqft', 'lot_size', 'bed', 'bath', 'sleeps')
def check_positive(cls, v):
    if v < 0:
        raise ValueError('must be positive')
    return v

@field_validator('last_updated')
def check_date_format(cls, v):
    # Assuming ISO 8601 format: YYYY-MM-DDTHH:MM:SS
    try:
        datetime.fromisoformat(v)
    except ValueError:
        raise ValueError('last_updated must be a valid ISO 8601 date-time string')
    return v

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)

# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user


# def get_user(db, username: str):
#     if username in db.keys():
#         user_dict = db[username]
#         return UserInDB(**user_dict)

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")

# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user

# @app.post("/register")
# async def register_user(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
#     cursor = db.cursor()
#     # Check if user with the same email already exists
#     cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', (user.email,))
#     existing_user = cursor.fetchone()[0]

#     if existing_user > 0:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Hash the password before storing it in the database
#     hashed_password = pwd_context.hash(user.password)

#     # Insert the new user into the database
#     try:
#         cursor.execute('''
#             INSERT INTO users(username, email, password) VALUES (?, ?, ?)
#         ''', (user.username, user.email, hashed_password))
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

#     return {"message": "User created successfully", "data": user.model_dump(excludes={"password"})}


# @app.get("/")
# def read_root(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"message": "Hello World"}


@app.get("/hello")
def hello():
    return {"message": "Hello World"}

@app.get("/property", summary="Retrieve all properties", description="Returns a list of all properties in the database with detailed information.")
def get_properties(db: sqlite3.Connection = Depends(get_db)):
    """Fetches all properties from the database."""
    cursor = db.cursor()
    
    cursor.execute(f"""
        SELECT * FROM properties
    """)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    return data

@app.get("/property/{property_id}", summary="Retrieve a single property", description="Returns detailed information about a property specified by its ID.")
def get_property(property_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Fetches a single property by its ID from the database."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))

    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Property not found")
    else:
        columns = [desc[0] for desc in cursor.description]
        data = dict(zip(columns, row))
        return data
    

@app.post("/property", summary="Create a new property", description="Adds a new property to the database and returns the created property details.")
def create_property(property: Property, db: sqlite3.Connection = Depends(get_db)):
    """Creates a new property with the provided details. Inputs are validated for greater than 0 values."""
    cursor = db.cursor()
    try: 
        cursor.execute("""
            INSERT INTO properties (
                title, address, unit, property_value, year_built, bed, bath, sleeps, sqft, lot_size,
                description, image_url, url, last_updated, nightly_rate, property_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            property.title, property.address, property.unit, property.property_value, property.year_built,
            property.bed, property.bath, property.sleeps, property.sqft, property.lot_size,
            property.description, property.image_url, property.url, property.last_updated,
            property.nightly_rate, property.property_type
        ))
        db.commit()
        return {"message": "Property created", "property": property}
    except sqlite3.IntegrityError as ie:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {ie}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@app.put("/property/{property_id}", summary="Update an existing property", description="Updates an existing property specified by its ID with provided data.")
def update_property(property_id: int, property: UpdateProperty, db: sqlite3.Connection = Depends(get_db)):
    """Updates an existing property without needing the entire Property object."""
    cursor = db.cursor()
    update_data = property.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    # Need to dynamically create the set clause based on the keys in the update_data
    set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    update_data['id'] = property_id  

    sql_statement = f"UPDATE properties SET {set_clause} WHERE id = :id"

    try:
        cursor.execute(sql_statement, update_data)
        db.commit()
        return {"message": "Property updated", "property": property}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/property/{property_id}", summary="Delete a property", description="Deletes a property specified by its ID from the database.")
def delete_property(property_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Deletes a property by its ID."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
    property = cursor.fetchone()
    try: 
        if property:
            cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
            db.commit()
            return {"message": "Property deleted", "property_id": property_id}

        else:
            # No rows were deleted, indicating the property ID was not found
            raise HTTPException(status_code=404, detail="Property not found")

    except sqlite3.IntegrityError as ie:
        db.rollback()
        print(f"Integrity error occurred: {ie}")
        return {"error": str(ie)}, 400
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
        return {"error": str(e)}, 400
