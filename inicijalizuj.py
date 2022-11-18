from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Path
from pydanticmodel import Podatak
import dbmodel


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        raise Exception("nije povezana baza u f-ji get_db")
    finally:
        db.close()


def inicijalizuj(baza: Session = Depends(get_db)):
    p1 = Podatak(ime="NIkola", prezime="Tesla")
    p2 = Podatak(ime="Mihajlo", prezime="Pupin")
    p3 = Podatak(ime="Radovan", prezime="Damjanovic")
    unos1 = dbmodel.velikan(**p1.dict())
    unos2 = dbmodel.velikan(**p2.dict())
    unos3 = dbmodel.velikan(**p3.dict())
    baza.add(unos1)
    baza.commit()
    baza.refresh(unos1)
    baza.add(unos2)
    baza.commit()
    baza.refresh(unos2)
    baza.add(unos3)
    baza.commit()
    baza.refresh(unos3)

    baza.close()
