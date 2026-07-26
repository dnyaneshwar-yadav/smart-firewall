from firewall.database import Database

db = Database()

db.create_tables()

print("Database Created Successfully!")

db.close()
