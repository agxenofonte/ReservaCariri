import os
from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient

_client = None


def get_collection(name: str):
    global _client

    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise RuntimeError("Configure a variável de ambiente MONGODB_URI.")

    if _client is None:
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

    database_name = os.getenv("MONGODB_DATABASE", "reserva_cariri")
    return _client[database_name][name]


def parse_object_id(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido.")
    return ObjectId(id)


def serialize_document(document: dict[str, Any]) -> dict[str, Any]:
    document["id"] = str(document.pop("_id"))
    return document
