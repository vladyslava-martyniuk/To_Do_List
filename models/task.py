from __future__ import annotations

from base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey



class Task(Base):
    __tablename__ = "tasks"   

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="new")
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="tasks")

    def repr(self):
        return f"Task(id={self.id!r}, name={self.name!r}, status={self.status!r})"