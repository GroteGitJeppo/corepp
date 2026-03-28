## Installation
Tested on Ubuntu 22.04 with a NVIDIA GeForce RTX 4090 Laptop GPU <br/>
Software: Pytorch 2.1.0, torchvision 0.16.0, Python 3.10, CUDA 12.1 <br/> <br/>

**1) Download and install Anaconda:**
- download anaconda: https://www.anaconda.com/download (python 3.x version)
- install anaconda (using the terminal, cd to the directory where the file has been downloaded): bash Anaconda3-[distribution].sh <br/> <br/>

**2) Make a virtual environment (called corepp) using the terminal:**
- conda create --name corepp python=3.10 pip
- conda activate corepp <br/> <br/>

**Alternative (reproducible, from `environment.yml`):** from the `corepp` repository root, run `conda env create -f environment.yml` (or `conda env update -f environment.yml --prune` to refresh an existing env). This pins the same package versions as step 4 below, including pip **torch/torchvision (cu121)** and **`setuptools>=69,<81`** for PyTorch 2.1 compatibility. PointNet++ is used from a **pure PyTorch** tree (`Pointnet_Pointnet2_pytorch/`); no conda CUDA toolkit or `nvcc` is required. <br/> <br/>

**3) Download the code repository:**
- git clone https://github.com/UTokyo-FieldPhenomics-Lab/corepp.git 
- cd corepp <br/> <br/>

**4) Install the required software libraries (in the corepp virtual environment, using the terminal):**
- pip install -U torch==2.1.0 torchvision==0.16.0 -f https://download.pytorch.org/whl/cu121/torch_stable.html
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
- pip install "setuptools>=69,<81" *(recommended for PyTorch 2.1 / `pkg_resources` compatibility)* <br/> <br/>

**5) Check if Pytorch links with CUDA (in the corepp virtual environment, using the terminal):** (same checks after `conda env create -f environment.yml`.)
- python
- import torch
- torch.version.cuda *(should print 12.1)*
- torch.cuda.is_available() *(should True)*
- torch.cuda.get_device_name(0) *(should print the name of the first GPU)*
- quit() <br/> <br/>

**PointNet++:** use the **`Pointnet_Pointnet2_pytorch/`** tree with this environment. You do **not** need to compile custom `.cu` extensions in the repo. GPU acceleration comes from the **PyTorch cu121** wheels above. **`pytorch3d`** is included in `environment.yml` as an **optional** dependency (prebuilt wheel + `iopath`): it speeds up farthest-point sampling, ball query, and feature-propagation kNN. If `pytorch3d` fails to install for your platform, remove those pip lines and the code **falls back** to the original pure-PyTorch ops. <br/> <br/>

**Optional**: alter ~/.bashrc file to prevent libGL error when doing open3d visualization, refer to [link](https://github.com/conda-forge/ctng-compilers-feedstock/issues/95)
- cd ..
- sudo gedit ~/.bashrc
- add this line at the end of the bashrc file: **export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6**
- save and close the bashrc file
- source ~/.bashrc <br/> <br/>
