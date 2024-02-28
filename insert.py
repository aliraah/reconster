import sys
import pymongo
from pymongo import MongoClient
import time
import pytz
from datetime import datetime

# Connect to MongoDB
client = MongoClient("CONNECTION-STRING") # Add your connection string here
db = client.assets # Replace "assets" with your collection name

# Get current time in UTC
current_time_utc = datetime.utcnow()

# Convert UTC time to a specific timezone
timezone = pytz.timezone('Europe/Berlin')  # Replace'Europe/Berlin' your timezone
current_time_timezone = current_time_utc.replace(tzinfo=pytz.utc).astimezone(timezone)

# Format the time with timezone
pretty_time = current_time_timezone.strftime("%d. %b. %Y %H:%M %Z")

# Check if the command-line arguments are provided correctly
if len(sys.argv) != 3:
    print("Usage: python3 myscript.py /path/to/all-subs.txt org")
    sys.exit(1)

# Extract the directory path and organization name from the command-line arguments
directory_path = sys.argv[1]
organization = sys.argv[2]

collection = db[organization]

# Read subdomains from file
with open(f'{directory_path}', 'r') as file:
    new_subdomains = set(file.read().splitlines())

# Query existing subdomains from MongoDB
existing_subdomains = set(doc['subdomain'] for doc in collection.find({}, {'subdomain': 1}))

# Identify new subdomains
non_duplicate_subdomains = new_subdomains - existing_subdomains

# Insert non-duplicate subdomains into MongoDB
if non_duplicate_subdomains:
    new_docs = [{'subdomain': subdomain, 'org': organization, 'status': '', 'added': pretty_time, 'last_update': ''} for subdomain in non_duplicate_subdomains]
    collection.insert_many(new_docs)
    print(f"{len(non_duplicate_subdomains)} new subdomains inserted.")
else:
    print("No new subdomains to insert.")