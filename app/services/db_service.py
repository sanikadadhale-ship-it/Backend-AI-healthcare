from bson import ObjectId

def fix_object_id(doc):
    """Converts MongoDB _id ObjectId into string id"""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
    return doc

def fix_object_id_list(docs):
    """Converts MongoDB _id in list of documents"""
    return [fix_object_id(doc) for doc in docs]
