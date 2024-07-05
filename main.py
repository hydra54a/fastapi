from fastapi import FastAPI, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional,List
from pydantic import  field_validator
from datetime import datetime, date
from models import SessionLocal, login, users,userProfile,userAddress,userDepartment,userEmergencyContact,userEmergencyContactAddress,userBucket,cameras
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, join

app = FastAPI()

origins = ["http://localhost","http://localhost:3000", "https://faceid.skooltek.co"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ItemCreate(BaseModel):
    name: str
    description: str
class loginCreate(BaseModel):
    uid: str

    
class LoginResponse(BaseModel):
    id: int
    uid: str
    created_at: str
    @field_validator('created_at', mode='before')
    def format_created_at(cls, value):
        # Ensure the value is a datetime object
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value
    class Config:
        orm_mode = True
    
    
class logout(BaseModel):
    uid: str

class LoginQuery(BaseModel):
    uid: Optional[str] = None

class usersCreate(BaseModel):
    status: int

class userCreateResponse(BaseModel):
    id: int
    status: int
    class Config:
        orm_mode = True
        from_attributes = True
class camerasCreate(BaseModel):
    name: str
    address: str
    type: str
class camerasCreateResponse(BaseModel):
    id: int
    name: str
    address: str
    type: str
    class Config:
        # orm_mode = True
        # from_attributes = True
        from_attributes=True
class UserProfileCreate(BaseModel):
    firstName: str
    user_id: int
    middleName: str
    lastName: str
    mobileNumber: str
    email: str
    bdate: str
    gender: str
class UserProfileCreateResponse(BaseModel):
    id: int
    firstName: str
    user_id: int
    middleName: str
    lastName: str
    mobileNumber: str
    email: str
    bdate: str
    gender: str
    class Config:
        orm_mode = True
        from_attributes = True

class UserAddressCreate(BaseModel):
    country: str
    user_id: int
    street: str
    city: str
    state: str
    zipCode: str
class UserAddressCreateResponse(BaseModel):
    id: int
    country: str
    user_id: int
    street: str
    city: str
    state: str
    zipCode: str
    
    class Config:
        # orm_mode = True
        from_attributes = True

class UserDepartmentCreate(BaseModel):
    user_id: int
    Department: str 
    userLevel: str
    
class UserDepartmentCreateResonse(BaseModel):
    id: int
    user_id: int
    Department: str 
    userLevel: str
    class Config:
        orm_mode = True
        from_attributes = True
       
class userEmergencyContactCreate(BaseModel):
    user_id: int
    firstName: str
    middleName: str
    lastName: str
    email: str
    mobileNumber: str
    bdate: str
class userEmergencyContactCreateResponse(BaseModel):
    id: int
    user_id: int
    firstName: str
    middleName: str
    lastName: str
    email: str
    mobileNumber: str
    bdate: str
    class Config:
        orm_mode = True
        from_attributes = True
    
class userEmergencyContactAddressCreate(BaseModel):
    country: str
    user_id: int
    street: str
    city: str
    state: str
    zipCode: str
class userEmergencyContactAddressCreateResponse(BaseModel):
    id: int
    emergencyContact_user_id: int
    country: str
    user_id: int
    street: str
    city: str
    state: str
    zipCode: str
    class Config:
        orm_mode = True
        from_attributes = True
class UserResponse(BaseModel):
    id: int
    status: int
    created_at: str
    profiles: List[UserProfileCreateResponse]
    addresses: List[userEmergencyContactAddressCreateResponse]
    departments: List[UserDepartmentCreateResonse]

    class Config:
        orm_mode = True
        from_attributes = True
class UsersResponse(BaseModel):
    users: List[UserResponse]

    class Config:
        orm_mode = True  
        from_attributes = True
class CameraBase(BaseModel):
    uid: int
    name: str
    description: str
    class Config:
        orm_mode = True
        from_orm = True  # Enable from_orm usage with SQLAlchemy models
        from_attributes = True  # Required when using from_orm with SQLAlchemy models
        

class PaginatedCameras(BaseModel):
    total: int
    items: List[CameraBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def format_date(input_data):
    try:
        # Example: Check if input_data is a dictionary
        if isinstance(input_data, dict):
            date_str = input_data.get('date')  # Assuming 'date' is the key to extract
            # Perform further processing or validation on date_str if needed
            return date_str
            return f"Formatted date: {date_str}"
        
        # Example: Check if input_data is an object with 'date' attribute
        elif hasattr(input_data, 'date'):
            date_str = input_data.date  # Assuming 'date' is an attribute to extract
            # Perform further processing or validation on date_str if needed
            return date_str
            # return f"Formatted date: {date_str}"
        
        else:
            raise ValueError("Input should be a valid dictionary or object to extract fields from")
    
    except Exception as e:
        print(f"Error formatting date: {e}")
        # Handle the error appropriately (logging, returning an error response, etc.)
        return f"Error: {e}"
    
@app.post("/login/", response_model=loginCreate)
def create_login(item: loginCreate, db: Session = Depends(get_db)):
    db_login = login(uid=item.uid)
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login
@app.post("/camera/", response_model=camerasCreate)
def create_camera(item: camerasCreate, db: Session = Depends(get_db)):
    db_camera = cameras(name=item.name,address=item.address,type=item.type)
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera
@app.get("/cameras/", response_model=List[camerasCreate])
def query_cameras(
    id: Optional[int] = None,
    limit: int = Query(default=10, ge=1),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(cameras)

    if id is not None:
        query = query.filter(cameras.uid == id)

    cameras_ = query.offset(offset).limit(limit).all()
    print(f"Fetched {len(cameras_)} items from the database")

    if not cameras_:
        raise HTTPException(status_code=404, detail="No cameras found")

    return cameras_
@app.get("/attendance/")
def attendance():
    data = [
            {
                "date": "06/01/2024",
                "name": "Anthony Derecho",
                "account_type": "Student",
                "department_level": "level 1",
                "entry": "13:05",
                "exit": "23:01",
                "actions": ""
            },
            {
                "date": "06/02/2024",
                "name": "Anthony Derecho",
                "account_type": "Student",
                "department_level": "level 1",
                "entry": "11:08",
                "exit": "20:18",
                "actions": ""
            },
            {
                "date": "06/11/2024",
                "name": "Anthony Derecho",
                "account_type": "Student",
                "department_level": "level 1",
                "entry": "07:45",
                "exit": "11:31",
                "actions": ""
            },
            {
                "date": "06/01/2024",
                "name": "Anthony Derecho",
                "account_type": "Student",
                "department_level": "level 1",
                "entry": "13:05",
                "exit": "23:01",
                "actions": ""
            },
            {
                "date": "06/01/2024",
                "name": "Raphel Derecho",
                "account_type": "Student",
                "department_level": "level 1",
                "entry": "13:09",
                "exit": "23:31",
                "actions": ""
            }
            ]
    return JSONResponse(content=data)

@app.get("/logins/", response_model=List[LoginResponse])
def query_logins(uid: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(login)
    
    if uid is not None:
        query = query.filter(login.uid == uid)
    
    logins = query.all()
    
    if not logins:
        raise HTTPException(status_code=404, detail="No logins found")
    return logins

@app.post("/newuser/")
# @app.post("/newuser/", response_model=userCreateResponse)
def user_create(status:int = Form(...),
                firstName: str = Form(...),
                middleName: str = Form(...),
                lastName: str = Form(...),
                mobileNumber: str = Form(...),
                email: str = Form(...),
                gender: str = Form(...),
                bdate: str = Form(...),
                country: str = Form(...),
                street: str = Form(...),
                city: str = Form(...),
                state: str = Form(...),
                zipCode: str = Form(...),
                Department: str = Form(...),
                userLevel: str = Form(...),
                efirstName: str = Form(..., alias="efirstName"),
                emiddleName: str = Form(..., alias="emiddleName"),
                elastName: str  = Form(..., alias="elastName"),
                eemail: str = Form(..., alias="eemail"),
                emobileNumber: str = Form(..., alias="emobileNumber"),
                ebdate:  str = Form(..., alias="ebdate"),
                ecountry: str = Form(..., alias="ecountry"),
                estreet: str = Form(..., alias="estreet"),
                ecity: str = Form(..., alias="ecity"),
                estate: str = Form(..., alias="estate"),
                ezipCode: str = Form(..., alias="ezipCode"),
                db: Session = Depends(get_db)
            ):
   
    data_dict = {'date': bdate, 'other_field': 'value'}
    edata_dict = {'date': ebdate, 'other_field': 'value'}




       
    newUser = users(status = status)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    newUserProfile = userProfile(
        user_id = newUser.id,
        firstName = firstName, 
        middleName = middleName,
        lastName = lastName,
        email = email,
        mobileNumber = mobileNumber,
        bdate = format_date(data_dict),
        gender = gender
    )
    db.add(newUserProfile)
    db.commit()
    db.refresh(newUserProfile)
    
    newUserAddress = userAddress(
        user_id = newUser.id,
        country=country,
        street = street,
        city=city,
        state=state,
        zipCode=zipCode
    )
    db.add(newUserAddress)
    db.commit()
    db.refresh(newUserAddress)
    
    newUserDept = userDepartment(
        user_id = newUser.id,
        Department = Department,
        userLevel = userLevel
    )
    db.add(newUserDept)
    db.commit()
    db.refresh(newUserDept)
    
    EmergencyContact = userEmergencyContact(
        user_id = newUser.id,
        firstName = efirstName, 
        middleName = emiddleName,
        lastName = elastName,
        email = eemail,
        mobileNumber = emobileNumber,
        bdate = format_date(edata_dict)
    )
    db.add(EmergencyContact)
    db.commit()
    db.refresh(EmergencyContact)
    
    EmergencyContactAddress = userEmergencyContactAddress(
        user_id = newUser.id,
        emergencyContact_user_id = EmergencyContact.id,
        country=ecountry,
        street = estreet,
        city=ecity,
        state=estate,
        zipCode=ezipCode
    )
    db.add(EmergencyContactAddress)
    db.commit()
    db.refresh(EmergencyContactAddress)
    
    
    return {"success": True, "data":{"uid":newUser.id}, "message":"ok"}
@app.get("/users", response_model=List[dict])
async def getAllUsers(db: Session = Depends(get_db)):
    # Define your query using SQLAlchemy's select and join capabilities
    query = (
        select(users.id, users.status, users.created_at, userProfile, userAddress, userDepartment)
        .select_from(users)
        .join(userProfile, users.id == userProfile.user_id)
        .join(userAddress, users.id == userAddress.user_id)
        .join(userDepartment, users.id == userDepartment.user_id)
    )

    results = db.execute(query).fetchall()

    # Process the results into a suitable response format
    user_responses = []
    for result in results:
        user_dict = {
            "id": result[0],
            "status": result[1],
            "created_at": result[2],
            "profiles": {
                "id": result[3].id,
                "user_id": result[3].user_id,
                "firstName": result[3].firstName,
                "middleName": result[3].middleName,
                "lastName": result[3].lastName,
                "email": result[3].email,
                "mobileNumber": result[3].mobileNumber,
                # Add other fields from UserProfile as needed
            },
            "addresses": {
                "id": result[4].id,
                "user_id": result[4].user_id,
                "country": result[4].country,
                "street": result[4].street,
                "city": result[4].city,
                "zipCode": result[4].zipCode,
                # Add other fields from UserAddress as needed
            },
            "departments": {
                "id": result[5].id,
                "user_id": result[5].user_id,
                "department": result[5].Department,
                "level": result[5].userLevel,
                # Add other fields from UserDepartment as needed
            }
        }
        user_responses.append(user_dict)

    return user_responses

    