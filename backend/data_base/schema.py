from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: datetime
    path: str


class User(BaseModel):
    id: int
    email: str
    username: str
    fd_number: Optional[str]
    password_hash: str
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


class FireDepartmentResponse(BaseModel):
    id: int
    title: str
    address: str


class CreateFireDepartmentRequest(BaseModel):
    title: str
    address: str
    users_ids: Optional[List[int]]


class UpdateFireDepartmentRequest(BaseModel):
    firedepartment_id: int
    fields: Dict[str, Any]


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
    start_work_day: datetime
    finish_work_day: datetime
    work_day_range: int
    week_day_range: int


class CreateWorktypeRequest(BaseModel):
    title: str
    start_work_day: datetime
    finish_work_day: datetime
    work_day_range: int
    week_day_range: int
    humans_ids: Optional[List[int]]


class UpdateWorktypeRequest(BaseModel):
    worktype_id: int
    fields: Dict[str, Any]


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


class CreateHumanRequest(BaseModel):
    title: str
    phone_1: Optional[str]
    phone_2: Optional[str]
    is_firefigher: bool
    work_day: str
    start_vacation: str
    finish_vacation: str
    rank_id: int
    position_id: int
    worktype_id: int
    emergencies_ids: Optional[List[int]]


class UpdateHumanRequest(BaseModel):
    human_id: int
    fields: Dict[str, Any]


class EmergencyResponse(BaseModel):
    id: int
    title: str
    description: str
    urgent: bool


class CreateEmergencyRequest(BaseModel):
    title: str
    description: str
    urgent: bool
    tags_ids: Optional[List[int]]
    humans_ids: Optional[List[int]]
    shorts_ids: Optional[List[int]]
    calls_ids: Optional[List[int]]


class UpdateEmergencyRequest(BaseModel):
    emergency_id: int
    fields: Dict[str, Any]


class CallResponse(BaseModel):
    id: int
    start: datetime
    finish: datetime
    info: Optional[str]


class CreateCallRequest(BaseModel):
    start: datetime
    finish: datetime
    emergency_id: int
    info: Optional[str]


class UpdateCallRequest(BaseModel):
    call_id: int
    fields: Dict[str, Any]
