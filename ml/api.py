from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import traceback
import uvicorn

# Импорт анализатора из вашего проекта
from main import AdvancedBankingAnalyzer

# Маппинг тональностей на русский
RUS_SENT_MAP = {
    'positive': 'положительно',
    'negative': 'отрицательно',
    'neutral': 'нейтрально'
}

class ReviewItem(BaseModel):
    id: int
    text: str

class PredictRequest(BaseModel):
    data: List[ReviewItem]

class PredictItem(BaseModel):
    id: int
    topics: List[str]
    sentiments: List[str]

class PredictResponse(BaseModel):
    predictions: List[PredictItem]

app = FastAPI(title="Banking Review Topic API")
analyzer: AdvancedBankingAnalyzer | None = None

@app.on_event("startup")
def startup_event():
    global analyzer
    try:
        analyzer = AdvancedBankingAnalyzer()
    except Exception:
        traceback.print_exc()
        analyzer = None

@app.get("/health")
def health():
    return {"status": "ok", "analyzer_initialized": analyzer is not None}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    global analyzer
    if analyzer is None:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    # Подготовка формата для analyzer
    reviews = []
    for item in req.data:
        reviews.append({
            "id": item.id,
            "text": item.text,
            "rating": None,
            "date": None,
            "file": "api"
        })
    try:
        analyzed = analyzer.process_reviews_batch(reviews, batch_size=50)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

    preds: List[PredictItem] = []
    for r in analyzed:
        topics = r.get("predicted_themes") or []
        sentiments = []
        for t in topics:
            s = r.get("theme_sentiments", {}).get(t)

            # если rule-based нет или он нейтрален, посмотрим детальные метки модели (blanchefort)
            use_label = None
            if s is None or (isinstance(s, str) and s.lower() == 'neutral'):
                detailed = r.get('theme_sentiments_detailed', {}).get(t, {})
                bl_label = detailed.get('blanchefort_label')
                bl_conf = detailed.get('blanchefort_confidence')
                if isinstance(bl_label, str):
                    bl_norm = bl_label.lower()
                    # если модель даёт не-neutral, используем её
                    if bl_norm != 'neutral':
                        use_label = bl_norm

            # если не решили использовать модель — берем rule-based или общий
            if use_label is None:
                if isinstance(s, str):
                    s_norm = s.lower()
                else:
                    s_norm = r.get('overall_sentiment', 'neutral')
                    if isinstance(s_norm, str):
                        s_norm = s_norm.lower()
                sentiments.append(RUS_SENT_MAP.get(s_norm, "нейтрально"))
            else:
                sentiments.append(RUS_SENT_MAP.get(use_label, "нейтрально"))
        # Если тем не найдено — вернуть общую тональность для отзыва
        if not topics:
            overall = r.get('overall_sentiment', 'neutral')
            overall_norm = overall.lower() if isinstance(overall, str) else 'neutral'
            sentiments = [RUS_SENT_MAP.get(overall_norm, 'нейтрально')]

        preds.append(PredictItem(id=r.get("id"), topics=topics, sentiments=sentiments))

    return PredictResponse(predictions=preds)

if __name__ == "__main__":
    # Для разработки: uvicorn c:\.../api:app --host 0.0.0.0 --port 8000
    uvicorn.run("api:app", host="0.0.0.0", port=8000, workers=1)