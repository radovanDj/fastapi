from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


from database import Base


class velikan(Base):
    # ovako se definise naziv tabele
    __tablename__ = "velikani"

    id = Column(Integer, primary_key=True, index=True)
    ime = Column(String(255), nullable=True)
    prezime = Column(String(255), nullable=True)
