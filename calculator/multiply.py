import sys
from pathlib import Path

from azureml.pipeline.wrapper.dsl.module import ModuleExecutor, InputDirectory, OutputDirectory
from azureml.pipeline.wrapper import dsl
from azureml.core.run import Run

@dsl.module(
    name="multiply"
)
def multiply(
    left: InputDirectory(),
    right: InputDirectory(),
    result: OutputDirectory()
):

    l = float((Path(left).resolve() / f'data').read_text().strip())
    r = float((Path(right).resolve() / f'data').read_text().strip())
    print('left = ', l)
    print('right = ', r)

    m = l * r
    run = Run.get_context()
    run.log('result', m)
    run.log('left', l)
    run.log('right', r)
    run.flush()

    Path(result).absolute().mkdir(parents=True, exist_ok=True)
    with open(Path(result).resolve() / f'data', 'w') as fout:
        fout.write(str(m))

if __name__ == "__main__":
    ModuleExecutor(multiply).execute(sys.argv)