# nis2pyr development

## Setting up a nis2pyr development environment

Create a Conda virtual environment.

```text
conda create -n nis2pyr python=3.9
conda activate nis2pyr
```

Get the nis2pyr source code.

```text
git clone https://github.com/vibbits/nis2pyr.git
```

Now `cd` into the repo you just cloned (this is the folder which contains `setup.cfg`) and install the nis2pyr package in developer mode:

```text
pip install -e .[dev]
```

This will also install the developer tools `pytest`, `flake8` and `pyinstaller`.

## Packaging nis2pyr

### Packaging into a stand-alone directory

The `nis2pyr.py` program requires a Python environment to execute. This complicates deploying it on non-development machines where Python is not installed. It is however possible to bundle nis2pyr with all its dependencies and a Python interpreter into a stand-alone directory which contains a `nis2pyr.exe` executable that runs the program. This can be accomplished with [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/index.html) as follows.

In the development environment set up as explained above, `cd` into the directory which contains the `nis2pyr.py` file and run pyinstaller:

```text
pyinstaller --collect-all nd2 --collect-all ome_types --collect-all xmlschema nis2pyr.py
```

The `--collect-all` options are needed to give `pyinstaller` a hand finding modules needed by nis2pyr.

The dist\nis2pyr directory is now self-contained and holds a `nis2pyr.exe` which can be executed on the command line outside a Python development environment.

### Packaging into a stand-alone executable

Instead of bundling nis2pyr in a directory containing the executable as well as all its dependencies, it is also possible to bundle everything in a single executable which is basically a self-extracting archive holding the same files. This is done by passing the `--onefile` option to `pyinstaller`:

```text
pyinstaller --onefile --collect-all nd2 --collect-all ome_types --collect-all xmlschema nis2pyr.py
```

The resulting single file `nis2pyr.exe` is now even easier to deploy. However, starting it will be a bit slower because behind the scenes its contents are first unpacked into a temporary folder every time nis2pyr is run.
