from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Define your MySQL database connection string
DATABASE_URL = "mysql://root:$3rVerus1!@localhost:3306/facetek"

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create MetaData object
metadata = MetaData()

try:
    # Reflect all tables from the database using the engine
    metadata.reflect(bind=engine)

    # Get all table names
    table_names = metadata.tables.keys()

    # Define delete order respecting dependencies
    delete_order = ['userEmergencyContactAddress','userEmergencyContact','userS3','userDepartment', 'userProfile', 'userAddress', 'users']

    # Iterate through each table name and delete all rows
    for table_name in delete_order:
        if table_name in table_names:
            # Load each table dynamically
            table = Table(table_name, metadata, autoload=True)

            # Delete all rows from the table
            session.query(table).delete()

    # Commit changes and close the session
    session.commit()

except Exception as e:
    # Rollback changes if any error occurs
    session.rollback()
    raise e

finally:
    # Close the session
    session.close()