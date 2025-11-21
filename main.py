from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from app.embedding_service import QuotationEmbeddingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Quotation Management RAG API",
    description="API for managing quotations with vector embeddings and natural language Q&A",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize embedding service
embedding_service = QuotationEmbeddingService()

# Pydantic models
class QuotationItemCreate(BaseModel):
    id: Optional[int] = None
    customername: Optional[str] = None
    customerphone: Optional[str] = None
    customeremail: Optional[str] = None
    customerid: Optional[int] = 0
    customercode: Optional[str] = None
    quotationid: Optional[int] = 0
    quotationcode: Optional[str] = None
    quptationstatus: Optional[str] = None
    quotationtotalamount: Optional[float] = 0.00
    quotationtermsconditions: Optional[str] = None
    quotationsellerremarks: Optional[str] = None
    quotationissuedby: Optional[str] = "indispare"
    quotationcreatedat: Optional[str] = None
    itemname: Optional[str] = None
    itemspecifications: Optional[str] = None
    itembrand: Optional[str] = None
    itemquantity: Optional[float] = None
    itemdeliverydate: Optional[str] = None
    itempricedemanded: Optional[str] = None
    itempricevalidtill: Optional[str] = None
    itemlistingprice: Optional[float] = 0.00
    itemsellerdiscount: Optional[float] = 0.00
    itemcustomerdiscount: Optional[float] = 0.00
    itempurchaseprice: Optional[float] = 0.00
    itemsellingprice: Optional[float] = 0.00
    itemproductid: Optional[int] = None
    itemhsncode: Optional[str] = None
    itemuom: Optional[str] = None
    itemtaxpercent: Optional[str] = "18"
    sellername: Optional[str] = None
    sellerphone: Optional[str] = None

class QueryRequest(BaseModel):
    question: str
    n_results: Optional[int] = 5

class QueryResponse(BaseModel):
    question: str
    answer: str
    documents: List[str]
    count: int

# Routes
@app.get("/")
async def root():
    return {
        "message": "Quotation Management RAG API",
        "version": "1.0.0",
        "endpoints": [
            "/docs",
            "/quotations/add",
            "/quotations/bulk-add",
            "/query",
            "/stats"
        ]
    }

@app.post("/quotations/add")
async def add_quotation(item: QuotationItemCreate):
    """
    Add a single quotation item to the vector database
    """
    try:
        item_dict = item.dict()
        embedding_service.add_quotation_item(item_dict)
        return {
            "status": "success",
            "message": "Quotation item added successfully",
            "item_id": item_dict.get('id') or item_dict.get('quotationcode')
        }
    except Exception as e:
        logger.error(f"Error adding quotation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quotations/bulk-add")
async def bulk_add_quotations(items: List[QuotationItemCreate]):
    """
    Add multiple quotation items in bulk
    """
    try:
        items_list = [item.dict() for item in items]
        embedding_service.bulk_add_quotation_items(items_list)
        return {
            "status": "success",
            "message": f"Added {len(items_list)} quotation items successfully",
            "count": len(items_list)
        }
    except Exception as e:
        logger.error(f"Error in bulk add: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_quotations(query: QueryRequest):
    """
    Query quotations using natural language questions.
    Examples:
    - "What quotations do we have for customer John?"
    - "Show me all items with price above 10000"
    - "Which quotations are pending?"
    - "What items did we quote for bearings?"
    """
    try:
        # Get raw results
        results = embedding_service.query(query.question, query.n_results)
        
        # Generate natural language answer
        answer = embedding_service.generate_answer(query.question, query.n_results)
        
        return QueryResponse(
            question=query.question,
            answer=answer,
            documents=results['documents'],
            count=results['count']
        )
    except Exception as e:
        logger.error(f"Error querying: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query-simple")
async def query_simple(
    question: str = Query(..., description="Natural language question about quotations"),
    n_results: int = Query(5, description="Number of results to return")
):
    """
    Simple GET endpoint for querying (useful for testing)
    """
    try:
        answer = embedding_service.generate_answer(question, n_results)
        return {
            "question": question,
            "answer": answer
        }
    except Exception as e:
        logger.error(f"Error in simple query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/quotations/{item_id}")
async def delete_quotation(item_id: str):
    """
    Delete a quotation item from the vector database
    """
    try:
        embedding_service.delete_by_id(item_id)
        return {
            "status": "success",
            "message": f"Deleted quotation item {item_id}"
        }
    except Exception as e:
        logger.error(f"Error deleting: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """
    Get statistics about the vector database
    """
    try:
        count = embedding_service.get_collection_count()
        return {
            "status": "success",
            "total_items": count,
            "model": "all-MiniLM-L6-v2",
            "vector_db": "ChromaDB"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Quotation Management RAG API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
