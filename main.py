from dataclasses import dataclass
from typing_extensions import Self
from anyio import create_task_group, run, sleep
from fastapi import FastAPI, HTTPException,Path
from typing import Optional
from pydantic import BaseModel




app = FastAPI()


class Podatak(BaseModel):
    """ovo je klasa koja definise velikana i u sebi ima 
    id - redni broj
    ime - ime coeka
    prezime - prezime coeka
    """    
    id:int
    ime:str
    prezime:str
   
       
        
p1=Podatak(id=0,ime="NIkola",prezime="Tesla")
p2=Podatak(id=1,ime="Mihajlo",prezime="Pupin")
p3=Podatak(id=2,ime="Radovan",prezime="Damjanovic")
velikani=[p1,p2,p3]


@app.get('/')
def root():
    return 'ovo je test api sa svim REST metodama za vezbu'
    


@app.get('/velikan/{id}')
async def citaj(id: int  = Path(..., description=" unesi identifikacioni broj velikana")):    
    for vel in velikani:
        if vel.id==id:
            return vel                         
    return "nema gi sa tim rednim brojem"
    raise HTTPException(status_code=404, detail="nema gi sa tim rednim brojem")
    
    
@app.post('/velikan/{id}')
async def dodaj(id: int, ime: str,prezime: str):
    """_summary_

    Args:
        id (int): redni broj koji mora da se dodeli rucno
        ime (str): ime velikana
        prezime (str): prezime velikana

    Raises:
        HTTPException: ovaj redni broj vec postoji
        HTTPException: ovaj velikan vec postoji

    Returns:
        _type_: Podatak
    """
    for vel in velikani:
        if vel.id==id:
            raise HTTPException(status_code=503, detail="ovaj redni broj vec postoji")
        if vel.ime==ime and vel.prezime==prezime:
            raise HTTPException(status_code=503, detail="ovaj velikan vec postoji")
    velikani.append(Podatak(id=id,ime=ime,prezime=prezime))
    return Podatak(id=id,ime=ime,prezime=prezime)

@app.post('/velikan')
async def dodajKrozBodi(podt: Podatak):
    """_summary_

    Args:
        id (int): _description_
        podt (Podatak): _description_

    Raises:
        HTTPException: ako redni broj vec postoji
        HTTPException: ako velikan vec postoji

    Returns:
        _type_: _description_
    """
    for vel in velikani:
        if vel.id==podt.id:
            raise HTTPException(status_code=404, detail="ovaj redni broj vec postoji")
        if vel.ime==podt.ime and vel.prezime==podt.prezime:
            raise HTTPException(status_code=404, detail="ovaj velikan vec postoji")
    velikani.append(podt)
    return podt
    

@app.put('/velikan/{id}')
async def izmeni(id: int, ime:Optional[str] = None ,prezime: Optional[str] = None ):
    for vel in velikani:
        if vel.id==id:
            if ime !=None:
                vel.ime=ime
            if prezime !=None:
                vel.prezime=prezime
            return vel    
    raise HTTPException(status_code=503, detail="nema gi sa tim rednim brojem")       
    return Podatak(id,ime,prezime) 
    
async def vratisve():
    await sleep(2)
        
        
    
@app.get('/velikani')
async def citajsve():    
    async with create_task_group() as tg:  
        await tg.spawn(vratisve)        
        await tg.spawn(vratisve)        
        await tg.spawn(vratisve)        
        await tg.spawn(vratisve)        
        await tg.spawn(vratisve)                   
               
        # ceka se 2 sec a trebalo bi 6
    return velikani        
  
  
@app.delete('/velikan/{id}')
async def brisi(id: int):
    """
     id: unesi identifikacioni broj velikana kog zelis da obrises sa liste
    """ 
    for vel in velikani:
        if vel.id==id:
            velikani.remove(vel)
            return "uspesno obrisan"                         
    return "nema gi sa tim rednim brojem"
    raise HTTPException(status_code=404, detail="nema gi sa tim rednim brojem")