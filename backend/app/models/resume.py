"""Resume and ResumeVersion ORM Models."""

import uuid
from typing import Any

from sqlalchemy import JSON, BigInteger, Boolean, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Resume(Base, TimestampMixin):
    """Resume document model representing master and role-specific tailored versions."""

    __tablename__ = "resumes"

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
    target_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_master: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    parent_version_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("resumes.id", ondelete="SET NULL"),
        nullable=True,
    )
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    structured_data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="draft",
        nullable=False,
    )

    # Relationships
    versions: Mapped[list["ResumeVersion"]] = relationship(
        "ResumeVersion",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="ResumeVersion.version_number.desc()",
    )

    def __repr__(self) -> str:
        return f"<Resume(id={self.id}, title='{self.title}', user_id={self.user_id})>"


class ResumeVersion(Base):
    """Immutable snapshot of resume modifications and role-specific adaptations."""

    __tablename__ = "resume_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    role_name: Mapped[str] = mapped_column(String(255), nullable=False)
    structured_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    diff_summary: Mapped[dict[str, Any] | None] = mapped_column(JSON, default=dict, nullable=True)

    # Relationship
    resume: Mapped["Resume"] = relationship("Resume", back_populates="versions")

    def __repr__(self) -> str:
        return f"<ResumeVersion(id={self.id}, resume_id={self.resume_id}, v={self.version_number})>"
