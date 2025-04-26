from fastapi import APIRouter, HTTPException, Request
from beanie import Document
from datetime import datetime
from enum import Enum
import uuid
from passlib.context import CryptContext
from pydantic import BaseModel

profileRouter = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

class ProfileBase(BaseModel):
    username: str  
    password: str

class Profile(Document):
    id: str  # Unique identifier for the profile
    name: str  # User's name
    role: RoleEnum  # User's role (admin or user)
    createdDate: datetime  # Date the profile was created
    password: str  # User's password
    clan: str  # Clan the user belongs to
    email: str  # Email address
    picture: str  # Profile picture URL
    lastLoggedIn: datetime  # Last login timestamp

    class Settings:
        name = "profiles"  # MongoDB collection name

    @classmethod
    def initialize_default(cls, id: str) -> "Profile":
        return cls(
            id=id,
            name="John Tester",
            role=RoleEnum.user,
            createdDate=datetime.now(),
            password="default_password",  # Placeholder password
            clan="Clanity Clan",
            email="john@test.com",
            picture="",
            lastLoggedIn=datetime.now(),
        )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@profileRouter.post('/register')
async def register(data: ProfileBase):
    print("Registering:", data.username)
    existing = await Profile.find_one(Profile.name == data.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = Profile(
        id=str(uuid.uuid4()),
        name=data.username,
        role=RoleEnum.user,
        createdDate=datetime.now(),
        password=hash_password(data.password),
        clan="",
        email="",
        picture="",
        lastLoggedIn=datetime.now()
    )

    await user.insert()


    return {"status": "success", "message": "User registered successfully", "userId": str(user.id)}

@profileRouter.post('/login')
async def login(data: ProfileBase):
    print("Logging in:", data.username)
    user = await Profile.find_one(Profile.name == data.username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    print("User found:", user)

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Update last login time
    user.lastLoggedIn = datetime.now()
    user.save()

    return {
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "role": user.role,
            "clan": user.clan,
            "email": user.email,
            "picture": user.picture
        },
        "userId": str(user.id),
    }



@profileRouter.get("/{id}", response_model=Profile)
async def get_profile(id: str):
    profile = await Profile.get(id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@profileRouter.put("/{id}", response_model=Profile)
async def update_profile(id: str, request: Request):
    existing_profile = await Profile.get(id)
    if not existing_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    data = await request.json()

    for field, value in data.items():
        if hasattr(existing_profile, field):
            setattr(existing_profile, field, value)
    await existing_profile.save()
    return existing_profile

@profileRouter.delete("/{id}", response_model=dict)
async def delete_profile(id: str):
    profile = await Profile.get(id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    await profile.delete()
    return {"message": f"Profile with ID '{id}' has been deleted"}

