from dataclasses import dataclass


@dataclass
class Dimensions:
    x: float
    y: float
    z: float


@dataclass
class Machine:
    workspace: Dimensions
    frame: Dimensions