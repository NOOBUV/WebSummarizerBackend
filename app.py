from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tempfile


tempfile.tempdir = './temp'
app = FastAPI()


class URLRequest(BaseModel):
    url: str


@app.post("/crawl_and_summarize")
def crawl_and_summarize(request: URLRequest):
    return "hello world"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
