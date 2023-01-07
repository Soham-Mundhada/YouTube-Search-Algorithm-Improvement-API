# importing module
from pymongo import MongoClient
from datetime import date

def insert_data(tags,file):
    print("iserting data ....")
    # creation of MongoClient
    client=MongoClient()

    # Connect with the portnumber and host
    client = MongoClient('mongodb://localhost:27017/')

    # Access database
    mydatabase = client['youtube_api']
    
    # Access collection of the database
    mycollection=mydatabase['top50']
    #FETCHING THE COLLECTION TOP50 FROM YOUTUBE_API DB
    tags=tags.lower()
    # dictionary to be added in the database
    rec={
        "time":str(date.today().strftime("%d/%m/%Y")), # dd/mm/yyyy
        "title": tags,
        "data": file,
    }
    #print(type(rec))
    # inserting the data in the database
    mycollection.insert_one(rec)
    #print(rec)

def get_data(tags):
    print("getting data ..... ")
    # creation of MongoClient
    client=MongoClient()

    # Connect with the portnumber and host
    client = MongoClient('mongodb://localhost:27017/')

    # Access database
    mydatabase = client['youtube_api']

    # Access collection of the database
    mycollection=mydatabase['top50']

    tags=tags.lower()
    element=mycollection.find_one({"title":tags})
    print("we get data.........")
    if element is None: 
        return ""
    return element['data']

