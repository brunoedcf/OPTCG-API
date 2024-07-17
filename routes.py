from typing import List
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Collection, Card, CardWithCollection

router = APIRouter()


# POST route for creating a new collection
@router.post(
    "/collections",
    response_description="Add new collection",
    status_code=status.HTTP_201_CREATED,
    response_model=Collection,
)
def create_collection(request: Request, collection: Collection = Body(...)):
    collection = jsonable_encoder(collection)
    new_collection = request.app.database["collections"].insert_one(collection)
    created_collection = request.app.database["collections"].find_one(
        {"_id": new_collection.inserted_id}
    )

    return created_collection


# POST route for creating a new card
@router.post(
    "/cards",
    response_description="Add new card",
    status_code=status.HTTP_201_CREATED,
    response_model=Card,
)
def create_card(request: Request, card: Card = Body(...)):
    # Ensure the referenced collection_id exists
    if not request.app.database["collections"].find_one({"_id": card.collection_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )

    card = jsonable_encoder(card)
    new_card = request.app.database["cards"].insert_one(card)
    created_card = request.app.database["cards"].find_one({"_id": new_card.inserted_id})

    return created_card


# GET route for getting all collections
@router.get(
    "/collections",
    response_description="Get all collections",
    response_model=List[Collection],
)
def get_all_collections(request: Request):
    collections = list(request.app.database["collections"].find({}))
    return collections


# GET route for getting a collection by acronym
@router.get(
    "/collections/{acronym}",
    response_description="Get a collection by acronym",
    response_model=Collection,
)
def get_collection_by_acronym(request: Request, acronym: str):
    collection = request.app.database["collections"].find_one({"acronym": acronym})
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return collection


# GET route for getting all cards
@router.get("/cards", response_description="Get all cards", response_model=List[Card])
def get_all_cards(request: Request):
    cards = list(request.app.database["cards"].find({}))
    return cards


# GET route for getting cards by collection
@router.get(
    "/cards/collection/{collection_id}",
    response_description="Get cards by collection ID",
    response_model=List[Card],
)
def get_cards_by_collection(request: Request, collection_id: str):
    if not request.app.database["collections"].find_one({"_id": collection_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    cards = list(request.app.database["cards"].find({"collection_id": collection_id}))
    return cards


@router.get(
    "/cards/{collection_number}",
    response_description="Get a card by collection number",
    response_model=CardWithCollection,
)
def get_card_by_collection_number(request: Request, collection_number: str):
    card = request.app.database["cards"].find_one(
        {"collection_number": collection_number}
    )
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found"
        )

    collection = request.app.database["collections"].find_one(
        {"_id": card["collection_id"]}
    )
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )

    return {"card": card, "collection": collection}


# PUT route for updating a collection by acronym
@router.put(
    "/collections/{acronym}",
    response_description="Update a collection by acronym",
    response_model=Collection,
)
def update_collection_by_acronym(
    request: Request, acronym: str, collection: Collection = Body(...)
):
    # Exclude the fields that should not be updated
    collection_data = collection.dict(
        exclude_unset=True, exclude={"id", "_id", "acronym"}
    )
    if len(collection_data) >= 1:
        update_result = request.app.database["collections"].update_one(
            {"acronym": acronym}, {"$set": collection_data}
        )

        if update_result.modified_count == 1:
            updated_collection = request.app.database["collections"].find_one(
                {"acronym": acronym}
            )
            if updated_collection is not None:
                return updated_collection

    existing_collection = request.app.database["collections"].find_one(
        {"acronym": acronym}
    )
    if existing_collection is not None:
        return existing_collection

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Collection with acronym {acronym} not found",
    )


# PUT route for updating a card by collection number
@router.put(
    "/cards/{collection_number}",
    response_description="Update a card by collection number",
    response_model=Card,
)
def update_card_by_collection_number(
    request: Request, collection_number: str, card: Card = Body(...)
):
    # Exclude the fields that should not be updated
    card_data = card.dict(
        exclude_unset=True, exclude={"id", "_id", "collection_number"}
    )
    if len(card_data) >= 1:
        update_result = request.app.database["cards"].update_one(
            {"collection_number": collection_number}, {"$set": card_data}
        )

        if update_result.modified_count == 1:
            updated_card = request.app.database["cards"].find_one(
                {"collection_number": collection_number}
            )
            if updated_card is not None:
                return updated_card

    existing_card = request.app.database["cards"].find_one(
        {"collection_number": collection_number}
    )
    if existing_card is not None:
        return existing_card

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Card with collection number {collection_number} not found",
    )
