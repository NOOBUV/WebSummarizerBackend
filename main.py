from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from webCrawler import WebCrawler
from summarizer import summarize_content
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

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
