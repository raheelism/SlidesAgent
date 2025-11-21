from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import json
from llm_client import LLMClient
from slide_generator import SlideGenerator

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ContentRequest(BaseModel):
    topic: str
    context: str
    num_slides: int = 5
    university: str
    subject: str
    lecturer: str

class PPTXRequest(BaseModel):
    data: dict

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/generate_content")
async def generate_content(request: ContentRequest):
    try:
        llm_client = LLMClient()
        print(f"Generating content for topic: {request.topic}")
        
        content_data = llm_client.generate_slide_content(
            request.topic, 
            request.context, 
            request.num_slides,
            request.university,
            request.subject,
            request.lecturer
        )
        
        return content_data

    except Exception as e:
        print(f"Error generating content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_pptx")
async def create_pptx(request: PPTXRequest):
    try:
        slide_generator = SlideGenerator()
        data = request.data
        
        print(f"Creating PPTX for topic: {data.get('topic')}")
        
        filename = f"generated_slides.pptx"
        output_path = os.path.join("static", "downloads", filename)
        
        slide_generator.create_presentation(data, output_path)
        
        return {
            "message": "Slides generated successfully", 
            "download_url": f"/static/downloads/{filename}"
        }

    except Exception as e:
        print(f"Error creating PPTX: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
