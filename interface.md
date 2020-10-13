
### Component

```python
# load component
component.load(
    workspace:azureml.core.workspace.Workspace,
    name:str=None,
    version:str=None,
)

component.batch_load(
    workspace:azureml.core.workspace.Workspace,
    identifiers:List[str],
)

component.from_yaml(
    workspace:azureml.core.workspace.Workspace,
    yaml_file:str=None,
)

component.from_func(
    workspace:azureml.core.workspace.Workspace,
    func:types.FunctionType,
    force_reload=True
)

component.run(
    use_docker=True,
    track_run_history=True,
)

component.set_input()

component.set_parameters()

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

run.visualize()

run.profile()
```