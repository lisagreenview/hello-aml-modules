# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import argparse
import shutil


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default='output_dir')
    global args
    args, _ = parser.parse_known_args()
    os.makedirs(args.output_dir, exist_ok=True)


def run(input_files):
    # make inference
    print('Input batch size:', len(input_files))
    result = []
    for input_file in input_files:
        output_file = os.path.join(args.output_dir, os.path.basename(input_file))
        print(f"Copy file from {input_file} to {output_file}")
        shutil.copyfile(input_file, output_file)

        # Append result
        result.append("Success")
    print("Batch done")
    # We should return a list with the same length as input_files.
    return result


if __name__ == '__main__':
    # For local debug
    init()
    input_dir = 'input_dir'
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    result = run(files)
    print(result)
