from fastapi import FastAPI, HTTPException, Depends, status, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator, Field
from typing import Optional, Annotated
from datetime import datetime
from passlib.context import CryptContext
from contextlib import asynccontextmanager
from database.database import get_db, create_tables
from datetime import datetime
import sqlite3

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn_generator = get_db()
    conn = next(conn_generator)
    create_tables(conn)
    yield


app = FastAPI(lifespan=lifespan)
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: str
    password: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_current_active_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: sqlite3.Connection = Depends(get_db),
):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (credentials.username,))

    row = cursor.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    is_correct_username = row[1] == credentials.username
    is_correct_password = pwd_context.verify(credentials.password, row[2])

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def root():
    return "Property API v1"

@app.post("/register")
def register_user(user: User, db: sqlite3.Connection = Depends(get_db)):
    """
    Registers a new user by hashing their password and storing user credentials in the database.
    """
    user.password = pwd_context.hash(user.password)  # Hash the password
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                   (user.username, user.email, user.password))
    db.commit()
    return {"message": "User registered successfully"}


@app.post("/login")
def login(username: str, password: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user and verify_password(password, user[0]):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


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

    @field_validator('property_value', 'sqft', 'lot_size', 'bed', 'bath', 'sleeps')
    def check_positive(cls, v):
        if not isinstance(v, int):
            raise ValueError('must be an integer')
        if v < 0:
            raise ValueError('must be positive')
        return v

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

    @field_validator('property_value', 'sqft', 'lot_size', 'bed', 'bath', 'sleeps')
    def check_positive(cls, v):
        if not isinstance(v, int):
            raise ValueError('must be an integer')
        if v < 0:
            raise ValueError('must be positive')
        return v

@app.get("/hello")
def hello(username: Annotated[str, Depends(get_current_active_user)]):
    return {"message": "Vantage Score Challenge"}

@app.get("/property", summary="Retrieve all properties", description="Returns a list of all properties in the database with detailed information.")
def get_properties(db: sqlite3.Connection = Depends(get_db), currentUser = Depends(get_current_active_user)):
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
def get_property(property_id: int, db: sqlite3.Connection = Depends(get_db), currentUser = Depends(get_current_active_user)):
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
def create_property(property: Property, db: sqlite3.Connection = Depends(get_db), currentUser = Depends(get_current_active_user)):
    """Creates a new property with the provided details. Inputs are validated for greater than 0 values."""
    cursor = db.cursor()
    property = Property(**property.model_dump())
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
def update_property(property_id: int, property: UpdateProperty, db: sqlite3.Connection = Depends(get_db), currentUser = Depends(get_current_active_user)):
    """Updates an existing property without needing the entire Property object."""
    cursor = db.cursor()

    cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
    property_db_check = cursor.fetchone()

    if property_db_check is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    update_property = property.model_dump(exclude_none=True)

    if not update_property:
        raise HTTPException(status_code=400, detail="No data provided for update")

    # Need to dynamically create the set clause based on the keys in the update_data
    set_clause = ", ".join([f"{key} = :{key}" for key in update_property.keys()])
    update_property['id'] = property_id  


    sql_statement = f"UPDATE properties SET {set_clause} WHERE id = :id"

    try:
        cursor.execute(sql_statement, update_property)
        db.commit()
        return {"message": "Property updated", "property": property}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/property/{property_id}", summary="Delete a property", description="Deletes a property specified by its ID from the database.")
def delete_property(property_id: int, db: sqlite3.Connection = Depends(get_db), currentUser = Depends(get_current_active_user)):
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
