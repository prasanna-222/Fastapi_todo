from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = []

class Student(BaseModel):
    name: str
    age: int
    grade: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

@app.get("/students")
def get_students():
    return students

@app.head("/students")
def head_students():
    return {"X-Total-students": len(students)}

@app.options("/students")
def options_students():
    return {
        "allowed_methods": ["Get", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
    }

@app.post("/students")
def create_student(student: Student):
    students.append(student.dict())
    return {"message": "Student added", "data": "student"}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if 0 <= student_id < len(students):
        return students[student_id]
    raise HTTPException(status_code=404, detail="Student not found")

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if 0 <= student_id < len(students):
        students[student_id] = student.dict()
        return {"message": "Student update", "data": student}
    raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{student_id}")
def partial_update_student(student_id: int, student: Student):
    if 0 <= student_id < len(students):
        current_data = students[student_id]
        update_data = student.dict(exclude_unset=True)
        current_data.update(update_data)
        students[student_id] = current_data
        return {"message": "Student partially update", "data": current_data}
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if 0 <= student_id < len(students):
        removed = students.pop(student_id)
        return {"message": "Student delete", "data": removed}
    raise HTTPException(status_code=404, detail="Student not found")

@app.get("/search")
def search_students(name: str = None):
    if name:
        results = [s for s in students if s["name"].lower() == name.lower()]
        return {"results": results}
    return {"message": "No name provided"}

def common_dependency():
    return {"note": "Common dependency injected"}

@app.get("/check")
def check(dep=Depends(common_dependency)):
    return dep
