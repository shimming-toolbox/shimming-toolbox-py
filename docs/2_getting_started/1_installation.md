# Installation

We recommend that shimming-toolbox-py be used with [Miniconda](https://conda.io/docs/glossary.html#miniconda-glossary), a lightweight version of the [Anaconda distribution](https://www.anaconda.com/distribution/). Miniconda is typically used to create virtual Python environments, which provides a separation of installation dependencies between different Python projects. Although it is possible to install shimming-toolbox-py without Miniconda or virtual environments, we only provide instructions for this recommended installation setup.

First, verify that you have a compatible version of Miniconda or Anaconda properly installed and in your system path.

In a new terminal window (macOS or Linux) or Anaconda Prompt (Windows – if it is installed), run the following command:

```
conda search python
```

If a list of available Python versions are displayed and versions >=3.6.0 are available, you may skip to the next section (Git).

## Linux
To install Miniconda, run the following commands in your terminal:

```bash
cd
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
echo ". ~/miniconda/etc/profile.d/conda.sh" >> ~/.bashrc
source ~/.bashrc
```

## macOS

The Miniconda installation instructions depend on whether your system default shell is Bash or Zsh. You can determine this from the output of running the following in your terminal:

```bash
echo $SHELL
```

### Bash

```bash
cd
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
echo ". ~/miniconda/etc/profile.d/conda.sh" >> ~/.bash_profile
source ~/.bash_profile
```

### Zsh
```zsh
cd
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
source $HOME/miniconda/bin/activate
conda init zsh
```

## Windows
NOTE: The shimming-toolbox-py installation instruction using the Miniconda have only been tested for Windows 10. Older versions of Windows may not be compatible with the tools required to run shimming-toolbox-py.

To install Miniconda, go to the [Miniconda installation website](https://conda.io/miniconda.html) and click on the Python 3.x version installer compatible with your Windows system (64-bit recommended). After the download is complete, execute the downloaded file, and follow the instructions. If you are unsure about any of the installation options, we recommend you use the default settings.

## Git (optional)
Git is a software version control system. Because shimming-toolbox-py is hosted on GitHub, a service that hosts Git repositories, having Git installed on your  system allows you to download the most up-to-date development version of shimming-toolbox-py from a terminal, and also allows you to contribute to the project if you wish to do so.

Although an optional step (shimming-toolbox-py can also be downloaded other ways, see below), if you want to install Git, please follow instructions for your operating system on the [Git website](https://git-scm.com/downloads).

## Virtual Environment
Virtual environments are a tool to separate the Python environment and packages used between Python projects. They allow for different versions of Python packages to be installed and managed for the specific needs of your projects. There are several virtual environment managers available, but the one we recommend and will use in our installation guide is [conda](https://conda.io/docs/), which is installed by default with Miniconda. We strongly recommend you create a virtual environment before you continue with your installation.

To create a Python 3.6 virtual environment named “shim_venv”, in a terminal window (macOS or Linux) or Anaconda Prompt (Windows) run the following command and answer “y” to the installation instructions:

```bash
conda create -n shim_venv python=3.6
```

Then, activate your virtual environment:
```bash
conda activate shim_venv
```

To switch back to your default environment, run:
```bash
conda deactivate
```

## shimming-toolbox-py

### Development version
To install the development version of shimming-toolbox-py, clone shimming-toolbox-py's repository (you will need to have Git installed on your system):

```bash
git clone https://github.com/shimming-toolbox/shimming-toolbox.git
```

If you don't have Git installed, download and extract shimming-toolbox-py from this [link](https://github.com/shimming-toolbox/shimming-toolbox/archive/master.zip).

Then, in your Terminal, go to the shimming-toolbox-py folder and install the shimming-toolbox-py package. The following `cd` command assumes that you followed the `git clone` instruction above:

```bash
cd shimming-toolbox-py
pip install -e ".[testing]"
```

NOTE: If you downloaded shimming-toolbox-py using the link above instead of `git clone`, you may need to cd to a different folder (e.g. `Downloads` folder located within your home folder `~`), and the shimming-toolbox-py folder may have a different name (e.g. `shimming-toolbox-py-master`).

#### Updating
To update an already cloned shimming-toolbox-py package, pull the latest version of the project from GitHub and reinstall the application:
```bash
cd shimming-toolbox-py
git pull
pip install -e ".[testing]"
```

## Testing the installation
### Comprehensive test
To run the entire testing suite, run `pytest` from the shimming-toolbox-py directory:
```bash
cd shimming-toolbox-py
pytest
```
See https://docs.pytest.org/ for more options.

If all tests pass, shimming-toolbox-py was installed successfully.