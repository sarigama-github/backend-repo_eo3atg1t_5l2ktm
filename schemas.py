"""
Database Schemas for Xperience Hub Client Portal

Each Pydantic model corresponds to a MongoDB collection.
Collection name is the lowercase of the class name.
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr

class Client(BaseModel):
    name: str = Field(..., description="Primary contact full name")
    company: str = Field(..., description="Client company name")
    email: EmailStr = Field(..., description="Contact email")
    avatar_url: Optional[str] = Field(None, description="Optional avatar image URL")

class Project(BaseModel):
    client_id: str = Field(..., description="Related client id as string")
    name: str = Field(..., description="Project name")
    status: Literal['planning','active','paused','completed'] = Field('active', description="Project status")
    goal: Optional[str] = Field(None, description="Primary project goal / outcome")
    sentiment: float = Field(0.75, ge=0.0, le=1.0, description="Client sentiment (0-1)")

class Milestone(BaseModel):
    project_id: str = Field(..., description="Related project id")
    title: str = Field(..., description="Milestone title")
    due_date: Optional[str] = Field(None, description="ISO date string for due date")
    status: Literal['upcoming','in-progress','done'] = Field('upcoming', description="Milestone status")
    description: Optional[str] = Field(None, description="Details for the milestone")

class Update(BaseModel):
    project_id: str = Field(..., description="Related project id")
    title: str = Field(..., description="Update title")
    message: str = Field(..., description="Human, friendly update body")
    mood: Literal['excited','on-track','blocked'] = Field('on-track', description="Tone of the update")
    progress: int = Field(0, ge=0, le=100, description="Percent progress for this update")
    celebrate: bool = Field(False, description="Whether this update triggers a celebration")

class Celebration(BaseModel):
    project_id: str = Field(..., description="Related project id")
    type: Literal['applause','milestone','shoutout'] = Field('applause', description="Celebration type")
    note: Optional[str] = Field(None, description="Optional note for the celebration")
