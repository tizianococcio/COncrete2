from typing import Dict, Any, List
from model import predict_emissions
from scipy.optimize import direct, dual_annealing, differential_evolution, shgo


class CO2Optimizer:
    """
    A class for optimizing CO2 emissions in a concrete production process.

    Attributes:
        model: Trained CO2 emissions prediction model.
        default_bounds: Dictionary containing default parameter bounds for optimization.
        fixed_params: Dictionary containing parameters which should be maintained 
            fixed during optimization.
    """
    def __init__(self, model):
        """
        Initialize CO2Optimizer with a trained model.

        Args:
            model: Trained CO2 emissions prediction model.
        """
        self.model = model
        self.default_bounds = {
            'temperature': (15, 30),  # degrees Celsius
            'humidity': (30, 80),  # percentage (%)
            'curing_time': (12, 48),  # hours
            'energy_consumption': (100, 500),  # kilowatt-hours (kWh)
            'dosing_events': (1, 10),  # Number of dosing events
            'active_power_curve': (100, 500),  # watts (W)
            'truck_drum_rotation_speed': (10, 30),  # rotations per minute (rpm)
            'truck_drum_duration': (10, 60),  # minutes
            'cement': (300, 400),  # kg
            'sand': (500, 1000),  # kg
            'gravel': (1000, 1500)  # kg
        }
        self.fixed_params = {}

    def set_fixed_param(self, param_name: str, value: float) -> None:
        """
        Set a parameter which should be maintained fixed during optimization.

        Args:
            param_name (str): Name of the parameter.
            value (float): Value of the parameter.
        Raises:
            ValueError: If the parameter name is not valid.
        """
        if param_name in self.default_bounds:
            self.fixed_params[param_name] = value
        else:
            raise ValueError(f"Parameter {param_name} is not a valid parameter")

    def predict_co2_emissions(self, inputs: Dict[str, Any]) -> float:
        """
        Predicts CO2 emissions for the given values. This is used to train the optimizer model.

        Args:
            inputs (dict): Dictionary of input values

        Returns:
            float: Predicted CO2 emissions.            
        """
        return predict_emissions(self.model, inputs)

    def objective_function(self, params: List[float], fixed_params={}) -> float:
        """
        Objective function for optimization.

        Args:
            params: List of parameter values.
            fixed_params: Dictionary of fixed parameters.

        Returns:
            float: Predicted CO2 emissions.
        """
        opt_params = [param for param in self.default_bounds if param not in fixed_params]
        param_dict = dict(zip(opt_params, params))

        # Insert amount_produced_m3 after energy_consumption
        energy_consumption_index = opt_params.index('energy_consumption') + 1
        keys = list(param_dict.keys())
        before = {k: param_dict[k] for k in keys[:energy_consumption_index]}
        after = {k: param_dict[k] for k in keys[energy_consumption_index:]}

        before.update({'amount_produced_m3': 1})
        before.update(after)        
        return self.predict_co2_emissions(before)

    def optimize(self, algorithm='direct') -> tuple[Dict, float]:
        """
        Optimize parameters to minimize CO2 emissions using differential optimization.

        Returns:
            dict: Optimal parameter values.
            float: Minimum CO2 emissions.
        """
        # Adjust bounds by excluding fixed parameters
        bounds = [self.default_bounds[param] for param in self.default_bounds if param not in self.fixed_params]

        # Run the optimization
        if algorithm == 'dual_annealing':
            result = dual_annealing(self.objective_function, bounds, args=(self.fixed_params,), seed=42)
        elif algorithm == 'differential_evolution':
            result = differential_evolution(self.objective_function, bounds, args=(self.fixed_params,), seed=42)
        elif algorithm == 'shgo':
            result = shgo(self.objective_function, bounds, args=(self.fixed_params,))
        else:
            # default to 'direct' algorithm
            result = direct(self.objective_function, bounds, args=(self.fixed_params,))

        # Get the optimal input values
        optimal_inputs = result.x
        optimal_co2_emissions = result.fun

        # Map to named dictionary
        optimal_inputs_dict = {}
        value_index = 0
        for param in self.default_bounds:
            if param in self.fixed_params:
                optimal_inputs_dict[param] = self.fixed_params[param]
            else:
                optimal_inputs_dict[param] = optimal_inputs[value_index]
                value_index += 1

        return optimal_inputs_dict, optimal_co2_emissions