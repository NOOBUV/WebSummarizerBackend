from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import tempfile
import stat
from webCrawler import WebCrawler
from summarizer import summarize_content

temp_dir = './tmp'

# Ensure the directory exists
os.makedirs(temp_dir, exist_ok=True)

# Set full permissions for the user (read, write, execute)
os.chmod(temp_dir, stat.S_IRWXU)

# Set the custom temporary directory
tempfile.tempdir = temp_dir
app = FastAPI()


class URLRequest(BaseModel):
    url: str


@app.post("/crawl_and_summarize")
def crawl_and_summarize(request: URLRequest):
    crawler = WebCrawler(request.url)
    urls = crawler.crawl()

    if not urls:
        raise HTTPException(status_code=404, detail="No URLs found.")

    summaries = summarize_content(urls)
    return {"summaries": summaries}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
