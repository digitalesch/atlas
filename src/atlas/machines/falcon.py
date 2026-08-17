from atlas.machines.machine import Machine
from atlas.machines.components.frame import BoxedTowerFrame
from atlas.machines.components.motion import CoreXY
from atlas.machines.components.bed import BuildPlate
from atlas.machines.components.toolhead import Toolhead

Falcon = Machine(
    name="Falcon",
    frame=BoxedTowerFrame(
        width=560,
        depth=560,
        height=680,
    ),
    motion=CoreXY(
        envelope_x=560,
        envelope_y=560,
    ),
    bed=BuildPlate(
        width=400,
        depth=400,
    ),
    toolhead=Toolhead(
        width=60,
        depth=60,
        offset_x=0,
        offset_y=0,
    ),
)
