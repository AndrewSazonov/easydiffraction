from abc import ABC, abstractmethod


class MinimizerBase(ABC):
    @abstractmethod
    def fit(self, sample_models, experiments, calculator):
        pass

    @abstractmethod
    def results(self):
        pass

    @staticmethod
    @abstractmethod
    def display_results(result):
        """
        Display results of the fitting procedure.
        """
        pass

    @abstractmethod
    def _prepare_parameters(self, parameters):
        """
        Prepare the parameters for the minimizer engine.
        """
        pass

    def _objective_function(self, engine_params, parameters, sample_models, experiments, calculator):
        """
        Objective function to be minimized.
        """
        self._sync_parameters(engine_params, parameters)

        residuals = []

        for expt_id, experiment in experiments._items.items():
            y_calc = calculator.calculate_pattern(sample_models, experiment)
            y_meas = experiment.datastore.pattern.meas
            y_meas_su = experiment.datastore.pattern.meas_su

            diff = (y_meas - y_calc) / y_meas_su
            residuals.extend(diff)

        import numpy as np
        return np.array(residuals)

    @staticmethod
    def _sync_parameters(engine_params, parameters):
        """
        Synchronize engine parameter values back to Parameter instances.
        """
        for param in parameters:
            param_name = param.id
            param_obj = engine_params[param_name]
            param.value = param_obj.value
