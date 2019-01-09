# GEOVAR: Geometric Variation

Automatic generation of **all possible** _geometric variations_ from a _constrained part_.
> _**constrained object(s)** refers to any part designed, generated, and/or rendered around a set of variables (e.g. width, length, thickness, etc.)_

> _**geometric variations**, variants, or derivatives refers to any part created from altering, modifying, or changing the value of a single or multiple variables that define an original, constrained object_

> _**all possible** refers to the number of permutations dependent on the original object's number of constraints (Nvars) and the range of possible values for ech constraint (Nvals)_

---

## Requirements

GEOVAR currently relies on [Onshape](https://www.onshape.com/) and Onshape's public [repositories](https://github.com/onshape-public) for baseline design, constraint definitions, geometric variation generation, .STL exporting.

---

## Implementation

1.  **Create a _constrained part_ using Onshape's configurations**
    
    > **NOTE** Constraints can be imposed to an **Onshape** document through **variables** or **configurations**. Here we recommend the       use of **configurations** as these feature _default_, _minimum_, and _maximum_ value parameters.
    
    To learn how to implement **configurations**, follow this Onshape [tutorial](https://www.onshape.com/videos/introducing-onshape-configurations).
    
    **permute** is the example Onshape part available to test the implementation of **GEOVAR**. Search for **permute** within Onshape's public domain and create a copy for testing and validation
    
<img align="center" src="https://github.com/pd3d/geovar/blob/win3/media/fig_onshape_permute.PNG">



### Windows

1. Install the latest version of [Python 3](https://www.python.org/downloads/windows/) by following the link, make sure to click on the ___"Add Python 3.x to PATH".___ This is very vital for the modules to be loaded.
<p align="center"><img src="https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/windows/install-python.png" alt="python_addPath" width="550"/></p>

2. After Python has been installed, install the _```onshapepy```_ module by typing the following in a command prompt
```
py -3 -m pip3 install --upgrade pip
py -3 -m pip3 install onshapepy
```

3. Now that the module is installed and ready, create a file named _```onshapepy```_ in your home directory ```C:\Users\<USER_NAME>\```, where ```<USER_NAME>``` is to be replaced with the user name for the desktop machine. Within _```onshapepy```_ file, specify your credentials as follows:
```
creds:
    access_key: *******YOUR API KEY*******
    secret_key: *******YOUR API SECRET****
```
If you haven't generated your access and secrets keys yet, do so [here](https://dev-portal.onshape.com/keys). Lastly, right click _```onshapepy```_ and rename it _```.onshapepy.```_, the last dot will be dropped automatically and you'll have _```.onshapepy```_

4. No step 4, you are now ready!

### UNIX (i.e Ubuntu)

1. Install Python 3 by issuing the following commands in a terminal,
```
sudo apt update
sudo apt install python3 python3-pip
```

2. Get the _```onshapepy```_ module,
```
pip3 install --upgrade pip
pip3 install onshapepy
```

3. Place the generated API keys in the user's home directory under _```.onshapepy```_
```
cd ~
nano .onshapepy
```
Then copy the API keys using the same format as in the Windows section.
