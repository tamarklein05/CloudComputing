from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="NER API", description="API לזיהוי ישויות בטקסט", version="1.0")

ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple"
)

class TextRequest(BaseModel):
    text: str

@app.post("/ner")
def extract_entities(request: TextRequest):
    results = ner_pipeline(request.text)
    entities = []
    for ent in results:
        entities.append({
            "entity": ent["entity_group"],
            "text": ent["word"],
            "score": ent["score"]
        })
    return {"entities": entities}
