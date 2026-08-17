from dataclasses import dataclass


@dataclass(frozen=True)
class Toolhead:
    width: float
    depth: float
    offset_x: float = 0.0
    offset_y: float = 0.0
