from dataclasses import dataclass


@dataclass(frozen=True)
class Dimensions:
    x: float
    y: float
    z: float = 0.0
