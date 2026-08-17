from dataclasses import dataclass

from atlas.machines.dimensions import Dimensions


@dataclass(frozen=True)
class BoxedTowerFrame:
    width: float
    depth: float
    height: float

    @property
    def dimensions(self) -> Dimensions:
        return Dimensions(
            x=self.width,
            y=self.depth,
            z=self.height,
        )
