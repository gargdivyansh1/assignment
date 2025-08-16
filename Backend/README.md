# flatZ Backend

flatZ is a recommendation platform for community events and activities. This backend provides REST APIs, data management, and recommendation logic using collaborative filtering and content-based models.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Data Pipeline](#data-pipeline)
- [Models Used](#models-used)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [How to Extend](#how-to-extend)
- [Development & Testing](#development--testing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

The backend is built with **FastAPI** and provides:
- Personalized recommendations for users
- Explanations for recommendations
- Feedback collection for continuous improvement

It uses a combination of collaborative filtering, content-based filtering, and popularity-based models.

---

## Architecture

```
Backend/
├── app/                # FastAPI application code
│   ├── main.py         # API endpoints
│   ├── crud.py         # CRUD operations
│   ├── database.py     # Database setup (SQLite/SQLAlchemy)
│   ├── models.py       # ORM models
│   ├── schemas.py      # Pydantic schemas
│   ├── reco_engine.py  # Recommendation logic
│   └── __init__.py
├── data/               # Raw data files
│   ├── users.csv
│   ├── items.csv
│   ├── interactions.csv
│   └── making_data.py  # Data preprocessing script
├── models/             # Pre-trained model files
│   ├── cf_model.pkl
│   ├── cf_user_map.pkl
│   ├── cf_item_map.pkl
│   ├── content_embeddings.pkl
│   ├── content_items.pkl
│   └── popularity_scores.pkl
├── scripts/
│   └── train_models.py # Model training script
├── requirements.txt    # Python dependencies
├── package.json        # (Optional) Node dependencies
└── README.md           # This file
```

---

## Data Pipeline

1. **Raw Data Collection:**  
   - `users.csv`: User profiles (user_id, demographics, etc.)
   - `items.csv`: Event/activity metadata (item_id, title, description, tags, etc.)
   - `interactions.csv`: User-item interactions (user_id, item_id, interaction_type, timestamp)

2. **Preprocessing:**  
   - Run `data/making_data.py` to clean and format data for model training.

3. **Model Training:**  
   - Execute `scripts/train_models.py` to train collaborative filtering and content-based models.
   - Outputs are saved in `models/`.

4. **Serving Recommendations:**  
   - FastAPI endpoints in `app/main.py` use `reco_engine.py` to generate recommendations using trained models.

---

## Models Used

- **Collaborative Filtering (CF):**
  - Matrix factorization using implicit feedback.
  - Model files: `cf_model.pkl`, `cf_user_map.pkl`, `cf_item_map.pkl`.
  - Used for personalized recommendations based on user-item interaction patterns.

- **Content-Based Filtering:**
  - Item embeddings generated from item metadata (e.g., tags, descriptions).
  - Model files: `content_embeddings.pkl`, `content_items.pkl`.
  - Used for recommendations when user history is sparse.

- **Popularity-Based:**
  - Simple popularity scores for cold-start recommendations.
  - Model file: `popularity_scores.pkl`.

---

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd flatZ/Backend
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Prepare data:**
   - Place your CSV files in `data/`.
   - Run preprocessing if needed:
     ```sh
     python data/making_data.py
     ```

4. **Train models (optional, if not using provided models):**
   ```sh
   python scripts/train_models.py
   ```

5. **Start the API server:**
   ```sh
   uvicorn app.main:app --reload
   ```

---

## API Endpoints

| Endpoint                  | Method | Description                                 |
|---------------------------|--------|---------------------------------------------|
| `/v1/reco/homefeed`       | GET    | Get personalized recommendations for a user |
| `/v1/reco/explanations`   | GET    | Get explanations for recommendations        |
| `/v1/reco/feedback`       | POST   | Submit user feedback for an item            |

- See `app/main.py` for full endpoint details and request/response formats.
- Interactive API docs available at [http://localhost:8000/docs](http://localhost:8000/docs) after starting the server.

---

## How to Extend

- **Add new data:** Update CSVs in `data/` and retrain models.
- **Add new recommendation logic:** Modify `app/reco_engine.py`.
- **Add new endpoints:** Edit `app/main.py` and define schemas in `app/schemas.py`.
- **Integrate with frontend:** Connect API endpoints to your frontend application.

---

## Development & Testing

- Use VS Code for development.
- Run unit tests (if available) using:
  ```sh
  pytest
  ```
- Debug and inspect API using Swagger UI at `/docs`.

---

## Contact

For questions or contributions, open an issue or pull request