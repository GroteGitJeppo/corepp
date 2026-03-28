## Installation
Tested on Ubuntu 22.04 with a NVIDIA GeForce RTX 4090 Laptop GPU <br/>
Software: Pytorch 2.1.0, torchvision 0.16.0, Python 3.10, CUDA 12.1 <br/> <br/>

**1) Download and install Anaconda:**
- download anaconda: https://www.anaconda.com/download (python 3.x version)
- install anaconda (using the terminal, cd to the directory where the file has been downloaded): bash Anaconda3-[distribution].sh <br/> <br/>

**2) Make a virtual environment (called corepp) using the terminal:**
- conda create --name corepp python=3.10 pip
- conda activate corepp <br/> <br/>

**Alternative (reproducible, from `environment.yml`):** from the `corepp` repository root, run `conda env create -f environment.yml` (or `conda env update -f environment.yml --prune` to refresh an existing env). This installs **PyTorch**, **torchvision**, **`pytorch-cuda=12.1`**, and **pytorch3d** via **conda** (channels `pytorch`, `nvidia`, `pytorch3d`) so they share the same CUDA 12.1 runtime. Remaining libraries use **pip** pins as listed below. **`setuptools>=69,<81`** is included for PyTorch 2.1 compatibility. PointNet++ is used from **`Pointnet_Pointnet2_pytorch/`**; no `nvcc` or project-local `.cu` build is required. <br/> <br/>

**Official PyTorch conda recipe (reference):** [PyTorch Get Started](https://pytorch.org/get-started/locally/) — choose **Conda**, **Linux**, **Python 3.10**, **CUDA 12.1**; the shown command matches `pytorch` + `torchvision` + `pytorch-cuda=12.1` from `pytorch` and `nvidia` channels. **PyTorch3D** is documented at [facebookresearch/pytorch3d INSTALL.md](https://github.com/facebookresearch/pytorch3d/blob/main/INSTALL.md) (`conda install pytorch3d -c pytorch3d`). <br/> <br/>

**3) Download the code repository:**
- git clone https://github.com/UTokyo-FieldPhenomics-Lab/corepp.git 
- cd corepp <br/> <br/>

**4) Install the required software libraries (only if you did not use `environment.yml`):** in the corepp environment, install **PyTorch + torchvision + CUDA 12.1 + pytorch3d** with conda first, then pip for the rest:

- conda install pytorch==2.1.0 torchvision==0.16.0 pytorch-cuda=12.1 pytorch3d=0.7.7 -c pytorch -c nvidia -c pytorch3d
- pip install open3d==0.17.0
- pip install scikit-image==0.22.0
- pip install plyfile==1.0.2
- pip install Pillow==9.5.0 
- pip install trimesh==4.0.5 
- pip install diskcache==5.6.3
- pip install tensorboard==2.15.1
- pip install numba==0.58.1 
- pip install opencv-python==4.8.1.78
- pip install matplotlib==3.8.2 pandas==2.1.4 scikit-learn==1.3.2 scipy==1.11.4 tqdm==4.66.1
- pip install iopath
- pip install "setuptools>=69,<81" *(recommended for PyTorch 2.1 / `pkg_resources` compatibility)* <br/> <br/>

**5) Check if Pytorch links with CUDA (in the corepp virtual environment, using the terminal):** (same checks after `conda env create -f environment.yml`.)
- python
- import torch
- torch.version.cuda *(should print 12.1)*
- torch.cuda.is_available() *(should True)*
- torch.cuda.get_device_name(0) *(should print the name of the first GPU)*
- import pytorch3d *(should succeed if conda pytorch3d installed)*
- quit() <br/> <br/>

**PointNet++:** use the **`Pointnet_Pointnet2_pytorch/`** tree with this environment. You do **not** need to compile custom `.cu` extensions in the repo. **`pytorch3d`** is installed via **conda** (`pytorch3d` channel) together with **`pytorch-cuda=12.1`**. If `pytorch3d` is missing or fails to import, the code **falls back** to the original pure-PyTorch ops in `pointnet2_utils.py`. <br/> <br/>

**Troubleshooting (conda solver):** mixing `pytorch`, `nvidia`, `pytorch3d`, and `conda-forge` can occasionally make the solver strict. If `conda env create` fails with unsatisfiable dependencies, try `conda config --set channel_priority flexible` once, or use **mamba** (`mamba env create -f environment.yml`). If **`pytorch3d=0.7.7`** has no build for your platform, temporarily drop the version pin on `pytorch3d` in `environment.yml` and let conda resolve a compatible build. <br/> <br/>

**Optional**: alter ~/.bashrc file to prevent libGL error when doing open3d visualization, refer to [link](https://github.com/conda-forge/ctng-compilers-feedstock/issues/95)
- cd ..
- sudo gedit ~/.bashrc
- add this line at the end of the bashrc file: **export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6**
- save and close the bashrc file
- source ~/.bashrc <br/> <br/>
