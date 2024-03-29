from pydantic import BaseModel
import datetime


# PRIMARY SCHEMAS

class CvatProject(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class MarkupStatus(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Geolocation(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class MlPurpose(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class System(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class LocationHrz(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class LocationVrt(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Object(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Orientation(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Vector(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# SCHEMAS WITH LINKS

class Dump(BaseModel):
    id: int
    name: str
    description: str
    comment: str
    geolocation_id: int
    geolocation: Geolocation
    system_id: int
    system: System
    ml_purpose_id: int
    ml_purpose: MlPurpose
    created: datetime.datetime

    class Config:
        orm_mode = True


class CvatProjectDump(BaseModel):
    id: int
    dump_id: int
    dump: Dump
    cvat_project_id: int
    cvat_project: CvatProject
    status_id: int
    status: MarkupStatus
    pillar_num: int

    class Config:
        orm_mode = True


class SimulantDump(BaseModel):
    id: int
    dump_id: int
    dump: Dump
    object_id: int
    object: Object
    vector_id: int
    vector: Vector
    locationhrz_id: int
    locationhrz: LocationHrz
    locationvrt_id: int
    locationvrt: LocationVrt
    orientation_id: int
    orientation: Orientation

    class Config:
        orm_mode = True
