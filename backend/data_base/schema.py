import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    email: str
    username: str
    fd_number: str
    secret_key: str
    created_at: str
    last_used: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str


class UserAuthResponse(UserResponse):
    token: str


class UserRegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    firedepartment_id: Optional[int]


class FireDepartmentResponse(BaseModel):
    id: int
    title: str
    address: str


# Модель для запроса создания пользователя
class CreateUser(BaseModel):
    email: str
    username: str
    password: str
    fd_number: int


class LoginUser(BaseModel):
    email: str
    password: str


class TagResponse(BaseModel):
    id: int
    title: str


class CreateTagRequest(BaseModel):
    title: str
    emergencies_ids: Optional[List[int]]


class UpdateTagRequest(BaseModel):
    tag_id: int
    fields: Dict[str, Any]


class ShortResponse(BaseModel):
    id: int
    title: str
    explanation: Optional[str]
    into_new_line: bool


class CreateShortRequest(BaseModel):
    title: str
    explanation: Optional[str]
    into_new_line: bool
    emergencies_ids: Optional[List[int]]


class UpdateShortRequest(BaseModel):
    short_id: int
    fields: Dict[str, Any]


class RankResponse(BaseModel):
    id: int
    title: str
    priority: int


class CreateRankRequest(BaseModel):
    title: str
    priority: int
    humans_ids: Optional[List[int]]


class UpdateRankRequest(BaseModel):
    rank_id: int
    fields: Dict[str, Any]


class PositionResponse(BaseModel):
    id: int
    title: str


class CreatePositionRequest(BaseModel):
    title: str
    humans_ids: Optional[List[int]]


class UpdatePositionRequest(BaseModel):
    position_id: int
    fields: Dict[str, Any]


class WorktypeResponse(BaseModel):
    id: int
    title: str
    start_work_day: datetime.datetime
    finish_work_day: datetime.datetime
    work_day_range: int
    week_day_range: int


class HumanResponse(BaseModel):
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


class EmergencyResponse(BaseModel):
    id: int
    title: str
    description: str
    urgent: bool


class CallResponse(BaseModel):
    id: int
    start: datetime.date
    finish: datetime.date
    info: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CallResponse(BaseModel):
    title: str
    description: Optional[str]
    # humans: Optional[List[Human]]
    # shorts: Optional[List[Short]]
