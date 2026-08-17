from dataclasses import dataclass


@dataclass(frozen=True)
class BuildPlate:
    width: float
    depth: float
