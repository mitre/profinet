# Profinet Plugin Code

Where possible, the Caldera for OT plugins leverage open-source libraries and payloads, unifying their exposure through the Caldera Adversary Emulation framework.

* The Profinet plugin leverages the open-source library [pnio-dcp](https://gitlab.com/pyshacks/pnio_dcp/-/tree/v1.1.6?ref_type=tags) - version 1.1.6.

* The pnio-dcp library is licensed with the [MIT License](https://gitlab.com/pyshacks/pnio_dcp/-/blob/v1.1.6/LICENSE.md?ref_type=tags)

* A custom command-line interface was created by our team for the pnio-dcp library to allow for Caldera agent interoperability. The CLI payload comes precompiled with the plugin, but can be recompiled following the instructions below.


## Specific Code Modifications
* __Change 1__: Expose timeout as a variable instead of constant.<br>
The file 'pnio_dcp.py' is modified to add another parameter to the DCP object constructor for timeout. See lines 47, 55-57 for changes.


## Reproducing Builds
### Build System Configuration
| Item            | Windows binary   | Linux binary       |
|---------        |--------------    |-------             |
| OS ver.         | Windows 10 v21H2 | Ubuntu 22.04.2 LTS |
| Python ver.     | 3.8.10           | 3.8-dev            |
| Pyinstaller ver.| 6.10.2           | 6.10.2             |
| pnio_dcp ver.   | 1.1.6            | 1.1.6              |
| binary name     | dcp_utility.exe  | dcp_utility        |


### Step-by-Step Instructions
1. Download source
```sh
git clone --depth 1 --branch v1.1.6 https://gitlab.com/pyshacks/pnio_dcp.git
```
2. Replace pnio_dcp.py in downloaded source with provided modified version.

3. Validate you have the proper version of python installed. Optionally, create and enter a virtual environment with the required python version using packages like pyenv, venv, pipenv, or poetry.

```sh
python --version
```

4. Install pnio_dcp library <br>
```sh
pip install /src/pnio_dcp
```

5. Silence setuptools_scm warning <br>
modify _warn_on_old_setuptools function in the setuptools_scm package to silence false-positive warning. See line 28, setuptools_scm/_integration/setuptools.py <br>

```py
def _warn_on_old_setuptools(_version: str = setuptools.__version__) -> None:
    return
    ...
```

6. Test functionality of python cli prior to build
```sh
python /src/dcp_utility.py --help
```

7. Build the binary with a static builder<br>
```sh
pip install pyinstaller

sudo env "PATH=$PATH" pyinstaller /src/dcp_utility.py --onefile
```