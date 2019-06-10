import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ema_workbench import (Model, CategoricalParameter,
                           ScalarOutcome, TimeSeriesOutcome, IntegerParameter, RealParameter)

from ema_workbench import (MultiprocessingEvaluator, ema_logging,
                           perform_experiments, SequentialEvaluator)

from dike_model_function_V2_0 import (DikeNetwork,DikeNetworkTS)  # @UnresolvedImport
from problem_formulation_V2_2 import get_model_for_actor_problem_formulation

from ema_workbench.util.utilities import save_results

import sys

def make_models(dike_nums):
	models = {}
	for num in dike_nums:
		models['A.{}'.format(num)] = get_model_for_actor_problem_formulation(
			num+7, outcome_type='scalar')
	return models

def run_models(model_dict, num_scenarios=1, num_policies=1):
	ema_logging.log_to_stderr(ema_logging.INFO)

	for key in model_dict.keys():
		with MultiprocessingEvaluator(model_dict[key][0],n_processes = 10) as evaluator:
			results = evaluator.perform_experiments(
	        	scenarios=num_scenarios, policies=num_policies, reporting_frequency=50)
			save_results(results, '{}_results.tar.gz'.format(key))
	return

if __name__ == '__main__':
	dike_nums = [1,2,3,4,5]
	n_scenarios = 150
	n_policies = 150
	models = make_models(dike_nums)
	run_models(models, num_scenarios=n_scenarios, num_policies=n_policies)
