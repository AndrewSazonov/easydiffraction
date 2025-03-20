import numpy as np
from scipy.interpolate import interp1d

from .calculators.factory import CalculatorFactory
from easydiffraction.utils.chart_plotter import ChartPlotter


class Analysis:
    _calculator = CalculatorFactory.create_calculator('cryspy')

    def __init__(self, project):
        self.project = project
        self.calculator = Analysis._calculator  # Default calculator shared by project
        self._refinement_strategy = 'single'

    def show_refinable_params(self):
        print("\nSample Models Parameters:")
        self.project.sample_models.show_all_parameters_table()

        print("\nExperiment Parameters:")
        self.project.experiments.show_all_parameters_table()

    def show_free_params(self):
        free_params = self.project.sample_models.get_free_params() + \
                      self.project.experiments.get_free_params()

        print("\nFree Parameters:")

        if not free_params:
            print("No free parameters found.")
            return

        import pandas as pd
        df = pd.DataFrame(free_params)

        if df.empty:
            print("No free parameters found.")
            return

        df.rename(columns={
            "item_id": "block",
            "cif_full_name": "cif_name",
            "uncertainty": "error",
            "free": "free"
        }, inplace=True)

        df = df[["block", "cif_name", "value", "error", "free"]]

        try:
            from tabulate import tabulate
            print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
        except ImportError:
            print(df.to_string(index=False))

        return free_params

    def show_available_calculators(self):
        CalculatorFactory.show_available_calculators()

    def set_calculator_by_name(self, calculator_name):
        if calculator_name not in CalculatorFactory.available_calculators():
            raise ValueError(
                f"Unknown calculator '{calculator_name}'. Available calculators: {CalculatorFactory.available_calculators()}"
            )

        self.calculator = CalculatorFactory.create_calculator(calculator_name)
        print(f"Calculator switched to: {calculator_name}")

    def calculate_pattern(self, expt_id):
        experiment = self.project.experiments[expt_id]
        sample_models = self.project.sample_models

        x_points = experiment.datastore.pattern.x

        if experiment.background.points:
            background_points = np.array(experiment.background.points)
            bg_x, bg_y = background_points[:, 0], background_points[:, 1]

            interp_func = interp1d(
                bg_x, bg_y,
                kind='linear',
                bounds_error=False,
                fill_value=(bg_y[0], bg_y[-1])
            )
            interpolated_bkg = interp_func(x_points)
            experiment.datastore.pattern.bkg = interpolated_bkg
        else:
            interpolated_bkg = np.zeros_like(x_points)
            experiment.datastore.pattern.bkg = interpolated_bkg

        calculated_pattern = self.calculator.calculate_pattern(sample_models, experiment)
        calculated_pattern_with_bkg = calculated_pattern + interpolated_bkg

        experiment.datastore.pattern.calc = calculated_pattern_with_bkg

        return calculated_pattern_with_bkg

    def show_calc_chart(self, expt_id, x_min=None, x_max=None):
        experiment = self.project.experiments[expt_id]

        if experiment.datastore.pattern.calc is None:
            print(f"No calculated pattern found for {expt_id}. Running calculation...")
            self.calculate_pattern(expt_id)

        pattern = experiment.datastore.pattern

        plotter = ChartPlotter()
        plotter.plot(
            y_values_list=[pattern.calc],
            x_values=pattern.x,
            x_min=x_min,
            x_max=x_max,
            title=f"Calculated diffraction pattern for {expt_id}",
            labels=['calc']
        )

    def show_meas_vs_calc_chart(self, expt_id, x_min=None, x_max=None, show_residual=False):
        experiment = self.project.experiments[expt_id]

        self.calculate_pattern(expt_id)

        pattern = experiment.datastore.pattern

        if pattern.meas is None or pattern.calc is None or pattern.x is None:
            print(f"No data available for {expt_id}. Cannot display chart.")
            return

        series = [pattern.meas, pattern.calc]
        labels = ['meas', 'calc']

        if show_residual:
            residual = pattern.meas - pattern.calc
            series.append(residual)
            labels.append('residual')

        plotter = ChartPlotter()
        plotter.plot(
            y_values_list=series,
            x_values=pattern.x,
            x_min=x_min,
            x_max=x_max,
            title=f"Measured vs Calculated diffraction pattern for {expt_id}",
            labels=labels
        )

    def fit(self):
        print("Starting the fitting process...")

        sample_models = self.project.sample_models
        experiments = self.project.experiments

        if not sample_models or not experiments:
            print("No sample models or experiments found in the project. Fit aborted.")
            return

        if not self.calculator:
            raise ValueError("No calculator is set. Cannot run fit.")

        # Create an instance of DiffractionMinimizer if not already there
        if not hasattr(self, 'fitter') or self.fitter is None:
            from .minimization import DiffractionMinimizer
            self.fitter = DiffractionMinimizer(engine='lmfit')  # Or configurable!

        # Run the fitting process
        self.fitter.fit(sample_models, experiments, self.calculator)

        # After fitting, get the results
        self.fit_results = self.fitter.results

        print("Fit completed.")

    def show_fit_results(self):
        if not hasattr(self, 'fit_results') or not self.fit_results:
            print("No fit results found. Run fit() first.")
            return

        print("\nFitting Results:")
        print(f"Reduced Chi-square: {self.fit_results.redchi:.2f}")
        if hasattr(self.fit_results, "params"):
            for param_name, param_obj in self.fit_results.params.items():
                print(f"  {param_name}: {param_obj.value} (init = {param_obj.init_value})")
        else:
            print("No refined parameters found in fit results.")