import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Brother(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    first_name: str = Field(...)
    assembly: str = Field(...)
    disciple_maker: str = Field(...)
    statut: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "SOUNDJOCK",
                "first_name": "Welen",
                "assembly": "Orsay",
                "disciple_maker": "Jill NANFACK",
                "new_birth_date": "15/11/2011",
                "statut": "frère"
            }
        }

class BrotherUpdate(BaseModel):
    name: Optional[str]
    first_name: Optional[str]
    assembly: Optional[str]
    disciple_maker: Optional[str]
    statut: Optional[str]


    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "SOUNDJOCK",
                "first_name": "Welen",
                "assembly": "Orsay",
                "disciple_maker": "Jill NANFACK",
                "new_birth_date": "19/05/2015",
                "statut": "frère"                
            }
        }


class Assembly(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    adress: str = Field(...)
    city: str = Field(...)
    region: str = Field(...)
    country: str = Field(...)
    leader: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Villeneuve-la-Garenne",
                "adress": "14 Rue Chaillon, 92390 Villeneuve-la-Garenne",
                "city": "Villeneuve-la-Garenne",
                "region": "Île-de-france (Paris)",
                "country": "France",
                "leader": "Noé YOLÉKÉ"                
            }
        }

class AssemblyUpdate(BaseModel):
    name: Optional[str]
    adress: Optional[str]
    city: Optional[str]
    region: Optional[str]
    country: Optional[str]
    leader: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Villeneuve-la-Garenne",
                "adress": "14 Rue Chaillon, 92390 Villeneuve-la-Garenne",
                "city": "Villeneuve-la-Garenne",
                "region": "Île-de-france (Paris)",
                "country": "France",
                "leader": "Noé YOLÉKÉ"                
            }
        }