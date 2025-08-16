from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from collections import Counter
from . import database, schemas, crud, reco_engine
from app.models import User, Item
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
db = database.SessionLocal()
engine = reco_engine.RecoEngine()
engine.fit_content_embeddings(db)
engine.compute_popularity(db)
engine.fit_cf(db)

origins = [
    os.getenv("FRONTEND_URL")
]
origins = [origin for origin in origins if origin is not None]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],          
)

@app.get("/v1/reco/homefeed", response_model=schemas.HomefeedResponse)
def homefeed(user_id: int, top_k: int = 10):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"user_id": user_id, "recommendations": []}

    if user_id not in engine.user_map:
        recs = engine.recommend_cold_start(db, user)
    else:
        recs = engine.recommend_hybrid(db, user, top_k=top_k)

    enriched_recs = []
    for r in recs:
        item = db.query(Item).filter(Item.id == r["item_id"]).first()
        if not item:
            continue
        creator_id = item.creator_id
        creator = db.query(User).filter(User.id == creator_id).first()

        enriched_recs.append({
            "item_id": item.id,
            "title": item.title,
            "description": item.description,
            "tags": item.tags,
            "score": r["score"],
            "reason": r.get("reason", "recommended for you"),
            "creator_name": creator.name if creator else "Unknown",
            "community": creator.community if creator else "Unknown"
        })
        print(enriched_recs)

    return {"user_id": user_id, "recommendations": enriched_recs}


@app.post("/v1/reco/feedback")
def feedback(feedback: schemas.Feedback):
    interaction = crud.log_interaction(db, feedback.user_id, feedback.item_id, feedback.feedback_type)
    
    item = db.query(Item).filter(Item.id == feedback.item_id).first()
    popularity_score = getattr(item, "popularity_score", 0)
    if feedback.feedback_type == "like":
        popularity_score += 1
    elif feedback.feedback_type == "view":
        popularity_score += 0.5
    elif feedback.feedback_type == "share":
        popularity_score += 0.2
    popularity_score = popularity_score

    db.commit()
    db.refresh(item)

    return {
        "status": "ok",
        "interaction_id": interaction.id,
        "updated_score": popularity_score
    }


@app.get("/v1/reco/explanations")
def explanations(user_id: int, top_k: int = 10):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"user_id": user_id, "explanations": []}

    rec_content = engine.recommend_content(user.tags , top_k=top_k*2)
    rec_cf = engine.recommend_cf(user.id, top_k=top_k*2)
    rec_pop = engine.popularity_scores

    combined_scores = {}
    for item_id in set([r["item_id"] for r in rec_content] + [r["item_id"] for r in rec_cf] + list(rec_pop.keys())):
        c = next((r["score"] for r in rec_content if r["item_id"] == item_id), 0)
        f = next((r["score"] for r in rec_cf if r["item_id"] == item_id), 0)
        p = rec_pop.get(item_id, 0)
        combined_scores[item_id] = 0.5*c + 0.3*f + 0.2*p

    sorted_items = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    explanations_list = []
    for item_id, score in sorted_items[:top_k]:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            continue
        creator_id = item.creator_id
        creator = db.query(User).filter(User.id == creator_id).first()
        reasons = []
        if item_id in [r["item_id"] for r in rec_content]:
            reasons.append("Matches your interests (content-based)")
        if item_id in [r["item_id"] for r in rec_cf]:
            reasons.append("Liked by similar users (collaborative filtering)")
        if item_id in rec_pop:
            reasons.append(f"Popular in community/block (popularity={rec_pop[item_id]:.2f})")
        
        explanations_list.append({
            "item_id": item.id,
            "title": item.title,
            "description": item.description,
            "tags": item.tags,
            "score": score,
            "reasons": reasons,
            "creator_name": creator.name if creator else "Unknown",
            "community": creator.community if creator else "Unknown"
        })

        if creator :
            print(creator)

    return {"user_id": user_id, "explanations": explanations_list}

