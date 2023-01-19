from dataclasses import Field
from pydantic import BaseModel, Field


# ovo je schemas.py fajl koji u FastAPI dokumentaciji postoji
class Podatak(BaseModel):
    """ovo je klasa koja definise velikana i u sebi ima 
    ime - ime čoveka
    prezime - prezime čoveka
    """
    ime: str = Field(default="")
    prezime: str = Field(default="")

    class Config:
        """ovo je za pydantic i sluzi da se prenesu neke informacije pydantic-u za mapiranje
        """
        schema_extra = {
            "example": {
                "id": 2,
                "ime": "Radovan",
                "prezime": "Đurđević"}
        }
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
