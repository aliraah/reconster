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

def read_subdomains_from_file(filename):
    subdomains = []
    with open(filename, 'r') as file:
        for line in file:
            subdomains.append(line.strip())  # Remove newline characters and append to the list
    return subdomains


def update_200():
    filename = directory_path + "/200.txt"
    subdomains_list = read_subdomains_from_file(filename)
    updated_count = 0  # Initialize a counter for updated records

    for subdomain in subdomains_list:
        result = collection.update_one({"subdomain": subdomain}, {"$set": {"status": 200, "last_update": pretty_time}})
        if result.modified_count > 0:
            updated_count += 1
    return updated_count

updated_records_count_200 = update_200()
if updated_records_count_200 > 0:
    print(f"{updated_records_count_200} records with status 200 updated.")



def update_301():
    filename = directory_path + "/301.txt"
    subdomains_list = read_subdomains_from_file(filename)
    updated_count = 0  # Initialize a counter for updated records

    for subdomain in subdomains_list:
        result = collection.update_one({"subdomain": subdomain}, {"$set": {"status": 301, "last_update": pretty_time}})
        if result.modified_count > 0:
            updated_count += 1
    return updated_count

updated_records_count_301 = update_301()
if updated_records_count_301 > 0:
    print(f"{updated_records_count_301} records with status 301 updated.")



def update_302():
    filename = directory_path + "/302.txt"
    subdomains_list = read_subdomains_from_file(filename)
    updated_count = 0  # Initialize a counter for updated records

    for subdomain in subdomains_list:
        result = collection.update_one({"subdomain": subdomain}, {"$set": {"status": 302, "last_update": pretty_time}})
        if result.modified_count > 0:
            updated_count += 1
    return updated_count

updated_records_count_302 = update_302()
if updated_records_count_302 > 0:
    print(f"{updated_records_count_302} records with status 302 updated.")



def update_401():
    filename = directory_path + "/401.txt"
    subdomains_list = read_subdomains_from_file(filename)
    updated_count = 0  # Initialize a counter for updated records

    for subdomain in subdomains_list:
        result = collection.update_one({"subdomain": subdomain}, {"$set": {"status": 401, "last_update": pretty_time}})
        if result.modified_count > 0:
            updated_count += 1
    return updated_count

updated_records_count_401 = update_401()
if updated_records_count_401 > 0:
    print(f"{updated_records_count_401} records with status 401 updated.")



def update_403():
    filename = directory_path + "/403.txt"
    subdomains_list = read_subdomains_from_file(filename)
    updated_count = 0  # Initialize a counter for updated records

    for subdomain in subdomains_list:
        result = collection.update_one({"subdomain": subdomain}, {"$set": {"status": 403, "last_update": pretty_time}})
        if result.modified_count > 0:
            updated_count += 1
    return updated_count

updated_records_count_403 = update_403()
if updated_records_count_403 > 0:
    print(f"{updated_records_count_403} records with status 403 updated.")



def update_404():
    filename = directory_path + "/404.txt"
    subdomains_list = read_subdomains_from_file(filename)
    updated_count = 0  # Initialize a counter for updated records

    for subdomain in subdomains_list:
        result = collection.update_one({"subdomain": subdomain}, {"$set": {"status": 404, "last_update": pretty_time}})
        if result.modified_count > 0:
            updated_count += 1
    return updated_count

updated_records_count_404 = update_404()
if updated_records_count_404 > 0:
    print(f"{updated_records_count_404} records with status 404 updated.")



def update_503():
    filename = directory_path + "/503.txt"
    subdomains_list = read_subdomains_from_file(filename)
    updated_count = 0  # Initialize a counter for updated records

    for subdomain in subdomains_list:
        result = collection.update_one({"subdomain": subdomain}, {"$set": {"status": 503, "last_update": pretty_time}})
        if result.modified_count > 0:
            updated_count += 1
    return updated_count

updated_records_count_503 = update_503()
if updated_records_count_503 > 0:
    print(f"{updated_records_count_503} records with status 503 updated.")