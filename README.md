
# TuneParams

TuneParams is a command-line tool that allows users to modify and execute Python scripts with customizable parameters. 

## Features

- Modify parameters dynamically in your Python scripts.
- Run scripts with parameter values specified in the command line or in a separate file.
- Easy integration with existing Python projects.

## Installation

You can install TuneParams via pip:

```bash
pip install tuneparams
```

## Usage

You can run your ML/Python scripts using 2 methods with `TuneParams`. 

1. **Command Line Parameters**: 
   Specify the parameters you want to change directly in the command prompt. For example, if you want to test 10 different parameter combinations like `random_state=33, min_depth=41`, `n_estimators=11`, and `test_size=0.4`, you can provide them as follows:
   ```bash
   tuneparams <script.py> param1=value1 param2=value2 ...
   ```

2. **Parameter File**: 
   Alternatively, you can create a file containing all possible combinations of parameters and use it to run `TuneParams`. The file should have each parameter set separated by commas, and each combination in a new line. You can run them as follows:
   ```bash
   tuneparams <script.py> --param-file <file.txt>
   ```

   **Note:** In the parameter file, each line should contain parameters in the format `param1=value1, param2=value2, ...`.

## Examples

### Command Line Example
```bash
tuneparams my_script.py learning_rate=0.01 epochs=10
```

### Parameter File Example
Create a file `params.txt` with the following content:
```
learning_rate=0.01, epochs=10
learning_rate=0.1, epochs=5
```
Then run:
```bash
tuneparams my_script.py --param-file params.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
