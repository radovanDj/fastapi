from dataclasses import dataclass
from typing import List, Optional

from anyio import create_task_group, run, sleep
from sqlalchemy.orm import Session
from sqlalchemy import select
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
        except:
            ret = HTTPException(
                status_code=503, detail="nesto se iscasilo")

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
    except:
        ret = HTTPException(
            status_code=503, detail="nesto se iscasilo")

    return ret


# @app.put("/velikan/{id}")
# async def izmeni(id: int, ime: Optional[str] = None, prezime: Optional[str] = None):
#     for vel in velikani:
#         if vel.id == id:
#             if ime != None:
#                 vel.ime = ime
#             if prezime != None:
#                 vel.prezime = prezime
#             return vel
#     raise HTTPException(status_code=503, detail="nema gi sa tim rednim brojem")


async def vratisve():
    await sleep(2)


# @app.get("/velikani")
# async def citajsve():
#     async with create_task_group() as tg:
#         await tg.spawn(vratisve)
#         await tg.spawn(vratisve)
#         await tg.spawn(vratisve)
#         await tg.spawn(vratisve)
#         await tg.spawn(vratisve)

#         # ceka se 2 sec a trebalo bi 6
#     return velikani


# @app.delete("/velikan/{id}")
# async def brisi(id: int):
#     """
#     id: unesi identifikacioni broj velikana kog zelis da obrises sa liste
#     """
#     for vel in velikani:
#         if vel.id == id:
#             velikani.remove(vel)
#             return "uspesno obrisan"
#     return "nema gi sa tim rednim brojem"
#     raise HTTPException(status_code=404, detail="nema gi sa tim rednim brojem")
