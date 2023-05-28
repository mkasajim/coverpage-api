from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from deta import Deta

app = FastAPI()
deta = Deta("d0zJc3BmyosL_tMp9tbNxVuwyVirbRS5J1Xekqpft85v8")  # configure your Deta project 
drive = deta.Drive("template")

@app.get("/", response_class=HTMLResponse)
def render():
    return """
    <form action="/upload" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    """
@app.get("/download")
def download_img():
    res = drive.get("Lab Report Template.docx")
    return StreamingResponse(res.iter_chunks(1024), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")