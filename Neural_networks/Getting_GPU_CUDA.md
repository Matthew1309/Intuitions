# Getting GPU support for tensorflow to work 7/12/2023
First I followed this link https://www.tensorflow.org/install/pip#windows-wsl2 to see how to install tensorflow, then from there I went to
this link https://docs.nvidia.com/cuda/wsl-user-guide/index.html to see how to get cuda working.

In between I ran `apt-get update`, then `apt install nvidia-cuda-toolkit`, then checked the CUDA version I have with `nvidia-smi`. Turns out I have version 11.6, with driver version 511.79. I think the drivers are okay, but the documentation wants me to have CUDA version 11.8!

Well I'm following the instructions https://docs.nvidia.com/cuda/wsl-user-guide/index.html for option 1 
> **Option 1: Installation of Linux x86 CUDA Toolkit using WSL-Ubuntu Package - Recommended**<br>
The CUDA WSL-Ubuntu local installer does not contain the NVIDIA Linux GPU driver, so by following the steps on the CUDA [download page for WSL-Ubuntu](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local), you will be able to get just the CUDA toolkit installed on WSL.

and this is what it says in the installer of the CUDA toolkit `%ProgramFiles%\NVIDIA GPU Computing Toolkit\CUDA\v#.#`

I restarted my computer, now when I run `nvidia-smi` I see<br>
```
NVIDIA-SMI 535.54.04              Driver Version: 536.25       CUDA Version: 12.2
```
<br>
However, I am still not detecting a GPU.

## My steps
Most of this was following this link https://www.tensorflow.org/install/pip#hardware_requirements
1. install CUDA toolkit as above
1. run this for some reason `sudo apt-key del 7fa2af80`
1. `conda create --name tensorflow python=3.9`
1. `conda activate tensorflow`
1. `conda install -c conda-forge cudatoolkit=11.8.0
pip install nvidia-cudnn-cu11==8.6.0.163`
1. `mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/:$CUDNN_PATH/lib' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh`
1. `pip install tensorflow==2.12.*`
1. `python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"`
1. `python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"`
1. Then for this to work in the jupyter lab, run jupyterlab on the commandline with the tensorflow env active, then and only then will GPUs pop up!


