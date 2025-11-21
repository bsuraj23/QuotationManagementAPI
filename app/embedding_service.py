from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class QuotationEmbeddingService:
    """Service for creating and querying vector embeddings of quotation data"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', persist_directory: str = './chroma_db'):
        """
        Initialize the embedding service
        
        Args:
            model_name: Name of the sentence transformer model
            persist_directory: Directory to persist ChromaDB data
        """
        self.model = SentenceTransformer(model_name)
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        self.collection = self.chroma_client.get_or_create_collection(
            name="quotation_items",
            metadata={"description": "Quotation items with customer, product, and pricing information"}
        )
        logger.info(f"Initialized embedding service with model: {model_name}")
    
    def create_document_text(self, quotation_item: Dict[str, Any]) -> str:
        """Create a searchable text document from quotation item"""
        doc_parts = []
        
        # Customer information
        if quotation_item.get('customername'):
            doc_parts.append(f"Customer: {quotation_item['customername']}")
        if quotation_item.get('customeremail'):
            doc_parts.append(f"Email: {quotation_item['customeremail']}")
        if quotation_item.get('customerphone'):
            doc_parts.append(f"Phone: {quotation_item['customerphone']}")
        
        # Quotation information
        if quotation_item.get('quotationcode'):
            doc_parts.append(f"Quotation Code: {quotation_item['quotationcode']}")
        if quotation_item.get('quptationstatus'):
            doc_parts.append(f"Status: {quotation_item['quptationstatus']}")
        if quotation_item.get('quotationtotalamount'):
            doc_parts.append(f"Total Amount: {quotation_item['quotationtotalamount']}")
        
        # Item information
        if quotation_item.get('itemname'):
            doc_parts.append(f"Item: {quotation_item['itemname']}")
        if quotation_item.get('itembrand'):
            doc_parts.append(f"Brand: {quotation_item['itembrand']}")
        if quotation_item.get('itemspecifications'):
            doc_parts.append(f"Specifications: {quotation_item['itemspecifications']}")
        if quotation_item.get('itemquantity'):
            doc_parts.append(f"Quantity: {quotation_item['itemquantity']}")
        
        # Pricing information
        if quotation_item.get('itemsellingprice'):
            doc_parts.append(f"Selling Price: {quotation_item['itemsellingprice']}")
        if quotation_item.get('itemlistingprice'):
            doc_parts.append(f"Listing Price: {quotation_item['itemlistingprice']}")
        
        # Seller information
        if quotation_item.get('sellername'):
            doc_parts.append(f"Seller: {quotation_item['sellername']}")
        
        return " | ".join(doc_parts)
    
    def add_quotation_item(self, quotation_item: Dict[str, Any]) -> None:
        """
        Add a quotation item to the vector database
        
        Args:
            quotation_item: Dictionary containing quotation item data
        """
        try:
            # Create document text
            doc_text = self.create_document_text(quotation_item)
            
            # Generate embedding
            embedding = self.model.encode(doc_text).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[doc_text],
                metadatas=[quotation_item],
                ids=[str(quotation_item.get('id', quotation_item.get('quotationcode', 'unknown')))]
            )
            logger.info(f"Added quotation item {quotation_item.get('id')} to vector database")
        except Exception as e:
            logger.error(f"Error adding quotation item: {str(e)}")
            raise
    
    def bulk_add_quotation_items(self, quotation_items: List[Dict[str, Any]]) -> None:
        """
        Add multiple quotation items in bulk
        
        Args:
            quotation_items: List of quotation item dictionaries
        """
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        for item in quotation_items:
            doc_text = self.create_document_text(item)
            documents.append(doc_text)
            embeddings.append(self.model.encode(doc_text).tolist())
            metadatas.append(item)
            ids.append(str(item.get('id', item.get('quotationcode', f'item_{len(ids)}'))))
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(quotation_items)} quotation items to vector database")
    
    def query(self, question: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query the vector database with a natural language question
        
        Args:
            question: Natural language question
            n_results: Number of results to return
            
        Returns:
            Dictionary containing results and metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.model.encode(question).tolist()
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            return {
                'question': question,
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else [],
                'distances': results['distances'][0] if results['distances'] else [],
                'count': len(results['documents'][0]) if results['documents'] else 0
            }
        except Exception as e:
            logger.error(f"Error querying vector database: {str(e)}")
            raise
    
    def generate_answer(self, question: str, n_results: int = 5) -> str:
        """
        Generate a natural language answer based on query results
        
        Args:
            question: Natural language question
            n_results: Number of results to consider
            
        Returns:
            Generated answer as string
        """
        results = self.query(question, n_results)
        
        if results['count'] == 0:
            return "I couldn't find any relevant information for your question."
        
        # Build answer from top results
        answer_parts = [f"Based on the quotation data, here's what I found:\n"]
        
        for idx, (doc, metadata, distance) in enumerate(zip(
            results['documents'], 
            results['metadatas'],
            results['distances']
        ), 1):
            # Add relevant information from each result
            answer_parts.append(f"\n{idx}. ")
            if metadata.get('quotationcode'):
                answer_parts.append(f"Quotation {metadata['quotationcode']}: ")
            if metadata.get('itemname'):
                answer_parts.append(f"{metadata['itemname']} ")
            if metadata.get('customername'):
                answer_parts.append(f"for {metadata['customername']} ")
            if metadata.get('itemsellingprice'):
                answer_parts.append(f"at ₹{metadata['itemsellingprice']} ")
            if metadata.get('quptationstatus'):
                answer_parts.append(f"(Status: {metadata['quptationstatus']})")
        
        return "".join(answer_parts)
    
    def delete_by_id(self, item_id: str) -> None:
        """Delete a quotation item from the vector database"""
        try:
            self.collection.delete(ids=[str(item_id)])
            logger.info(f"Deleted quotation item {item_id} from vector database")
        except Exception as e:
            logger.error(f"Error deleting quotation item: {str(e)}")
            raise
    
    def get_collection_count(self) -> int:
        """Get the number of items in the collection"""
        return self.collection.count()
