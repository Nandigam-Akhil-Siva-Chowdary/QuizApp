"""
Quick script to fix the quiz_questions collection schema issue.
Run this once to drop the broken collection and apply the new migration.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizapp.settings')
django.setup()

from pymongo import MongoClient
from django.conf import settings
from django.core.management import call_command

def main():
    print("=" * 60)
    print("Fixing QuizQuestion schema issue...")
    print("=" * 60)
    
    # Connect to MongoDB
    db_settings = settings.DATABASES['default']
    client_options = db_settings.get('CLIENT', {})
    host = client_options.get('host', 'localhost')
    port = client_options.get('port', 27017)
    db_name = db_settings.get('NAME', 'QuizApp')
    
    print(f"\nConnecting to MongoDB at {host}:{port}, database: {db_name}")
    
    try:
        client = MongoClient(host, port)
        db = client[db_name]
        
        # Drop the quiz_questions collection (it has wrong schema)
        if 'quiz_questions' in db.list_collection_names():
            print("\nDropping quiz_questions collection...")
            db.drop_collection('quiz_questions')
            print("✓ Collection dropped")
        else:
            print("\nNo quiz_questions collection found (already clean)")
        
        # Also drop quiz_answers if it exists (foreign key references)
        if 'quiz_answers' in db.list_collection_names():
            print("\nDropping quiz_answers collection (depends on quiz_questions)...")
            db.drop_collection('quiz_answers')
            print("✓ Collection dropped")
        
        client.close()
        
        print("\n" + "=" * 60)
        print("Running migrations to recreate with correct schema...")
        print("=" * 60)
        
        # Run migrations
        call_command('migrate', 'quiz', verbosity=2)
        
        print("\n" + "=" * 60)
        print("✓ Database fixed successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Restart your server if it's still running")
        print("2. Create quizzes with multiple questions without errors")
        print()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nIf MongoDB connection failed, make sure:")
        print("1. MongoDB is running")
        print("2. Connection settings in settings.py are correct")
        sys.exit(1)

if __name__ == '__main__':
    main()

