from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import os
import uvicorn
# import uuid
import shortuuid

from coverpage_generator import *

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <html>
        <head>
            <title>Generate Coverpage</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        </head>
        <body>
            <nav>
                <div class="nav-wrapper">
                <a href="#" class="brand-logo center">Coverpage Generator</a>
                </div>
            </nav>
            <div class="container">
                <form id="cover">
                <div>
                <div class="input-field inline">
                    <input id="id" type="text" required>
                    <label for="id">ID</label>
                    <span class="helper-text" validate>e.g. 18PHR053</span>
                </div>
                </div>
                <div>
                <div class="input-field inline">
                    <input id="subdate" type="text" required>
                    <label for="subdate">Submission date</label>
                    <span class="helper-text" validate>e.g. 01-06-2023</span>
                    <div class="right" style="margin-top: 8px">
                        <button class="btn waves-effect waves-light" type="submit" name="action">Download</button>
                    </div>
                </div>
                </div>
                </form>

                <!-- Progress/Loader -->
                <div id="loader">
                    <div class="spinner-layer spinner-green">
                        <div class="circle-clipper left">
                        <div class="circle"></div>
                        </div><div class="gap-patch">
                        <div class="circle"></div>
                        </div><div class="circle-clipper right">
                        <div class="circle"></div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                $('#loader').hide();


                var host = "https://" + $(location).attr('hostname') + "/";

               /* $.get( "/api", {
                     course_title: "Pharmaceutical Technology - II Lab", 
                     course_code: "PHR360" ,
                     id: "",
                     teacher_name: "Md. Shafiqul Islam",
                     teacher_designation: "Assistant Professor",
                     date: date
                     } ); */
            $('#cover').submit(function(e){
                e.preventDefault();
                var id = $('#id').val();
                var date = $('#subdate').val();
                $('#loader').show();

                jQuery.ajax({
                url: '/api', 
                method: 'GET', 
                data: {
                     course_title: "Pharmaceutical Technology - II Lab", 
                     course_code: "PHR360" ,
                     id: id,
                     teacher_name: "Md. Shafiqul Islam",
                     teacher_designation: "Assistant Professor",
                     date: date
                },
                success: function(response) {
                    $('#loader').hide();
                    console.log(response.download_url);
                    window.location.href = host + response.download_url;
                },
                error: function(xhr, status, error) {
                    // Handle errors
                    console.error(error);
                }
                });
            });

            </script>
        </body>
    </html>
    """

@app.get("/api")
async def create_cover(id: str, course_code: str, course_title: str, teacher_name: str, teacher_designation: str, date: str):
    document = Document("./template/Lab Report Template.docx")

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
    download_url = f"./downloads/lab_report_coverpage_{id}.docx"
    document.save(download_url)

    return {"download_url": download_url}



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