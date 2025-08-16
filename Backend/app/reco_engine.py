import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from . import crud
import implicit
from scipy.sparse import coo_matrix
from collections import Counter

class RecoEngine:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.item_embeddings = None
        self.items = []

        self.cf_model = implicit.als.AlternatingLeastSquares(factors=50, iterations=10)
        self.user_map = {}
        self.item_map = {}
        self.interactions_matrix = None

        self.popularity_scores = {}

    def fit_content_embeddings(self, db):
        self.items = crud.get_items(db)
        texts = [item.description for item in self.items]
        self.item_embeddings = normalize(self.embedding_model.encode(texts))

    def recommend_content(self, user_tags: str, top_k=10):
        if self.item_embeddings is None or len(self.item_embeddings) == 0:
            return []

        user_vec = normalize(self.embedding_model.encode([user_tags]))
        scores = np.dot(self.item_embeddings, user_vec.T).flatten()

        top_indices = scores.argsort()[::-1][:top_k]
        recommendations = []
        for i in top_indices:
            item = self.items[i]
            tag_overlap = len(set(user_tags.split(",")).intersection(set(item.tags.split(","))))
            combined_score = float(scores[i]) + 0.05 * tag_overlap  # small boost for matching tags
            recommendations.append({"item_id": item.id, "score": combined_score, "reason": "matches your interests"})
        return recommendations

    def fit_cf(self, db):
        interactions = db.query(crud.models.Interaction).all()
        user_ids = list({i.user_id for i in interactions})
        item_ids = list({i.item_id for i in interactions})
        self.user_map = {uid: idx for idx, uid in enumerate(user_ids)}
        self.item_map = {iid: idx for idx, iid in enumerate(item_ids)}

        rows, cols, data = [], [], []
        for i in interactions:
            rows.append(self.user_map[i.user_id])
            cols.append(self.item_map[i.item_id])
            data.append(1)

        self.interactions_matrix = coo_matrix((data, (cols, rows)), shape=(len(item_ids), len(user_ids)))
        self.cf_model.fit(self.interactions_matrix)

    def recommend_cf(self, user_id, top_k=10):
        if user_id not in self.user_map:
            return []

        user_idx = self.user_map[user_id]
        scores = self.cf_model.recommend(
            user_idx, self.interactions_matrix.T, N=top_k, filter_already_liked_items=False
        )

        item_ids_list = list(self.item_map.keys())
        recommendations = []
        for tup in scores:
            if isinstance(tup, (tuple, list)) and len(tup) == 2:
                item_idx, score = tup
                item_id = item_ids_list[item_idx]
                recommendations.append({"item_id": item_id, "score": float(score), "reason": "based on similar users"})
        return recommendations


    def compute_popularity(self, db):
        items = crud.get_items(db)
        interactions = db.query(crud.models.Interaction).all()
        pop_dict = {item.id: 0 for item in items}

        for i in interactions:
            pop_dict[i.item_id] += 1

        for item in items:
            if not item.created_at:
                continue  

            days_old = (datetime.utcnow() - item.created_at).days

            days_old = max(days_old, 0)

            recency_boost = 1 / (1 + days_old)
            pop_dict[item.id] += recency_boost


        self.popularity_scores = pop_dict


    def recommend_popular(self, user, top_k=10):
        sorted_items = sorted(
            self.popularity_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []
        creator_counter = Counter()
        for item_id, score in sorted_items:
            item = next((it for it in self.items if it.id == item_id), None)
            if not item:
                continue
            if item.tags.lower() in ['spam','low-quality']:
                continue
            if item.creator_id == user.id:
                continue
            if creator_counter[item.creator_id] >= 2: 
                continue

            recommendations.append({"item_id": item.id, "score": float(score), "reason": "popular in your community/block"})
            creator_counter[item.creator_id] += 1
            if len(recommendations) >= top_k:
                break
        return recommendations

    def recommend_hybrid(self, db, user, top_k=10):
        rec_content = {r['item_id']: r['score'] for r in self.recommend_content(user.tags, top_k=top_k*2)}
        rec_cf = {r['item_id']: r['score'] for r in self.recommend_cf(user.id, top_k=top_k*2)}
        rec_pop = {r['item_id']: r['score'] for r in self.recommend_popular(user, top_k=top_k*2)}

        combined_scores = {}
        for item_id in set(list(rec_content.keys()) + list(rec_cf.keys()) + list(rec_pop.keys())):
            c = rec_content.get(item_id, 0)
            f = rec_cf.get(item_id, 0)
            p = rec_pop.get(item_id, 0)
            combined_scores[item_id] = 0.5*c + 0.3*f + 0.2*p

        safe_items = []
        creator_counter = Counter()
        for item_id, score in sorted(combined_scores.items(), key=lambda x: x[1], reverse=True):
            item = next((it for it in self.items if it.id == item_id), None)
            if not item:
                continue
            if item.tags.lower() in ['spam','low-quality']:
                continue
            if item.creator_id == user.id:
                continue
            if creator_counter[item.creator_id] >= 2:
                continue
            safe_items.append({"item_id": item.id, "score": float(score), "reason": "recommended for you"})
            creator_counter[item.creator_id] += 1
            if len(safe_items) >= top_k:
                break
        return safe_items

    def recommend_cold_start(self, db, user, top_k=10):
        rec_pop = self.recommend_popular(user, top_k=50)
        rec_content = self.recommend_content(user.tags, top_k=50)
        combined = {r['item_id']: r['score'] for r in rec_pop + rec_content if r['item_id'] not in [item.id for item in self.items if item.creator_id==user.id]}
        sorted_items = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return [{"item_id": item_id, "score": float(score), "reason": "popular or matches interests"} for item_id, score in sorted_items[:top_k]]
