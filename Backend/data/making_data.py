import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from Backend.app import database, models
from Backend.app.database import Base

users = []
num_users = 1000

for i in range(1, num_users + 1):
    users.append({
        "id": i,
        "name": f"User{i}",
        "community": random.choice(["Block A","Block B","Block C","Block D"]),
        "tags": ",".join(random.sample(["fitness","food","pets","shopping","movies","events","park","hygiene","view"], 3)),
        "signup_date": (datetime.today() - timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d")
    })

users_df = pd.DataFrame(users)
users_df.to_csv("Backend/data/users.csv", index=False)
print("Generated users.csv")

categories = {
    "Yoga Class": ("Morning yoga session for fitness and relaxation", "fitness,wellness"),
    "Food Festival": ("Block B food festival featuring local cuisine", "food,event"),
    "Pet Meetup": ("Meet and share fun activities for your pets", "pets,community"),
    "Block Movie Night": ("Outdoor movie screening every Friday evening", "movies,entertainment"),
    "Gardening Workshop": ("Learn to plant seasonal vegetables & flowers", "gardening,workshop"),
    "Pottery Class": ("Weekly pottery classes for beginners", "art,crafts"),
    "Book Club": ("Monthly book discussions on contemporary literature", "books,community"),
    "Cycling Group": ("Weekend cycling tours around the city", "sports,outdoors"),
    "Tech Talk": ("Presentations on emerging technologies", "technology,education"),
    "Cooking Workshop": ("Hands-on cooking workshops for healthy meals", "food,education")
}

items = []
num_items = 1000
creator_ids = list(range(201, 251))
start_date = datetime(2025, 1, 1)

for i in range(101, 101 + num_items):
    title, (base_description, tags) = random.choice(list(categories.items()))
    
    description = f"{base_description} ({random.choice(['Beginner Friendly', 'Weekly Session', 'Join Now', 'Limited Slots'])})"
    
    creator_id = random.choice(creator_ids)
    days_ago = random.randint(0, 230)
    created_at = (start_date + timedelta(days=days_ago)).strftime("%Y-%m-%d")
    
    popularity_score = round(random.uniform(0, 10), 1)
    likes_count = random.randint(0, 100)
    views_count = random.randint(0, 500)
    shares_count = random.randint(0, 50)

    items.append([
        i, title, description, tags, creator_id, created_at,
        popularity_score, likes_count, views_count, shares_count
    ])

items_df = pd.DataFrame(
    items, 
    columns=["id","title","description","tags","creator_id","created_at","popularity_score","likes_count","views_count","shares_count"]
)
items_df.to_csv("Backend/data/items.csv", index=False)
print("Generated items.csv with popularity metrics")

interaction_types = ["like","view","share"]
num_interactions = 2000

interactions = []

user_ids = users_df['id'].tolist()
item_ids = items_df['id'].tolist()

for i in range(1, num_interactions + 1):
    user_id = random.choice(user_ids)  
    item_id = random.choice(item_ids)  
    interaction_type = random.choice(interaction_types)
    days_ago = random.randint(0, 230)
    timestamp = (start_date + timedelta(days=days_ago)).strftime("%Y-%m-%d")
    interactions.append([i, user_id, item_id, interaction_type, timestamp])

interactions_df = pd.DataFrame(interactions, columns=["id","user_id","item_id","type","timestamp"])
interactions_df.to_csv("Backend/data/interactions.csv", index=False)
print("Generated interactions.csv")

db = database.SessionLocal()
models.Base.metadata.drop_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)

for _, row in users_df.iterrows():
    db.add(models.User(id=row.id, name=row.name, community=row.community, tags=row.tags))
db.commit()
print("Inserted users into DB")

for _, row in items_df.iterrows():
    db.add(
        models.Item(
            id=row.id,
            title=row.title,
            description=row.description,
            tags=row.tags,
            creator_id=row.creator_id,
            created_at=row.created_at,  
            popularity_score=row.popularity_score,  
            likes_count=row.likes_count,         
            views_count=row.views_count,             
            shares_count=row.shares_count           
        )
    )
    print(row)
db.commit()
print(db)
print("Inserted items into DB with metrics")


for _, row in interactions_df.iterrows():
    db.add(models.Interaction(user_id=row.user_id, item_id=row.item_id, type=row.type, timestamp=row.timestamp))
db.commit()
print("Inserted interactions into DB")

print("Database initialization complete!")