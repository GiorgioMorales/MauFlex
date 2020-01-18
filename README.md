# MauFlex
**Mauritia Flexuosa segmentation software**

# Abstract

One of the most important ecosystems in the Amazon rainforest is the *Mauritia Flexuosa*
swamp or “aguajal”. However, deforestation of its dominant species, the *Mauritia Flexuosa* palm, 
also known as “aguaje”, is a common issue, and conservation is poorly monitored because of the difficult access to these swamps. 
The contribution of this work is the proposal of a segmentation and measurement method for areas covered in *Mauritia Flexuosa* 
palms using high-resolution aerial images acquired by UAVs. 
The method performs a semantic segmentation of *Mauritia Flexuosa* using an end-to-end trainable Convolutional Neural Network (CNN) 
based on the Deeplab v3+ architecture. Images were acquired under different environment and light conditions using three different 
RGB cameras. The MauFlex dataset was created from these images and it consists of 25,248 image patches of 512 X 512 pixels and 
their respective ground truth masks. The results over the test set achieved an accuracy of 98.143%, specificity of 96.599%, and sensitivity
of 95.556%. It is shown that our method is able not only to detect full-grown isolated *Mauritia* Flexuosa palms, but also young palms or 
palms partially covered by other types of vegetation.

# Implementation

This implementation of MauFlex on Python 3, Keras and Tensorflow. The model generates segmentation masks for each selected image of the selected folder. 

![GUI](https://github.com/GiorgioMorales/MauFlex/blob/master/assets/GUI.png)

**User interface**

![result](https://github.com/GiorgioMorales/MauFlex/blob/master/assets/result.png)

**Segmentatin result**

![mosaic](https://github.com/GiorgioMorales/MauFlex/blob/master/assets/bigmosaic2.jpg)

**Aerial image mosaics acquired near Lake Quistococha. (a) Mosaics of RGB images. (b) Mosaics of *Mauritia Flexuosa* masks.**

# Dataset

We acquired aerial images of Mauritia Flexuosa swamps (“aguajales”) south of the city of iquitos since 2015 to 2018. 
We selected the most 96 representative ones to create the dataset: 47 were acquired with a TurboAce UAV (Sony Nex-7 camera); 
28, with a Mavic Pro UAV; and 21, with a SkyRanger UAV. Each image has a correspondent binary hand-drawn Mauritia Flexuosa mask 
that indicates with white color the presence of this palm. From these images, we extracted image patches of 512 x 512.

The MauFlex dataset can be downloaded from here: http://didt.inictel-uni.edu.pe/dataset/MauFlex_Dataset.rar

# Citation
Use this Bibtex to cite this repository

```
@Article{f9120736,
AUTHOR = {Morales, Giorgio and Kemper, Guillermo and Sevillano, Grace and Arteaga, Daniel and Ortega, Ivan and Telles, Joel},
TITLE = {Automatic Segmentation of Mauritia flexuosa in Unmanned Aerial Vehicle (UAV) Imagery Using Deep Learning},
JOURNAL = {Forests},
VOLUME = {9},
YEAR = {2018},
NUMBER = {12},
ARTICLE-NUMBER = {736},
URL = {https://www.mdpi.com/1999-4907/9/12/736},
ISSN = {1999-4907},
DOI = {10.3390/f9120736}
}
```
