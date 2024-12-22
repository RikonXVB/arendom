from config.database import Base, engine
import models.user
import models.product

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables() 