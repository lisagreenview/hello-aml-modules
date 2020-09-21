import sys
from pathlib import Path
from tempfile import mkdtemp

from azureml.pipeline.wrapper.dsl.module import ModuleExecutor, InputDirectory, OutputDirectory
from azureml.pipeline.wrapper import Pipeline, Module, dsl
from azureml.core.run import Run

@dsl.module(name='add', description='Add two numbers - an illustrative module', job_type='basic')
def add(left: InputDirectory(), right: InputDirectory(), output: OutputDirectory()):
    l = float((Path(left).resolve() / f'data').read_text().strip())
    r = float((Path(right).resolve() / f'data').read_text().strip())
    print('left = ', l)
    print('right = ', r)

    m = l + r
    run = Run.get_context()
    run.log('result', m)
    run.log('left', l)
    run.log('right', r)
    run.flush()

    Path(output).absolute().mkdir(parents=True, exist_ok=True)
    with open(Path(output).resolve() / f'data', 'w') as fout:
        fout.write(str(m))

if __name__ == "__main__":
    ModuleExecutor(add).execute(sys.argv)