from coordinates import Coordinates
import uuid


class MapPoint:
    """Класс - представление точки на карте."""
    def __init__(self, description: str, init_cords: Coordinates, image: str):
        self._descript = description
        self._cords = init_cords
        self._uuid = uuid.uuid4()
        self._image_source = image
