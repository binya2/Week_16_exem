from fastapi import APIRouter
from dal import DAL

db = DAL()
router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/engineering/high-salary" )
def get_engineering_high_salary():
     return {'data' :db.get_engineering_high_salary_employees()}

@router.get("/by-age-and-role" )
def get_by_age_and_role():
    return {'data':db.get_employees_by_age_and_role()}

@router.get("/top-seniority" )
def get_top_seniority():
    return {'data' :db.get_top_seniority_employees_excluding_hr()}

@router.get("/engineering/age-or-seniority")
def get_engineering_age_or_seniority():
    return {'data' :db.get_employees_by_age_or_seniority()}

@router.get("/managers/excluding-departments")
def get_managers_excluding_departments():
    return {'data' :db.get_managers_excluding_departments()}

@router.get("/by-lastname-and-age")
def get_by_lastname_and_age():
    return {'data' :db.get_employees_by_lastname_and_age()}



