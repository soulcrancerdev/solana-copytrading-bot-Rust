"""Initialize database with schema."""

import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_settings

settings = get_settings()


def init_database():
    """Initialize database with schema."""
    schema_file = Path(__file__).parent.parent / "database" / "schema.sql"
    
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        return False
    
    # Extract connection details from DATABASE_URL
    db_url = settings.database_url
    # Format: postgresql://user:password@host:port/database
    
    try:
        # Use psql if available
        cmd = [
            "psql",
            db_url,
            "-f",
            str(schema_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database initialized successfully!")
            return True
        else:
            print(f"❌ Error initializing database: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("⚠️ psql not found. Please install PostgreSQL client tools.")
        print(f"Alternatively, run the SQL file manually: {schema_file}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    init_database()

