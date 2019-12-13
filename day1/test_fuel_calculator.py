from typing import List
from unittest import TestCase

from day1.fuel_calculator import calc_fuel_for_mass, calc_projected_fuel, log_and_calc_projected_fuel


class Tests(TestCase):
    def test_calc_projected_fuel(self):
        print(f'\n-- Testing recursive fuel need --')
        component_masses: List[float] = [14, 1969, 100756]
        expected_fuel: List[float] = [2, 966, 50346]
        computed_fuel: List[float] = [calc_projected_fuel(component) for component in component_masses]
        for i in range(0, len(component_masses)):
            self.assertEqual(expected_fuel[i], computed_fuel[i],
                             f'Component of mass={component_masses[i]} recursive fuel need not computed as expected. '
                             + f'Expected={expected_fuel[i]}, computed={computed_fuel[i]}')
        computed_fuel_2: List[float] = [log_and_calc_projected_fuel(component) for component in component_masses]
        self.assertEqual(computed_fuel, computed_fuel_2)

    def test_calc_fuel_for_mass(self):
        print(f'-- Testing pure fuel calculation --')
        component_masses: List[float] = [12, 14, 1969, 100756]
        expected_fuel: List[float] = [2, 2, 654, 33583]
        computed_fuel: List[float] = [calc_fuel_for_mass(component) for component in component_masses]
        for i in range(0, len(component_masses)):
            self.assertEqual(expected_fuel[i], computed_fuel[i], f'Component of ' +
                             f'mass={component_masses[i]} fuel not computed as expected. ' +
                             f'Expected={expected_fuel[i]}, computed={computed_fuel[i]}')
