import pickle
from sqlalchemy.orm import Session
from Backend.app import database, reco_engine, crud
import os

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def main():
    db: Session = database.SessionLocal()
    
    engine = reco_engine.RecoEngine()

    print("Training content-based embeddings...")
    engine.fit_content_embeddings(db)
    with open(f"{MODEL_DIR}/content_items.pkl", "wb") as f:
        pickle.dump(engine.items, f)
    with open(f"{MODEL_DIR}/content_embeddings.pkl", "wb") as f:
        pickle.dump(engine.item_embeddings, f)
    print("Content embeddings saved!")

    print("Training collaborative filtering model...")
    engine.fit_cf(db)
    with open(f"{MODEL_DIR}/cf_model.pkl", "wb") as f:
        pickle.dump(engine.cf_model, f)
    with open(f"{MODEL_DIR}/cf_user_map.pkl", "wb") as f:
        pickle.dump(engine.user_map, f)
    with open(f"{MODEL_DIR}/cf_item_map.pkl", "wb") as f:
        pickle.dump(engine.item_map, f)
    print("Collaborative filtering model saved!")

    print("Computing popularity and recency scores...")
    # engine.compute_popularity(db)
    # with open(f"{MODEL_DIR}/popularity_scores.pkl", "wb") as f:
    #     pickle.dump(engine.popularity_scores, f)
    # print("Popularity scores saved!")

    print("Training complete. All artifacts saved in the 'models/' folder!")

if __name__ == "__main__":
    main()
