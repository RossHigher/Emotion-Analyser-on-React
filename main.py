from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  
from typing import List 
from Advanced import Response
from EmojiText import ResponseLinear
app = FastAPI()

# Настройка CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_methods=["GET", "POST"],  
    allow_headers=["*"],  
)


class TextRequest(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    emotions: List[str]

@app.post("/api/analyze", response_model=EmotionResponse)
async def analyze_text(request: TextRequest):
    try:
        emotions = Response(request.text)  
        return EmotionResponse(emotions=emotions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# uvicorn main:app --reload 
