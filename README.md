# QuotationManagementAPI

Python FastAPI backend for Quotation Management System with **Vector Embeddings** and **RAG-based Natural Language Q&A**. This system allows you to store quotation data and query it using natural language questions.

## Features

- 🔍 **Natural Language Q&A**: Ask questions about quotations in plain English
- 🧠 **Vector Embeddings**: Uses sentence transformers for semantic search
- 🗄️ **ChromaDB**: Persistent vector database for fast retrieval
- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 📊 **Comprehensive Data Model**: Supports customer, quotation, and item tracking
- 🔄 **Bulk Operations**: Add multiple quotations efficiently

## Architecture

This system implements a **Retrieval Augmented Generation (RAG)** architecture:

1. **Data Ingestion**: Quotation data is converted to text and embedded using `sentence-transformers`
2. **Vector Storage**: Embeddings are stored in ChromaDB for efficient semantic search
3. **Query Processing**: Natural language questions are embedded and used to find similar quotations
4. **Answer Generation**: Relevant quotations are retrieved and formatted into natural language answers

## Technology Stack

- **FastAPI**: REST API framework
- **SQLAlchemy**: Database ORM
- **Sentence Transformers**: Vector embeddings (model: all-MiniLM-L6-v2)
- **ChromaDB**: Vector database
- **Pydantic**: Data validation

## Installation

```bash
# Clone the repository
git clone https://github.com/bsuraj23/QuotationManagementAPI.git
cd QuotationManagementAPI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Run the API server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Access API Documentation

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Add Single Quotation

```bash
curl -X POST "http://localhost:8000/quotations/add" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "customername": "John Industries",
    "customerphone": "+91-9876543210",
    "customeremail": "john@industries.com",
    "quotationcode": "QT-2025-001",
    "quptationstatus": "pending",
    "quotationtotalamount": 15000.00,
    "itemname": "Bearing 6205",
    "itembrand": "SKF",
    "itemspecifications": "Deep groove ball bearing",
    "itemquantity": 50,
    "itemsellingprice": 300.00,
    "sellername": "Indispare"
  }'
```

### 2. Query Using Natural Language

```bash
# Simple GET query
curl "http://localhost:8000/query-simple?question=What quotations do we have for bearings?"

# POST query with more options
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show me quotations for John Industries",
    "n_results": 5
  }'
```

### 3. Example Natural Language Questions

- "What quotations do we have for customer John?"
- "Show me all items with price above 10000"
- "Which quotations are pending?"
- "What items did we quote for bearings?"
- "Show me quotations from seller Indispare"
- "What are the most expensive items?"
- "Which customers have the most quotations?"

### 4. Bulk Add Quotations

```bash
curl -X POST "http://localhost:8000/quotations/bulk-add" \
  -H "Content-Type: application/json" \
  -d '[{
    "id": 1,
    "customername": "ABC Corp",
    "itemname": "Bearing",
    "itemsellingprice": 500
  },
  {
    "id": 2,
    "customername": "XYZ Ltd",
    "itemname": "Gear",
    "itemsellingprice": 750
  }]'
```

### 5. Get Statistics

```bash
curl "http://localhost:8000/stats"
```

## Database Schema

The system uses the following fields from your quotation_items table:

- **Customer Info**: customername, customerphone, customeremail, customerid, customercode
- **Quotation Info**: quotationid, quotationcode, quptationstatus, quotationtotalamount, quotationtermsconditions
- **Item Info**: itemname, itemspecifications, itembrand, itemquantity, itemdeliverydate
- **Pricing**: itemlistingprice, itemsellerdiscount, itemcustomerdiscount, itempurchaseprice, itemsellingprice
- **Additional**: itemproductid, itemhsncode, itemuom, itemtaxpercent
- **Seller Info**: sellername, sellerphone

## How Vector Embeddings Work

1. **Text Creation**: Each quotation item is converted to a searchable text format:
   ```
   Customer: John Industries | Email: john@industries.com | Item: Bearing 6205 | Brand: SKF | Selling Price: 300.00
   ```

2. **Embedding Generation**: The text is converted to a 384-dimensional vector using sentence-transformers

3. **Storage**: Vectors are stored in ChromaDB with metadata

4. **Query**: Your question is also converted to a vector and compared with stored vectors using cosine similarity

5. **Retrieval**: The most similar quotations are retrieved and formatted into an answer

## Use Cases

- **Sales Teams**: Quickly find quotations by customer, product, or status
- **Customer Support**: Answer customer queries about their quotations
- **Analytics**: Discover patterns in quotation data
- **Reporting**: Generate insights from historical quotation data

## Project Structure

```
QuotationManagementAPI/
├── app/
│   ├── models.py              # SQLAlchemy database models
│   └── embedding_service.py   # Vector embedding and RAG service
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

## Contributing

Feel free to open issues or submit pull requests!

## License

MIT License
