from typing import Literal
from pydantic import BaseModel, Field, EmailStr

class RegisterInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class ProductRecommendation(BaseModel):
    name: str
    category: str
    platform: str
    estimated_price: int = Field(ge=0)
    reason: str
    search_url: str
    budget_fit: str = "Within budget"

class RecommendationResponse(BaseModel):
    planner: Literal["home", "party", "jewelry"]
    budget: int
    budget_summary: str
    allocation: dict[str, int]
    recommendations: list[ProductRecommendation]
    tips: list[str]
    disclaimer: str = "Prices and availability are estimates unless supplied by an authorized provider."

class HomeRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    rooms: str = Field(min_length=2, max_length=1000)
    style: str = Field(min_length=2, max_length=200)
    needs: str = Field(min_length=2, max_length=2000)

class PartyRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=100000)
    event_type: str = Field(min_length=2, max_length=100)
    venue: str = Field(min_length=2, max_length=500)
    preferences: str = Field(default="", max_length=2000)

class SessionInfo(BaseModel):
    logged_in: bool
    user_id: int | None = None
    name: str | None = None
