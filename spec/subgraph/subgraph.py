#dummy change to fork.. 
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

# get components
from azure.ml.component import Component

train_component_func = Component.load(ws, name='samples.mpi_train')
score_component_func = Component.load(ws, name='microsoft.com.azureml.samples.score')
eval_component_func = Component.load(ws, name='microsoft.com.azureml.samples.score')

# define a sub pipeline
from azure.ml.component import Pipeline, Component, dsl, types, target_selector, ParameterGroup

class train_settings(ParameterGroup):
    learning_rate: types.Float(optional=False, default=0.01, description='learning rate')
    max_epochs: types.Integer(optional=False, default=5)

@dsl.pipeline(
    name = 'CoreRelevance.L2.Train-score-eval', 
    version = '0.0.1',
    display_name = 'train model and evaluate model perf',
    datastore = 'workspaceblob'
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

    # the outputs of score module won't be seen outside the subgraph, as it's not been promoted as pipeline level outputs
    return [
        types.Output(name = 'eval_output', value = eval.outputs.eval_output, description = 'metrics output'),
        types.Output(name = 'model_output', value = train.outputs.model_output, description = 'model')
    ]

pipeline_comp = training_pipeline()
pipeline_comp.validation()
pipeline_comp.create()

