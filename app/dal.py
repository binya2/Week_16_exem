import pymongo

from config import settings
from connection import get_database


class DAL:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[settings.COLLECTION]

    # 1
    def get_engineering_high_salary_employees(self):
        projection = {
            'employee_id': 1,
            'name': 1,
            'salary': 1,
            '_id': 0
        }
        query = {
            "job_role.department": "Engineering",
            'salary': {'$gt': 65000}
        }
        result = self.collection.find(query, projection)
        return list(serialize_docs(result))

    # 2
    def get_employees_by_age_and_role(self):
        projection = {'_id': 0}
        query = {
            "age": {"$gte": 30, "$lte": 45},
            "job_role.title":
                {"$in": ["Specialist", "Engineer"]}
        }

        result = self.collection.find(query, projection)
        return list(serialize_docs(result))

    # 3
    def get_top_seniority_employees_excluding_hr(self):
        projection = {}
        query = {
            'job_role.department': {"$ne": "HR"}
        }
        result = self.collection.find(query, projection).limit(7).sort([('years_at_company', pymongo.DESCENDING)])
        result = [{**doc, '_id': str(doc['_id'])} for doc in result]
        return list(serialize_docs(result))

    # 4
    def get_employees_by_age_or_seniority(self):
        projection = {'_id': 0,
                      'name': 1,
                      'years_at_company': 1,
                      'age': 1}
        query = {
            '$or': [
                {'age': {'$gt': 50}},
                {'years_at_company': {'$lt': 3}}
            ]
        }
        result = self.collection.find(query, projection)
        return list(serialize_docs(result))

    # 5
    def get_managers_excluding_departments(self):
        projection = {}
        query = {
            'job_role.title': 'Manager',
            'job_role.department': {'$nin': ['Sales', 'Marketing']}
        }
        result = self.collection.find(query, projection)
        result = [{**doc, '_id': str(doc['_id'])} for doc in result]
        return list(serialize_docs(result))

    # 6
    def get_employees_by_lastname_and_age(self):
        projection = {
            'name': 1,
            'age': 1,
            'job_role.department': 1,
            '_id': 0
        }
        query = {
            'name': {'$regex': '(Nelson|Wright)$', '$options': 'i'},
            'age': {'$lt': 35}}

        result = self.collection.find(query, projection)
        return list(serialize_docs(result))


def serialize_doc(doc: dict):
    if doc and "_id" in doc:
        doc["_id"] = doc["_id"].__str__()
    return doc


def serialize_docs(docs: list[dict]):
    return [serialize_doc(doc) for doc in docs]

# db = DAL()
# print(db.get_employees_by_age_and_role())
