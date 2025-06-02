import argparse
import json
import os


class Args:
    def __init__(self, description: str):
        self.parser = argparse.ArgumentParser(description)

        self.parser.add_argument(
            "config_file",
            metavar="CONFIG_FILE",
            nargs="?",
            type=str,
            default="default.json",
            help="configuration json file path within config_dir, see config/ for examples, default='default.json'",
        )
        self.parser.add_argument(
            "-c",
            "--config-dir",
            dest="config_dir",
            metavar="CONFIG_DIR",
            type=str,
            default="config",
            help="directory with config file, default='config'",
        )
        self.parser.add_argument(
            "benchmark_file",
            metavar="BENCHMARK_FILE",
            nargs="?",
            type=str,
            help="benchmark json file path within benchmark_dir, see benchmarks/ for examples, defaults to file specified in configuration",
        )
        self.parser.add_argument(
            "-b",
            "--benchmark-dir",
            metavar="BENCHMARK_DIR",
            default="benchmarks",
            type=str,
            help="benchmark directory, default='benchmarks'",
        )
        self.parser.add_argument(
            "--n_angles",
            dest="n_angles",
            metavar="N_ANGLES",
            type=int,
            help="number of angles",
        )
        self.parser.add_argument(
            "--method",
            choices=["DSA", "source-iteration"],
            dest="method",
            metavar="METHOD",
            help="solving method",
        )
        self.parser.add_argument(
            "--max-iter",
            dest="max_iter",
            metavar="MAX_ITER",
            type=int,
            help="max number of iterations in solving method",
        )
        self.parser.add_argument(
            "--tol",
            dest="tol",
            metavar="TOL",
            type=float,
            help="tolerance",
        )

        self.args = self.parser.parse_args()

        if self.args.config_file == None:
            self.parser.print_usage()
            print(f"{self.parser.prog} error: CONFIG_FILE is required")
            exit()

        config_file_path = os.path.join(self.args.config_dir, self.args.config_file)
        if not os.path.exists(config_file_path):
            config_file_path = self.args.config_file

            if not os.path.exists(config_file_path):
                raise Exception(
                    f"{config_file_path} not found in {self.args.config_dir} nor in ."
                )

        with open(config_file_path, "r") as file:
            config_options = json.load(file)

        expected_fields = {
            "n_angles": int,
            "method": str,
            "max_iter": int,
            "tol": float,
            "benchmark": str,
        }

        for field, ty in expected_fields.items():
            if field not in config_options:
                raise Exception(f"Key {field} not found in config file")

            if not isinstance(config_options[field], ty):
                raise Exception(
                    f"Field '{field}' is incorrect type in {config_file_path}, got {type(config_options[field])}, expected {ty}"
                )

        if self.args.benchmark_file is not None:
            benchmark_file_path = os.path.join(
                self.args.benchmark_dir, self.args.benchmark_file
            )
            self.benchmark_file = benchmark_file_path
        else:
            short_file_path = config_options["benchmark"]
            long_file_path = os.path.join(self.args.benchmark_dir, short_file_path)
            if os.path.exists(short_file_path):
                self.benchmark_file = short_file_path
            elif os.path.exists(long_file_path):
                self.benchmark_file = long_file_path
            else:
                raise Exception(
                    f"Benchmark file {short_file_path} does not exist in . or in {self.args.benchmark_dir}"
                )

        if self.args.n_angles is not None:
            self.n_angles = self.args.n_angles
        else:
            self.n_angles = config_options["n_angles"]

        if self.args.method is not None:
            self.method = self.args.method
        else:
            if config_options["method"] not in ["DSA", "source-iteration"]:
                raise Exception(
                    f"Invalid method name from {config_file_path}, got {config_options['method']}, expected 'DSA' or 'source-iteration'"
                )
            self.method = config_options["n_angles"]

        if self.args.max_iter is not None:
            self.max_iter = self.args.max_iter
        else:
            self.max_iter = config_options["max_iter"]

        if self.args.tol is not None:
            self.tol = self.args.tol
        else:
            self.tol = config_options["tol"]
