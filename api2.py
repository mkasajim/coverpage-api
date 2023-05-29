from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import uvicorn
# import uuid
import shortuuid

from coverpage_generator import *

app = FastAPI()


@app.get("/api")
async def create_cover(id: str, course_code: str, course_title: str, teacher_name: str, teacher_designation: str, date: str):
    document = Document("./Lab Report Template.docx")

    # unique_id = shortuuid.uuid()

    regex1 = re.compile("<course title>")
    regex2 = re.compile("<course code>")
    regex3 = re.compile("<id>")
    regex4 = re.compile("<teacher name>")
    regex5 = re.compile("<teacher designation>")
    regex6 = re.compile("<date>")

    replace_str1 = course_title
    replace_str2 = course_code
    replace_str3 = id
    replace_str4 = teacher_name
    replace_str5 = teacher_designation
    replace_str6 = date

    document_replace_text(document, regex1, replace_str1)
    document_replace_text(document, regex2, replace_str2)
    document_replace_text(document, regex3, replace_str3)
    document_replace_text(document, regex4, replace_str4)
    document_replace_text(document, regex5, replace_str5)
    document_replace_text(document, regex6, replace_str6)

    # download_url = f"downloads/{unique_id}_lab_report_coverpage.docx"
    download_url = f"./downloads/lab_report_coverpage.docx"
    document.save(download_url)

    return {"download_url": download_url}


@app.get("/")
def read_root():
    return {"Hello": "API"}

@app.get("/favicon.ico")
async def download_file():
    file_path = f"favicon.ico"
    return FileResponse(file_path)

@app.get("/downloads/{file_name}")
async def download_file(file_name: str):
    file_path = f"downloads/{file_name}"
    return FileResponse(file_path)

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 8080))
    uvicorn.run(app, host="0.0.0.0", port=PORT)