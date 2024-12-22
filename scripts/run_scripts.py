import os
import sys

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.create_tables import create_tables
from scripts.check_users import check_users

def main():
    print("Creating tables...")
    create_tables()
    
    print("\nChecking users...")
    check_users()

if __name__ == "__main__":
    main() 