from azureml.core import Workspace

subscription_id = '74eccef0-4b8d-4f83-b5f9-fa100d155b22' 
workspace_name = 'lisal-amlservice'
resource_group = 'lisal-dev'

ws = Workspace.get(name=workspace_name, subscription_id=subscription_id, resource_group=resource_group)

# get dataset
from azureml.core import Dataset

training_data_name = 'aml_component_training_data'
test_data_name = 'aml_component_test_data'

train_data = Dataset.get_by_name(ws, name=training_data_name)
test_data = Dataset.get_by_name(ws, name=test_data_name)

# Consume a pipeline component
from azure.ml.component import Pipeline, Component, dsl, types, target_selector, ParameterGroup
from .subgraph import train_settings

train_score_func = Component.load(name='CoreRelevance.L2.Train-score-eval')
compare_component_func = Component.load(ws, name='microsoft.com.azureml.samples.compare_2_models')

@dsl.pipeline(
    name = 'CoreRelevance.L2.Train-score-compare', 
    display_name = 'compare model performance',
    target = 'cpu_cluster', # target and datastore will be applied to subgraph if they're not set in subgraph
    datastore = 'adls_datastore'
)
def train_best_model_pipeline():
    compare_comp = compare_component_func()

    train_score_comp_1 = train_score_func(
        resources = {'instance_type':'ND40_v2_4GPU_2CPU','instance_count': 4},
        train = train_settings(learning_rate = 0.02, max_epochs = 10),
        input_data = train_data,
        test_dat = test_data
    )

    train_score_comp_1.inputs.input_data.configure(
        mode="mount",
        path_on_compute="/input/train_data/"
    )

    train_score_comp_1.inputs.test_data.configure(
        mode="mount",
        path_on_compute="/input/test_data/"
    )

    train_score_comp_1.outputs.model_output.configure( # override model_output configuration
        datastore='model_datastore',
        output_mode="mount",
        path_on_datastore=f"azureml/model/CR/train_result/lr{}"
    )

    # eval_output will use the default value set in "CoreRelevance.L2.Train-score-eval" subgraph

    train_score_comp_2 = train_score_func(
        resources = {'instance_type':'ND40_v2_4GPU_2CPU','instance_count': 6},
        train = train_settings(learning_rate = 0.01, max_epochs = 16),
        input_data = train_data,
        test_dat = test_data
    )

    train_score_comp_2.inputs.input_data.configure(
        mode="mount",
        path_on_compute="/input/path/on/compute/"
    )

    train_score_comp_2.inputs.test_data.configure(
        mode="mount",
        path_on_compute="/input/test_data/"
    )

    train_score_comp_2.outputs.model_output.configure( # override model_output configuration
        datastore='model_datastore',
        output_mode="mount",
        path_on_datastore="azureml/model/CR/train_result/"
    )

    compare_comp.set_inputs(
        model1=train_score_comp_1.outputs.model_output, 
        eval_result1=train_score_comp_1.outputs.eval_output,
        model2=train_score_comp_2.outputs.model_output,
        eval_result2=train_score_comp_2.outputs.eval_output
    )

    return {**compare_comp.outputs}

pipeline = train_best_model_pipeline()
pipeline.validation()
pipeline.submit()
