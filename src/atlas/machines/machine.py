from dataclasses import dataclass

from atlas.machines.components.bed import BuildPlate
from atlas.machines.components.frame import BoxedTowerFrame
from atlas.machines.components.motion import CoreXY
from atlas.machines.components.toolhead import Toolhead


@dataclass(frozen=True)
class Machine:
    name: str
    frame: BoxedTowerFrame | None = None
    motion: CoreXY | None = None
    bed: BuildPlate | None = None
    toolhead: Toolhead | None = None
