
### Component

```python
# load published component
component.load(
    workspace:azureml.core.workspace.Workspace,
    name:str=None, # name:version, name@label
    version:str=None,
    label:str=None, # check the backend capability
)

# load multiple published components
component.batch_load(
    workspace:azureml.core.workspace.Workspace,
    identifiers:List[str], # name:version, name@label
)

# load unpublished component from yaml (local or public github)
component.from_yaml(
    workspace:azureml.core.workspace.Workspace,
    yaml_file:str=None,
)

# load component from a local function (must be dsl.component)
# see example:https://github.com/lisagreenview/hello-aml-modules/blob/master/calculator/calculator.ipynb
component.from_func(
    workspace:azureml.core.workspace.Workspace,
    func:types.FunctionType,
    force_reload=True
)

# local run
component.run(
    use_docker=True,
    track_run_history=True,
)

# specify input port and parameter
component.set_inputs()

# configure run settings
component.runsettings.configure()
```

### Pipeline

```python
@dsl.pipeline()

# validate pipeline and visualize the graph
pipeline.validate()

# save as pipeline draft
pipeline.save(
    experiment_name=None,
    id=None,
    default_compute_target=None,
    pipeline_parameters=None,
    tags=None,
    properties=None,
)

# submit pipeline
pipeline.submit(
    experiment_name=None,
    default_compute_target=None,
    description=None,
    pipeline_parameters=None,
    tags=None,
    continue_on_step_failure=None,
    regenerate_outputs=None,
    skip_validation=False,
)

# pipeline local run
pipeline.run(
    experiment_name = None,
    show_output = True,
    show_graph = True,
)

```
### Run

```python
run.wait_for_completion()

# see example: https://github.com/Azure/DesignerPrivatePreviewFeatures/blob/sdkpreview/azureml-modules/samples/pipeline_run_visualize_profile.ipynb
run.visualize()

run.profile()
```