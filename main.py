from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db import getDB, lifespan

templates = Jinja2Templates(directory="templates")
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def home(db=Depends(getDB)):
    cur = await db.execute("SELECT * FROM students ORDER BY stuid;")
    return await cur.fetchall()

@app.get("/students/list/template")
async def stuList(request: Request, db=Depends(getDB)):
    cur = await db.execute("SELECT * FROM students ORDER BY stuid;")
    data = await cur.fetchall()
    return templates.TemplateResponse(name="studentList.html", request=request, context={"students": data})

@app.get("/student/add")
async def stuAddPage(request: Request):
    return templates.TemplateResponse(name="studentAdd.html", request=request)


@app.post("/student/create")
async def stuCreate(stuid: int = Form(...), name: str = Form(...), height: int = Form(...), db=Depends(getDB)):
    await db.execute("INSERT INTO students (stuid, name, height) VALUES (%s, %s, %s);", (stuid, name, height))
    return RedirectResponse(url="/students/list/template", status_code=303)

@app.get("/student/edit/{stuid}")
async def stuEdit(stuid: int, request: Request, db=Depends(getDB)):
    cur = await db.execute("SELECT * FROM students WHERE stuid=%s;", (stuid,))
    data = await cur.fetchone()
    return templates.TemplateResponse(name="studentEdit.html", request=request, context={"data": data})

@app.post("/student/update")
async def stuUpdate(stuid: int = Form(...), name: str = Form(...), height: int = Form(...), db=Depends(getDB)):
    print(stuid, name, height)
    await db.execute("UPDATE students SET name=%s, height=%s WHERE stuid=%s;", (name, height, stuid))
    return RedirectResponse(url="/students/list/template", status_code=303)

@app.get("/student/delete/{stuid}")
async def stuDelete(stuid: int, db=Depends(getDB)):
    await db.execute("DELETE FROM students WHERE stuid=%s;", (stuid,))
    return RedirectResponse(url="/students/list/template", status_code=303)