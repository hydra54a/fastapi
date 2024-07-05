from sqlalchemy import Column, String,Date, BIGINT, ForeignKey, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.sql import func


# Replace with your MySQL database credentials
DATABASE_URL: str = f"mysql://root:$3rVerus1!@localhost:3306/facetek"

Base = declarative_base()
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)

class login(Base):
    __tablename__ = "login"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    

class logout(Base):
    __tablename__ = "logout"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class users(Base):
    __tablename__ = "users"
    id = Column(BIGINT, primary_key=True, index=True)
    status = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class cameras(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    address = Column(String(255))
    type = Column(String(25))
    created_at = Column(DateTime(timezone=True), server_default=func.now())  
   
    

class userProfile(Base):
    __tablename__ = "userProfile"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"),nullable=False)
    firstName = Column(String(100))
    middleName = Column(String(100))
    lastName = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    mobileNumber = Column(String(20))
    bdate = Column(Date)
    gender = Column(String(1))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class userAddress(Base):
    __tablename__ = "userAddress"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"),nullable=False) 
    country = Column(String(255)) 
    street = Column(String(500))
    city = Column(String(255))
    state = Column(String(255))
    zipCode = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class userDepartment(Base):
    __tablename__ = "userDepartment"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"),nullable=False) 
    Department = Column(String(150)) 
    userLevel = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class userEmergencyContact(Base):
    __tablename__ = "userEmergencyContact"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"),nullable=False)
    firstName = Column(String(100))
    middleName = Column(String(100))
    lastName = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    mobileNumber = Column(String(20))
    bdate = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
class userEmergencyContactAddress(Base):
    __tablename__ = "userEmergencyContactAddress"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"),nullable=False) 
    emergencyContact_user_id = Column(BIGINT, ForeignKey("userEmergencyContact.id"),nullable=False) 
    country = Column(String(255)) 
    street = Column(String(500))
    city = Column(String(255))
    state = Column(String(255))
    zipCode = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())



class userBucket(Base):
    __tablename__ = "userS3"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"),nullable=False)
    s3_id = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
# Define relationships after all classes are defined
users.profiles = relationship("userProfile", back_populates="user")
users.addresses = relationship("userAddress", back_populates="user")
users.departments = relationship("userDepartment", back_populates="user")
users.emergency_contacts = relationship("userEmergencyContact", back_populates="user")
users.buckets = relationship("userBucket", back_populates="user")

userProfile.user = relationship("users", back_populates="profiles")
userAddress.user = relationship("users", back_populates="addresses")
userDepartment.user = relationship("users", back_populates="departments")
userEmergencyContact.user = relationship("users", back_populates="emergency_contacts")
userEmergencyContact.addresses = relationship("userEmergencyContactAddress", back_populates="emergency_contact")
userEmergencyContactAddress.emergency_contact = relationship("userEmergencyContact", back_populates="addresses")
userBucket.user = relationship("users", back_populates="buckets")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
