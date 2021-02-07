from fastapi import APIRouter, Body, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# custom imports
from models import StudentModel

router = APIRouter()

@router.get("/students", response_description="List students")
async def student_list(request: Request):
    students = []
    for student in await request.app.mongodb["students"].find().to_list(length=100):
        students.append(student)
    return students

@router.post("/students", response_description="Add a student")
async def add_student(request: Request, student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student =  await request.app.mongodb["students"].insert_one(student)
    created_student = await request.app.mongodb["students"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

@router.get("/students/{id}", response_description="Get a single student!")
async def get_a_student(request: Request, id: str):
    student = await request.app.mongodb["students"].find_one({"_id": id})
    if student:
        return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student with %s not found"%id)

@router.delete("/students/{id}", response_description="Delete a single student!")
async def delete_student(request: Request, id: str):
    student = await request.app.mongodb["students"].delete_one({"_id": id})
    if student.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student with %s not found"%id)