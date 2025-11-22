from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum
from . import login_manager
from app import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Boolean,
    func,
    UniqueConstraint,
    Numeric,
    CHAR,
    text,
    select,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ---------- Mixins ----------
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now(), nullable=False
    )

# ---------- Enums ----------
class RsvpStatus(PyEnum):
    going = "going"
    waitlisted = "waitlisted"
    interested = "interested"
    declined = "declined"
    canceled = "canceled"

# ---------- Association Tables ----------
event_categories = db.Table(
    "event_categories",
    db.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    Index("idx_event_categories_category", "category_id"),
)

# ---------- Models ----------
# User(id, email, username, full_name, avatar_url)
class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(50), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(Text)

    # Relationships
    organized_events: Mapped[list["Event"]] = relationship(
        back_populates="organizer", cascade="all, delete-orphan"
    )
    rsvps: Mapped[list["Rsvp"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[list["EventComment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"

# Category(id, slug, name)
class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    events: Mapped[list["Event"]] = relationship(
        secondary=event_categories, back_populates="categories"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} slug={self.slug!r}>"

# Event (id, title, description, address_line1, address_line2, starts_at, ends_at)
class Event(db.Model, TimestampMixin):
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("ends_at > starts_at", name="chk_event_time"),
        Index("idx_events_starts_at", "starts_at"),
        Index("idx_events_organizer", "organizer_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer)  # NULL = unlimited
    is_public: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    address_line1: Mapped[str | None] = mapped_column(String(255))
    address_line2: Mapped[str | None] = mapped_column(String(255))

    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    organizer: Mapped[User] = relationship(back_populates="organized_events")

    categories: Mapped[list[Category]] = relationship(
        secondary=event_categories, back_populates="events"
    )
    rsvps: Mapped[list["Rsvp"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
    comments: Mapped[list["EventComment"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )

    @hybrid_property
    def seats_taken(self) -> int:
        """Counts the number of occupied seats (1 per going RSVP + guests)."""
        return sum(
            (1 + r.guests_count) for r in self.rsvps if r.status == RsvpStatus.going
        )

    @seats_taken.expression  # type: ignore[no-redef]
    def seats_taken(cls):  # noqa: N805
        return (
            select(func.coalesce(func.sum(1 + Rsvp.guests_count), 0))
            .where((Rsvp.event_id == cls.id) & (Rsvp.status == RsvpStatus.going))
            .correlate(cls)
            .scalar_subquery()
        )

    @property
    def is_full(self) -> bool:
        return self.capacity is not None and self.seats_taken >= self.capacity

    def __repr__(self) -> str:
        return f"<Event id={self.id} title={self.title!r}>"

# Rsvp(id, user_id, event_id)
class Rsvp(db.Model, TimestampMixin):
    __tablename__ = "rsvps"
    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_rsvps_user_event"),
        Index("idx_rsvps_event_status", "event_id", "status"),
        Index("idx_rsvps_user", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)

    # Use native DB enum if available; otherwise it stores values as VARCHAR
    status: Mapped[RsvpStatus] = mapped_column(
        Enum(RsvpStatus, name="rsvp_status", native_enum=True), nullable=False
    )

    guests_count: Mapped[int] = mapped_column(Integer, server_default=text("0"), nullable=False)
    note: Mapped[str | None] = mapped_column(Text)

    user: Mapped[User] = relationship(back_populates="rsvps")
    event: Mapped[Event] = relationship(back_populates="rsvps")

    def __repr__(self) -> str:
        return f"<Rsvp id={self.id} user_id={self.user_id} event_id={self.event_id} status={self.status.value}>"

# EventComment(id, event_id, user_id, body)
class EventComment(db.Model):
    __tablename__ = "event_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    event: Mapped[Event] = relationship(back_populates="comments")
    user: Mapped[User] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"<EventComment id={self.id} event_id={self.event_id} user_id={self.user_id}>"


@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))
