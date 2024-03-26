from enum import Enum

from .dump_models.dump_model import DumpModel
from .dump_models.geolocation_model import GeolocationModel
from .simulant_models.simulant_dump_model import SimulantDumpModel
from .dump_models.system_model import SystemModel
from .dump_models.ml_purpose_model import MlPurposeModel
from .simulant_models.objects_model import ObjectModel
from .simulant_models.vector_model import VectorModel
from .simulant_models.location_hrz_model import LocationHrzModel
from .simulant_models.location_vrt_model import LocationVrtModel
from .simulant_models.orientation_model import OrientationModel
from .cvat_project_dump_models.cvat_project_dump_model import (CvatProjectDumpModel,
                                                               CvatProjectModel,
                                                               MarkupStatusModel)
from .base_model import Base


class Models(Enum):
    BaseModel = Base
    DumpModel = DumpModel
    SimulantDumpModel = SimulantDumpModel
    GeolocationModel = GeolocationModel
    SystemModel = SystemModel
    ObjectModel = ObjectModel
    VectorModel = VectorModel
    LocationHrzModel = LocationHrzModel
    LocationVrtModel = LocationVrtModel
    OrientationModel = OrientationModel
    MlPurposeModel = MlPurposeModel
    CvatProjectDumpModel = CvatProjectDumpModel
    CvatProjectModel = CvatProjectModel
    MarkupStatusModel = MarkupStatusModel
