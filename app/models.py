from sqlalchemy import Column, Integer, String, DECIMAL, Date, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class QuotationItem(Base):
    """Database model for quotation items table"""
    __tablename__ = "quotation_items"
    
    # Auto-increment ID (assumed primary key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Customer Information
    customername = Column(String(383), nullable=True)
    customerphone = Column(String(191), nullable=True)
    customeremail = Column(String(191), nullable=True)
    customerid = Column(Integer, nullable=True, default=0)
    customercode = Column(String(100), nullable=True)
    
    # Quotation Information
    quotationid = Column(Integer, nullable=True, default=0)
    quotationcode = Column(String(100), nullable=True)
    quptationstatus = Column(String(100), nullable=True)
    quotationtotalamount = Column(DECIMAL(12, 2), nullable=True, default=0.00)
    quotationtermsconditions = Column(Text, nullable=True)
    quotationsellerremarks = Column(String(100), nullable=True)
    quotationissuedby = Column(String(100), nullable=True, default='indispare')
    quotationcreatedat = Column(TIMESTAMP, nullable=True)
    
    # Item Information
    itemname = Column(String(100), nullable=True)
    itemspecifications = Column(Text, nullable=True)
    itembrand = Column(String(100), nullable=True)
    itemquantity = Column(DECIMAL(12, 2), nullable=True)
    itemdeliverydate = Column(Date, nullable=True)
    itempricedemanded = Column(String(100), nullable=True)
    itempricevalidtill = Column(Date, nullable=True)
    
    # Item Pricing
    itemlistingprice = Column(DECIMAL(12, 2), nullable=True, default=0.00, comment="Listing Price")
    itemsellerdiscount = Column(DECIMAL(12, 2), nullable=True, default=0.00, comment="Seller Discount")
    itemcustomerdiscount = Column(DECIMAL(12, 2), nullable=True, default=0.00, comment="Customer Discount")
    itempurchaseprice = Column(DECIMAL(12, 2), nullable=True, default=0.00, comment="Purchase Price")
    itemsellingprice = Column(DECIMAL(12, 2), nullable=True, default=0.00, comment="Selling Price")
    
    # Item Additional Details
    itemproductid = Column(Integer, nullable=True)
    itemhsncode = Column(String(100), nullable=True)
    itemuom = Column(String(100), nullable=True)
    itemtaxpercent = Column(String(100), nullable=True, default='18')
    
    # Seller Information
    sellername = Column(String(191), nullable=True)
    sellerphone = Column(String(191), nullable=True)
    
    def __repr__(self):
        return f"<QuotationItem(id={self.id}, quotationcode={self.quotationcode}, itemname={self.itemname})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'customername': self.customername,
            'customerphone': self.customerphone,
            'customeremail': self.customeremail,
            'customerid': self.customerid,
            'customercode': self.customercode,
            'quotationid': self.quotationid,
            'quotationcode': self.quotationcode,
            'quptationstatus': self.quptationstatus,
            'quotationtotalamount': float(self.quotationtotalamount) if self.quotationtotalamount else 0.00,
            'quotationtermsconditions': self.quotationtermsconditions,
            'quotationsellerremarks': self.quotationsellerremarks,
            'quotationissuedby': self.quotationissuedby,
            'quotationcreatedat': self.quotationcreatedat.isoformat() if self.quotationcreatedat else None,
            'itemname': self.itemname,
            'itemspecifications': self.itemspecifications,
            'itembrand': self.itembrand,
            'itemquantity': float(self.itemquantity) if self.itemquantity else None,
            'itemdeliverydate': self.itemdeliverydate.isoformat() if self.itemdeliverydate else None,
            'itempricedemanded': self.itempricedemanded,
            'itempricevalidtill': self.itempricevalidtill.isoformat() if self.itempricevalidtill else None,
            'itemlistingprice': float(self.itemlistingprice) if self.itemlistingprice else 0.00,
            'itemsellerdiscount': float(self.itemsellerdiscount) if self.itemsellerdiscount else 0.00,
            'itemcustomerdiscount': float(self.itemcustomerdiscount) if self.itemcustomerdiscount else 0.00,
            'itempurchaseprice': float(self.itempurchaseprice) if self.itempurchaseprice else 0.00,
            'itemsellingprice': float(self.itemsellingprice) if self.itemsellingprice else 0.00,
            'itemproductid': self.itemproductid,
            'itemhsncode': self.itemhsncode,
            'itemuom': self.itemuom,
            'itemtaxpercent': self.itemtaxpercent,
            'sellername': self.sellername,
            'sellerphone': self.sellerphone
        }
