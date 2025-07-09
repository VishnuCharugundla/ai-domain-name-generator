import json
import random
from faker import Faker
from pathlib import Path

fake = Faker()

# Categories and complexity levels
categories = [
    "tech", "food", "fashion", "legal", "health", 
    "finance", "education", "entertainment", "beauty", "real estate"
]

complexity_levels = ["simple", "medium", "complex"]

# Templates for each complexity level
templates = {
    "simple": [
        "A {category} company.",
        "A business focused on {category}."
    ],
    "medium": [
        "A {category} startup aiming to innovate in its domain.",
        "A growing {category} company serving urban customers."
    ],
    "complex": [
        "A {category} platform providing AI-powered solutions for enterprises worldwide.",
        "A {category} business specializing in personalized services and global logistics integration."
    ]
}

def generate_dataset(n=200):
    dataset = []
    for _ in range(n):
        cat = random.choice(categories)
        level = random.choice(complexity_levels)
        template = random.choice(templates[level])
        description = template.format(category=cat)

        dataset.append({
            "business_description": description,
            "category": cat,
            "complexity_level": level
        })

    return dataset

def save_dataset(dataset, filename="data/synthetic_dataset_v1.json"):
    Path("data").mkdir(exist_ok=True)
    with open(filename, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"✅ Dataset saved to {filename}")

if __name__ == "__main__":
    data = generate_dataset(n=200)
    save_dataset(data)
