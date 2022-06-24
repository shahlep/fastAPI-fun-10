from fastapi import APIRouter, HTTPException, status, Depends
import models as _models, schemas as _schemas, oauth2
from database import get_db


router = APIRouter(prefix="/vote", tags=["Vote"])
