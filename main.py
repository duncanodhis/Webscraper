from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from typing import List
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UrlsRequest(BaseModel):
    urls: List[str]

@app.post("/scrape")
async def scrape_urls(request: UrlsRequest):
    try:
        # Load HTML documents
        loader = AsyncHtmlLoader(request.urls)
        docs = loader.load()

        # Transform HTML to text
        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)

        # Return transformed documents as JSON
        response_data = [{"page_content": doc.page_content} for doc in docs_transformed]
        return JSONResponse(content={"docs": response_data})
    except Exception as e:
        logger.error("An error occurred: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
