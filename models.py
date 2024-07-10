import uuid
from pydantic import BaseModel, Field
from datetime import datetime


# Pydantic model for Collection
class Collection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str = Field(...)
    acronym: str = Field(...)
    release_date: datetime = Field(...)
    link: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "500 Years in the Future",
                "acronym": "OP-07",
                "release_date": "2024-06-28T00:00:00",
                "link": "https://www.ligaonepiece.com.br/?view=cards/edicoes",
            }
        }


# Pydantic model for Card
class Card(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    collection_id: str = Field(...)
    number: str = Field(...)
    collection_number: str = Field(...)
    name: str = Field(...)
    lowest_price: float
    highest_price: float
    link_marketplace: str = Field(...)
    image: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "a4b709c3-9c63-4a9e-9c74-11a1d3fcb1df",
                "collection_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "number": "OP07-002",
                "collection_number": "OP-07: OP07-002",
                "name": "Ain (OP07-002)",
                "lowest_price": 2.50,
                "highest_price": 3.99,
                "link_marketplace": "https://www.ligaonepiece.com.br/?view=cards/card&card=Ain%20(OP07-002)&ed=OP-07&num=OP07-002",
                "image": "//repositorio.sbrauble.com//arquivos/in/onepiece/34/667066301241f-bny1l-dl3ag-abe41489b7529f93619f73610b65569a.jpg",
            }
        }
