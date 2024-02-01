from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from INF import infenrece

app = FastAPI()

class Body(BaseModel):
    text:str

@app.get('/')
def root():
    return HTMLResponse('<h1> CWI German language')
@app.post('/simplify')
def predict(body: Body):
    detected_words, new_sentence , old_sentence = infenrece(body.text)
    return new_sentence

