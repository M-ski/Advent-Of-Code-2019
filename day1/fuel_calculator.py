from math import floor
from typing import List
import logging as log


def calc_fuel_for_mass(mass: float) -> float:
    fuel = floor(mass / 3) - 2
    log.debug(f'mass={mass} requires fuel={fuel}')
    return fuel if fuel > 0 else 0


def calc_projected_fuel(mass: float) -> float:
    fuel: float = calc_fuel_for_mass(mass)
    log.debug(f'*required fuel for mass={mass} is={fuel}, additional fuel required={fuel > 0}')
    if fuel > 0:
        return fuel + calc_projected_fuel(fuel)
    else:
        return fuel


def log_and_calc_projected_fuel(mass: float) -> float:
    calculated_fuel: float = calc_projected_fuel(mass)
    log.info(f'Total fuel required for component of mass={mass} is={calculated_fuel}')
    return calculated_fuel


if __name__ == '__main__':
    with open('input.txt', 'r') as source:
        component_masses: List[float] = [float(val) for val in source.readlines()]

    log.basicConfig(level=log.INFO)
    computed_fuel: List[float] = [log_and_calc_projected_fuel(component) for component in component_masses]
    total_fuel: float = sum(computed_fuel)
    log.info(f'Fuel required for all components is {total_fuel}.')

