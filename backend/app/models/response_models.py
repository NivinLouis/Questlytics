from sqlalchemy import column,Integer,String,DateTime
from database import Base
from database import datetime
class uploadedFile(Base):
    _tablename_="uploaded_files"
    id=column(Integer,primary_key=True,index=True)
    filename=column(String,index=True)
    content_type=column(String)
    upload_time=column(DateTime,default=DateTime.utcnow())
