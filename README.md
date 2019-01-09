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
> **NOTE** The following steps apply to all operating systems and applications

1.  **Create a _constrained part_ using Onshape's configurations**
    
    > **NOTE** Constraints can be imposed to an **Onshape** document through **variables** or **configurations**. Here we recommend the       use of **configurations** as these feature _default_, _minimum_, and _maximum_ value parameters.
    
    To learn how to implement **configurations**, follow this Onshape [tutorial](https://www.onshape.com/videos/introducing-onshape-configurations).
    
    **permute** is the example Onshape part available to test the implementation of **GEOVAR**. Search for **permute** within Onshape's public domain and create a copy for testing and validation
    
<img align="center" src="https://github.com/pd3d/geovar/blob/win3/media/fig_onshape_permute.PNG">

2.  **Generate Onshape API Access and Secret keys**
    1.  Log into Onshape's [developer portal](https://dev-portal.onshape.com/keys)
    2.  Select `Create new API key`
    3.  Select all the permissions required by your application
        > **GEOVAR** only requires permission to: **read your documents**, **write to your documents**, and **delete your documents and      workspaces**.

<img align="center" src="https://github.com/pd3d/geovar/blob/win3/media/fig_keys.PNG">    

---

### Windows
> **NOTE** The following steps only apply to users and/or application using/running on a **Windows OS**
> **WARNING** The following tests have only been tested/validated on **Windows 7 and 10**

1.  **Install the latest version of [Python 3](https://www.python.org/downloads/windows/)**
    > **NOTE** Make sure to add Python 3.x to the Windows **PATH** variable.

<img align="center" src="https://github.com/pd3d/geovar/blob/win3/media/fig_python_install.png">

2.  **Install the `onshapepy` module by typing the following in a command prompt**
> **NOTE** Remember to always run the command prompt as **administrator**
```
py -3 -m pip install --upgrade pip
py -3 -m pip install onshapepy
```
3.  **Create a file using a text editor like Notepad**
    1.  Within the file, type the following information;
        ```
        creds:
            access_key: *******YOUR API KEY*******
            secret_key: *******YOUR API SECRET****
        ```
    2.  Replace the `*******YOUR API KEY*******` and `*******YOUR API SECRET****` sections with the keys retrieved from Onshape's developer portal
    3.  Save file within the **user directory** `C:\Users\<USER_NAME>\`, using the **filename** `.onshapepy.`
    > **NOTE** Both **periods** on the `.onshapepy.` name are necessary. The last period will be dropped automaticall upon saving.

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
