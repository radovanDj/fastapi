from dataclasses import dataclass
from typing import Optional

from anyio import create_task_group, run, sleep
from sqlalchemy.orm import Session
import dbmodel
from inicijalizuj import get_db, inicijalizuj, obrisiSVE
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, Path

from dbmodel import velikan
from pydanticmodel import Podatak


app = FastAPI()

dbmodel.Base.metadata.create_all(bind=engine)

privremenaSesija = Session(engine)
# obrisiSVE(privremenaSesija)
testPodaci = privremenaSesija.query(dbmodel.velikan).all()
if len(testPodaci) == 0:
    inicijalizuj(Session(engine))
# rez = privremenaSesija.query(dbmodel.velikan).first()
# rez = privremenaSesija.query(dbmodel.velikan).filter(
#     velikan.ime == 'Radovan').first()
# print(rez.ime + ", prezime: " + rez.prezime)
privremenaSesija.close()

# p1 = Podatak(ime="NIkola", prezime="Tesla")
# p2 = Podatak(ime="Mihajlo", prezime="Pupin")
# p3 = Podatak(ime="Radovan", prezime="Damjanovic")
# velikani = [p1, p2, p3]

# , response_class=HTMLResponse se pise ako zelimo da povratni tip koji je uvek JSON vratimo kao HTML


@app.get("/")
def root(db: Session = Depends(get_db)):
    return db.query(dbmodel.velikan).all()


@app.get("/velikan/{id}")
async def citaj(db: Session = Depends(get_db),
                id: int = Path(..., description=" unesi identifikacioni broj velikana")):
    svi = db.query(dbmodel.velikan).all()
    for vel in svi:
        if vel.id == id:
            return vel
    return "nema gi sa tim rednim brojem"
    # raise HTTPException(status_code=404, detail="nema gi sa tim rednim brojem")


@app.post("/velikan/{ime}/{prezime}")
async def dodaj(ime: str, prezime: str, db: Session = Depends(get_db)):
    for vel in db.query(dbmodel.velikan).all():
        # if vel.id == id:
        #     raise HTTPException(
        #         status_code=503, detail="ovaj redni broj vec postoji")
        if vel.ime == ime and vel.prezime == prezime:
            raise HTTPException(
                status_code=503, detail="ovaj velikan vec postoji")
        podt = Podatak(ime=ime, prezime=prezime)
        try:
            db.add(dbmodel.velikan(**podt.dict()))
            db.commit()
            ret = db.query(dbmodel.velikan).filter(
                velikan.ime == ime, velikan.prezime == prezime).all()
        except Exception as e:
            return e

        return ret


@app.post("/velikan")
async def dodajKrozBodi(podt: Podatak, db: Session = Depends(get_db)):
    """_summary_

    Args:
        podt (Podatak): model podatka{"ime": "string", "prezime": "string"}


    Returns:
        dbmodel.velikan: dbmodel podatka{"id": "int","ime": "string", "prezime": "string"}
    """
    try:
        novVelikan = dbmodel.velikan(**podt.dict())
        db.add(novVelikan)
        db.commit()
        ret = db.query(dbmodel.velikan).filter(
            velikan.ime == novVelikan.ime, velikan.prezime == novVelikan.prezime).all()
    except Exception as e:
        return e

    return ret


@app.put("/velikan/{id}")
async def izmeni_krozPodatak(id: int, podt: Podatak, db: Session = Depends(get_db)):
    for vel in db.query(dbmodel.velikan).all():
        if vel.id == id:
            try:
                if len(podt.ime) != 0 and vel.ime != podt.ime:
                    vel.ime = podt.ime
                    db.commit()
                if len(podt.prezime) != 0 and vel.prezime != podt.prezime:
                    vel.prezime = podt.prezime
                    db.commit()
                return vel
            except Exception as e:
                return e

    return "nema gi sa tim rednim brojem"


@app.put("/velikan")
async def izmeni(id: int, ime: Optional[str] = "", prezime: Optional[str] = "", db: Session = Depends(get_db)):
    for vel in db.query(dbmodel.velikan).all():
        if vel.id == id:
            try:
                if ime != "" and vel.ime != ime:
                    vel.ime = ime
                    db.commit()

                if prezime != "" and vel.prezime != prezime:
                    vel.prezime = prezime
                    db.commit()

                return vel
            except Exception as e:
                return e

    return "nema gi sa tim rednim brojem"


async def vratisve():
    await sleep(2)


@app.get("/velikani")
async def citajsve(db: Session = Depends(get_db)):
    async with create_task_group() as tg:
        await tg.spawn(vratisve)
        await tg.spawn(vratisve)
        await tg.spawn(vratisve)
        await tg.spawn(vratisve)
        await tg.spawn(vratisve)

        # ceka se 2 sec a trebalo bi 10
    return db.query(dbmodel.velikan).all()


@app.delete("/velikan/{id}")
async def brisi(id: int, db: Session = Depends(get_db)):
    """
    id: unesi identifikacioni broj velikana kog zelis da obrises sa liste
    """
    for vel in db.query(dbmodel.velikan).all():
        if vel.id == id:
            try:
                db.delete(vel)
                db.commit()
                return db.query(dbmodel.velikan).all()
            except Exception as e:
                return e

    return "nema gi sa tim rednim brojem"
