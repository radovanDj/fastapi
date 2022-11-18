from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


from database import Base


class velikan(Base):
    __tablename__ = "velikani"

    id = Column(Integer, primary_key=True, index=True)
    ime = Column(String)
    prezime = Column(String)    


