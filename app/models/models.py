from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    storage_path = Column(String(512)) # Local directory path
    user = relationship("User", back_populates="projects")
    chapters = relationship("Chapter", back_populates="project", cascade="all, delete-orphan")

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(255))
    file_path = Column(String(512)) # Path to .md file
    chapter_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="chapters")
    drafts = relationship("Draft", back_populates="chapter", cascade="all, delete-orphan")

class Draft(Base):
    __tablename__ = "drafts"
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    title = Column(String(255))
    file_path = Column(String(512)) # Path to .md file
    draft_type = Column(String(50), default="rough") # rough, revised, polished, experimental, archived
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chapter = relationship("Chapter", back_populates="drafts")
