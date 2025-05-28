import json

class InputData:
    """
    A class to input data from JSON file

    Attributes
    ----------
    n_zones : int
        Number of materials or zones
    n_cells : list[int]
        Numbers of cells per zone
    zone_length : list[float]
        Length of each zone
    sigma_t : list[float]
        Total cross section sigma_t in each zone
    sigma_s : list[float]
        Total scattering cross section sigma_s in each zone
    source : list[float]
        Source q in each zone
    boundary_values: tuple(2)
        Prescribed value on on the left and right endpoints
    supg_tuning_value: float
        Tuning parameter for Petrov-Gallerkin stabilization
    """

    def __init__(self, input_file_path: str):
        self.input_file_path = input_file_path

        expected_fields = {
            "n_zones": int,
            "n_cells": list,
            "zone_length": list,
            "sigma_t": list,
            "source": list,
            "boundary_values": list,

            # optional fields
            # "supg_tuning_value": float,
            # "sigma_s" : list,
        }

        with open(input_file_path, "r") as file:
            json_data = json.load(file)

        for key, ty in expected_fields.items():
            if key not in json_data:
                raise Exception(f"Key {key} not found in input file")

            if not isinstance(json_data[key], ty):
                print(f'Key "{key}" is incorrect type from {input_file_path}')

        self.n_zones = json_data["n_zones"]
        self.n_cells = json_data["n_cells"]
        self.zone_length = json_data["zone_length"]
        self.sigma_t = json_data["sigma_t"]
        self.source = json_data["source"]
        self.boundary_values = tuple(json_data["boundary_values"])

        if "supg_tuning_value" in json_data:
            self.supg_tuning_value = json_data["supg_tuning_value"]

        if "sigma_s" in json_data:
            self.sigma_s = json_data["sigma_s"]

            for s, t in zip(self.sigma_s, self.sigma_t):
                assert s >= 0 and t >= s, "Invalid sigma_s or sigma_t, expected 0 <= sigma_s <= sigma_t for each zone"
