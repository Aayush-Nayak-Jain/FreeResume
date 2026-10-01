"""JobDescription ORM Model."""

import uuid
from typing import Any

from sqlalchemy import JSON, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class JobDescription(Base, TimestampMixin):
    """Job Description model storing submitted target roles, structured requirements, and weights."""

    __tablename__ = "job_descriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    structured_requirements: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    weights_config: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=lambda: {
            "skills": 0.40,
            "experience": 0.20,
            "projects": 0.15,
            "education": 0.10,
            "semantic_similarity": 0.10,
            "certifications": 0.05,
        },
        nullable=False,
    )

    # Relationship to user
    user = relationship("User", backref="job_descriptions")

    def __repr__(self) -> str:
        return f"<JobDescription(id={self.id}, title='{self.title}', user_id={self.user_id})>"
