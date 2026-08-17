from atlas.machines.machine import Machine


class MachineValidator:

    def validate(self, machine: Machine) -> list[str]:
        errors: list[str] = []

        if machine.motion.envelope_x < machine.bed.width:
            errors.append("Motion X envelope is smaller than the build plate.")

        if machine.motion.envelope_y < machine.bed.depth:
            errors.append("Motion Y envelope is smaller than the build plate.")

        if machine.frame.width < machine.bed.width:
            errors.append("Frame width is smaller than the build plate.")

        if machine.frame.depth < machine.bed.depth:
            errors.append("Frame depth is smaller than the build plate.")

        return errors
