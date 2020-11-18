import sys
from pathlib import Path
from tempfile import mkdtemp

from azureml.pipeline.wrapper.dsl.module import ModuleExecutor, InputDirectory, OutputDirectory
from azureml.pipeline.wrapper import dsl
from azureml.core.run import Run

@dsl.module(
    name='enter_num_manually', 
    description='Put a number in parameter and this module will convert it to a file', 
    job_type='basic')
def enter_num_manually(output: OutputDirectory(), num='0'):
    Path(output).absolute().mkdir(parents=True, exist_ok=True)
    with open(Path(output).resolve() / f'data', 'w') as fout:
        fout.write(num)

if __name__ == "__main__":
    ModuleExecutor(enter_num_manually).execute(sys.argv)