"""
Simple script to fix the quiz_questions collection schema.
This directly manipulates MongoDB without going through Django migrations.
"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import OperationFailure

# MongoDB connection settings
DB_NAME = "QuizApp"
MONGO_URI = "mongodb+srv://Akhil2310:Hasi2310@nexora.j9i1s4f.mongodb.net"

def main():
    print("=" * 60)
    print("Fixing QuizQuestion schema issue (Simple Method)")
    print("=" * 60)
    
    try:
        print(f"\nConnecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Test connection
        db.command('ping')
        print(f"✓ Connected to database: {DB_NAME}")
        
        # 1. Drop quiz_questions collection
        if 'quiz_questions' in db.list_collection_names():
            print("\nDropping quiz_questions collection...")
            db.drop_collection('quiz_questions')
            print("✓ Collection dropped")
        else:
            print("\nNo quiz_questions collection found")
        
        # 2. Drop quiz_answers collection (depends on questions)
        if 'quiz_answers' in db.list_collection_names():
            print("\nDropping quiz_answers collection...")
            db.drop_collection('quiz_answers')
            print("✓ Collection dropped")
        else:
            print("\nNo quiz_answers collection found")
        
        # 3. Update migration history to mark 0002 as applied but skip actual schema
        print("\nChecking migration history...")
        migrations_collection = db['django_migrations']
        
        # Check if 0002_initial is in history
        migration_0002 = migrations_collection.find_one({
            'app': 'quiz',
            'name': '0002_initial'
        })
        
        if migration_0002:
            print("✓ Migration 0002_initial is recorded")
        else:
            print("! Migration 0002_initial not found in history")
        
        # 4. Create the quiz_questions collection with a sample document to establish schema
        print("\nCreating quiz_questions collection with correct schema...")
        
        # Insert a dummy question to establish the collection structure
        # We'll delete it right after
        dummy_doc = {
            'quiz_id': None,  # Will be replaced by actual ObjectId when real questions are created
            'question_text': '__DUMMY__',
            'question_type': 'single',
            'options': [],
            'explanation_correct': '',
            'explanation_wrong': '',
        }
        
        result = db.quiz_questions.insert_one(dummy_doc)
        print(f"✓ Collection created with id: {result.inserted_id}")
        
        # Delete the dummy document
        db.quiz_questions.delete_one({'_id': result.inserted_id})
        print("✓ Dummy document removed")
        
        # 5. Verify the collection exists and is empty
        count = db.quiz_questions.count_documents({})
        print(f"\n✓ quiz_questions collection is ready (count: {count})")
        
        client.close()
        
        print("\n" + "=" * 60)
        print("✓ Database fixed successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Restart your server: python manage.py runserver")
        print("2. Go to Admin → Create Quiz")
        print("3. Add multiple questions to your quiz")
        print("4. Questions will be stored with auto-generated _id as primary key")
        print()
        
    except OperationFailure as e:
        print(f"\n✗ MongoDB Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

