## Polyrnn model

1) First Download the code.zip file.
2) Create the virtual environment of python 2.7
3) Unzip code.zip file, go inside the directory and install all the required libraries by the following command
```bash
pip install -r requirements.txt
```
4) Download the resnet encoder from following link,
```bash
https://download.pytorch.org/models/resnet50-19c8e357.pth
```
5) Download all the bhoomi images, as well as the csv which contains the corresponding links.
6) Open updatejason.py,change the corresponding paths and run, it will create training data
7) This data should be stored in following directory /data/train/images and /data/train_val/images
8) Move few random image jsons from train to train_val to create a validation dataset
9) Now cd to /Experiments and open mle.json, change paths to your system paths
10) cd to code directory and run program using following command,
```bash
export PYTHONPATH=$PWD
python Scripts/train/train_ce.py --exp Experiments/mle.json
```
