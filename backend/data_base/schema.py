import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    email: str
    username: str
    fd_number: str
    secret_key: str
    created_at: str
    last_used: Optional[str] = None


# Модель для запроса создания пользователя
class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str
    fd_number: int


class LoginUserRequest(BaseModel):
    email: str
    password: str


# Модель для ответа с информацией
class InfoResponse(BaseModel):
    message: str
    user_id: int
    username: str
    timestamp: str


class Tag(BaseModel):
    id: int
    title: str
    
    model_config = ConfigDict(from_attributes=True)


class Short(BaseModel):
    id: int
    title: str
    explanation: Optional[str]
    into_new_line: bool
    
    model_config = ConfigDict(from_attributes=True)


class Rank(BaseModel):
    id: int
    title: str
    priority: int
    
    model_config = ConfigDict(from_attributes=True)


class Position(BaseModel):
    id: int
    title: str
    
    model_config = ConfigDict(from_attributes=True)


class Worktype(BaseModel):
    id: int
    title: str
    start_work_day: datetime.datetime
    finish_work_day: datetime.datetime
    work_day_range: int
    week_day_range: int
    
    model_config = ConfigDict(from_attributes=True)


class Human(BaseModel):
    id: int
    title: str
    phone_1: Optional[str]
    phone_2: Optional[str]
    is_firefigher: bool
    # work_day: datetime.date
    # start_vacation: datetime.date
    # finish_vacation: datetime.date
    # worktype: 'Worktype'
    # position: 'Position'
    # rank: 'Rank'
    
    model_config = ConfigDict(from_attributes=True)


class Emergency(BaseModel):
    id: int
    title: str
    description: str
    urgent: bool
    
    model_config = ConfigDict(from_attributes=True)


class Calls(BaseModel):
    id: int
    start: datetime.date
    finish: datetime.date
    info: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CallResponse(BaseModel):
    title: str
    description: Optional[str]
    humans: Optional[List[Human]]
    shorts: Optional[List[Short]]
