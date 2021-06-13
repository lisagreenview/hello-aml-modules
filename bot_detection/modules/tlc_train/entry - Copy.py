"""This is an auto generated module entry file of Aether Module a2c82ca1-e437-4523-b05f-4a550cab43d0"""
import sys
import subprocess
import re
import shlex
from pathlib import Path
from enum import Enum
from azureml.pipeline.wrapper import dsl
from azureml.pipeline.wrapper.dsl.module import ModuleExecutor, InputDirectory, OutputDirectory, InputFile, OutputFile


optional_pattern = re.compile(r'(\[[\s\S]*?\])')
variable_pattern = re.compile(r'(\{[\s\S]*?\})')


def get_optional_mapping(interface):
    """Get the mapping from an optional variable to the corresponding command line in []."""
    return {variable_pattern.search(item).group(0): item[1:-1] for item in re.findall(optional_pattern, interface)}


def get_input_file(path: str):
    """Get the file of the input to workaround that windows compute will output a file as a directory."""
    path = Path(path)
    if path.is_dir():
        files = list(path.iterdir())
        return str(files[0])
    elif path.is_file():
        return path
    else:
        raise FileNotFoundError("Input file cannot be found: %s" % path)


def get_output_file(path: str, key: str):
    """Pad file path if output path is directory to workaround that windows compute will output a file as a directory."""
    if Path(path).is_dir():
        return Path(path) / key
    return path


class Enum_cache_instances_in_memory(Enum):
    Enum_0 = '-'
    Enum_1 = '+'

class Enum_use_threads(Enum):
    Enum_0 = '-'
    Enum_1 = '+'

class Enum_print_model_summary(Enum):
    Enum_0 = '-'
    Enum_1 = '+'


# One space at the end so the last char of the interface could be "
interface = r"""TL.exe /c Train {training_data}  /m {trained_model} /mt {trained_model_text} /ms {trained_model_summary} /mi {trained_model_ini_file}  /cl {predictor} [/cls {predictor_settings}] /inst {instances_reader} [/instset {instances_settings}] [/cacheInst{cache_instances_in_memory}] /rs {random_seed}  [/threads{use_threads}] [/tp {proportion_of_train_data_to_use}] [/sctrain {skipchartrain}] [/sctest {skipchartest}] [/ev {evaluator}] [/evs {evaluator_settings}] [/debug {debug_level}] [/summary{print_model_summary}] """


@dsl.module(
    name="""TLC: Train""",
    os='Windows',
)
def tlc_train(
    training_data: InputFile(type=(['AnyDirectory', 'AnyFile'])),
    trained_model: OutputFile(),
    trained_model_text: OutputFile(),
    trained_model_summary: OutputFile(),
    trained_model_ini_file: OutputFile(),
    predictor: str = "FastRankClassification",
    predictor_settings: str = None,
    instances_reader: str = "StreamingInstances",
    instances_settings: str = None,
    cache_instances_in_memory: Enum_cache_instances_in_memory = None,
    random_seed: int = 123,
    use_threads: Enum_use_threads = None,
    proportion_of_train_data_to_use: float = None,
    skipchartrain: str = None,
    skipchartest: str = None,
    evaluator: str = None,
    evaluator_settings: str = None,
    debug_level: int = None,
    print_model_summary: Enum_print_model_summary = None,
):
    input_file_keys = ["training_data"]
    output_file_keys = ["trained_model","trained_model_text","trained_model_summary","trained_model_ini_file"]
    port_keys = ["training_data","trained_model","trained_model_text","trained_model_summary","trained_model_ini_file"]

    func_args = {k: v for k, v in locals().items()}
    for k in port_keys:
        if func_args[k]:
            func_args[k] = str(Path(func_args[k]).absolute().resolve())  # Convert path format to align the OS.
    
    for k in input_file_keys:
        if func_args[k]:
            func_args[k] = get_input_file(func_args[k])  # Convert input directory to an input file to workaround.

    for k in output_file_keys:
        if func_args[k]:
            func_args[k] = get_output_file(func_args[k], k)  # Convert output directory to an output file to workaround.

    args = interface.strip()
    mapping = get_optional_mapping(args)

    for optional in mapping.values():
        args = args.replace('[%s]' % optional, optional)  # Remove optional tag "[]" in the interface.

    for k, v in func_args.items():
        goal = '{%s}' % k
        if v is None:
            args = args.replace(mapping.get(goal, goal), '')  # Remove all optional values which is None.

    # Replace every argument with the real variable value, note that for enum values, we need to use v.value to get proper str value.
    func_args = {k: v.value if isinstance(v, Enum) else str(v) for k, v in func_args.items()}
    # TODO: support special parameter format FastRankClassification{nl=60 mil=100 iter=100 lr=0.1}
    # args = [arg.format(**func_args) for arg in shlex.split(args)]
    args = args.format(**func_args)
    print(args)
    subprocess.run(args, check=True)
  

if __name__ == '__main__':
    ModuleExecutor(tlc_train).execute(sys.argv)
