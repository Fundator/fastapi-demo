from typing import List, Literal, Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import uuid
import logging
import os
import orjson
import typing
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import User, Token, authenticate_user, fake_users_db, create_access_token, get_current_active_user, get_password_hash
from model import Model, get_model, n_features

app = FastAPI() 
logger = logging.getLogger(__name__)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

class PredictRequest(BaseModel):
    data: List[List[float]]

    @validator("data")
    def check_dimensionality(cls, v):
        for point in v:
            if len(point) != n_features:
                raise ValueError(f"Each data point must contain {n_features} features")

        return v

class PredictResponse(BaseModel):
    data: List[float]

@app.post("/predict/", response_model=PredictResponse)
def predict(input: PredictRequest, model: Model = Depends(get_model), current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to predictions from ML model. 

    Parameters
    ----------
    input : PredictRequest
        PredictRequest according to class definition.
    
    Returns
    ----------
    prediction : PredictResponse
        PredictResponse according to class definition 
    
    """
    try:
        X = np.array(input.data)
        y_pred = model.predict(X)
        prediction = PredictResponse(data=y_pred.tolist())
    except:
        raise HTTPException(status_code=500, detail=f"Could not estimate with input: {input}")
    return prediction

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


