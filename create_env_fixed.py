# create_env_fixed.py
import os

# Create .env file with proper encoding
with open('.env', 'w', encoding='utf-8') as f:
    f.write('GEMINI_API_KEY=AIzaSyAkGgbqhI-1frAudws0C7r-T50g1QFusXM\n')
    f.write('DATABASE_URL=sqlite:///./data/recipes.db\n')
    f.write('REDIS_URL=redis://localhost:6379\n')

print("Created .env file successfully!")
print("Contents:")
with open('.env', 'r', encoding='utf-8') as f:
    print(f.read())

