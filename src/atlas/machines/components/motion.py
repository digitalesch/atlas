from dataclasses import dataclass


@dataclass(frozen=True)
class CoreXY:
    envelope_x: float
    envelope_y: float
