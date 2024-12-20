# models.py
from sqlalchemy import Table, Column, Integer, String, Float, Text, Boolean, ForeignKey, INTEGER
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):  # Existing User model
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    gardens = relationship("Garden", secondary="user_gardens",back_populates="members" )

# Association table for gardens and user, many-to-many

class UserGardens(Base):
    __tablename__ = "user_gardens"
    user_id =Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
    garden_id =Column("garden_id", Integer, ForeignKey("gardens.id"), primary_key=True)


# Association table for gardens and tags
garden_tags = Table(
    "garden_tags",
    Base.metadata,
    Column("garden_id", Integer, ForeignKey("gardens.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)

    # Many-to-many relationship with Garden
    gardens = relationship("Garden", secondary=garden_tags, back_populates="tags")

class Garden(Base):
    __tablename__ = "gardens"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True)
    description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    street_name = Column(String(100), nullable=True)
    photo = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=True)
    joinable = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    members = relationship("User", secondary="user_gardens", back_populates="gardens")

    owner = relationship("User", back_populates="gardens", foreign_keys=[owner_id])
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=garden_tags,
        back_populates="gardens",
        lazy="selectin"  # Specify the loading strategy
    )

