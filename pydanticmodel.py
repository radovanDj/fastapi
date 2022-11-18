from dataclasses import Field
from pydantic import BaseModel,Field


# ovo je schemas.py fajl koji u FastAPI dokumentaciji postoji
class Podatak(BaseModel):
    """ovo je klasa koja definise velikana i u sebi ima 
    id - redni broj
    ime - ime coeka
    prezime - prezime coeka
    """    
    ime:str=Field(min_length=1)
    prezime:str=Field(min_length=1)