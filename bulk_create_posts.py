from apps.post.models import Post  # Replace `myapp` with your app's name
from faker import Faker
import random

fake = Faker()

LOCATION_ID = 2
USER_ID = 1
CATEGORY_ID = 2

def bulk_create_posts(batch_size=5000, total_posts=100000):
    created_count = 0

    while created_count < total_posts:
        batch = []
        for _ in range(batch_size):
            batch.append(Post(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=3),
                laddered=fake.boolean(),
                status=random.choice([choice[0] for choice in Post.Status.choices]),
                category_id=CATEGORY_ID,
                user_id=USER_ID,
                location_id=LOCATION_ID,
                created_at=fake.date_time_between(start_date='-1y', end_date='now')
            ))

        Post.objects.bulk_create(batch)

        created_count += len(batch)
        print(f"{created_count}/{total_posts} posts created...")

    print("Bulk creation of posts completed!")

# Trigger the bulk creation
bulk_create_posts(batch_size=5000, total_posts=100)
