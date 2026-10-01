"""Candidate Profile ORM Model."""

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class CandidateProfile(Base, TimestampMixin):
    """Candidate master profile storing verified candidate background facts."""

    __tablename__ = "candidate_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    headline: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_info: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    skills: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    experience: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    education: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    projects: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    certifications: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    achievements: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    publications: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    links: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"<CandidateProfile(id={self.id}, user_id={self.user_id})>"
