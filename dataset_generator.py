import pandas as pd
import random

data = []

for i in range(2000):

    length = random.randint(20, 80)
    width = random.randint(20, 60)

    area = length * width

    if area < 800:
        bedrooms = 1
        bathrooms = 1
        balcony = 0

    elif area < 1500:
        bedrooms = 2
        bathrooms = 2
        balcony = 1

    elif area < 2500:
        bedrooms = 3
        bathrooms = 2
        balcony = 1

    else:
        bedrooms = 4
        bathrooms = 3
        balcony = 2

    data.append([length, width, area, bedrooms, bathrooms, balcony])

df = pd.DataFrame(data, columns=[
    "length",
    "width",
    "area",
    "bedrooms",
    "bathrooms",
    "balcony"
])

df.to_csv("house_dataset.csv", index=False)

print("Dataset generated successfully!")