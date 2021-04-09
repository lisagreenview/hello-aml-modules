from azureml.core import Workspace

subscription_id = '74eccef0-4b8d-4f83-b5f9-fa100d155b22' 
workspace_name = 'lisal-amlservice'
resource_group = 'lisal-dev'

ws = Workspace.get(name=workspace_name, subscription_id=subscription_id, resource_group=resource_group)

# get dataset
from azureml.core import Dataset

training_data_name = 'aml_component_training_data'
test_data_name = 'aml_component_test_data'

if training_data_name not in ws.datasets:
    print('Registering a training dataset for sample pipeline ...')
    train_data = Dataset.File.from_files(path=['https://dprepdata.blob.core.windows.net/demo/Titanic.csv'])
    train_data.register(workspace = ws, 
                        name = training_data_name, 
                        description = 'Training data (just for illustrative purpose)')
    print('Registered')

if test_data_name not in ws.datasets:
    print('Registering a test dataset for sample pipeline ...')
    test_data = Dataset.File.from_files(path=['https://dprepdata.blob.core.windows.net/demo/Titanic.csv'])
    test_data.register(workspace = ws, 
                       name = test_data_name, 
                       description = 'Test data (just for illustrative purpose)')
    print('Registered')

train_data = Dataset.get_by_name(ws, name=training_data_name)
test_data = Dataset.get_by_name(ws, name=test_data_name)

# get components
from azure.ml.component import Component

train_component_func = Component.load(ws, name='samples.mpi_train')
score_component_func = Component.load(ws, name='microsoft.com.azureml.samples.score')
eval_component_func = Component.load(ws, name='microsoft.com.azureml.samples.score')
compare_component_func = Component.load(ws, name='microsoft.com.azureml.samples.compare_2_models')

# define a sub pipeline
from azure.ml.component import Pipeline, Component, dsl, types, target_selector, ParameterGroup

class train_settings(ParameterGroup):
    learning_rate: types.Float(optional=False, default=0.01, description='learning rate')
    max_epochs: types.Integer(optional=False, default=5)

@dsl.pipeline(
    name = 'CoreRelevance.L2.Train-score-eval', 
    version = '0.0.1',
    display_name = 'train model and evaluate model perf',
    target = 'cpu_cluster',
    target_selector = my_target,
    datastore = 'wsblob'
)
def training_pipeline(
    input_data: types.Path(optional=False, description='training data'), # input data as pipeline parameter
    test_data: types.Path(optional=False, description='test data'),
    resources: types.Group( # define the Parameter Group inline
        description = "resource definition",
        value = [
            types.Integer(name = 'instance_count', optional = False, min = 1, max = 128, default = 1),
            types.String(name = 'instance_type', optional = False, default = 'ND40_v2_4GPU_2CPU')
        ]
    ),
    train: types.Group(desctiption = "training parameters") = train_settings() # use a defined ParameterGroup class
):
    train = train_component_func(
        training_data=input_data, 
        max_epochs = train.max_epochs, 
        learning_rate = train.learning_rate)

    train.runsettings.resource_layout.configure(
        instance_type = resources.instance_type,
        instance_count = resources.instance_count,
        )

    train.outputs.model_output.configure(
        datastore='my_datastore',
        output_mode="mount",
        path_on_datastore="azureml/model/CR/train_result",
    )
    # register the output dataset
    train.outputs.model_output.register_as(
        name="Bing.CR.L2_model", create_new_version=True)
                                           
    score = score_component_func(
        model_input=train.outputs.model_output, 
        test_data=test_data)

    eval = eval_component_func(scoring_result=score.outputs.score_output)

    eval.outputs.eval_output.configure(
        datastore = 'pipeline_datastore',
        output_mode = "mount",
        path_on_datastore = "azureml/pipeline/eval/eval_result"
    )
    
    return [
        types.Output(name = 'eval_output', value = eval.outputs.eval_output, description = 'metrics output'),
        types.Output(name = 'model_output', value = train.outputs.model_output, description = 'model')
    ]

pipeline_comp = training_pipeline()
pipeline_comp.validation()
pipeline_comp.create()

# Consume a pipeline component
from azure.ml.component._version import VERSION

train_score_func = Component.load(name='CoreRelevance.L2.Train-score-eval')

@dsl.pipeline(
    name = 'CoreRelevance.L2.Train-score-compare', 
    display_name = 'compare model performance',
    target = 'cpu_cluster',
    datastore = 'my_adls'
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