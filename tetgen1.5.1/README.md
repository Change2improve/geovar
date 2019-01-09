
# About TetGen #
This is TetGen version 1.5.1 (released on August, 2018)

Please see the documentation of TetGen for compiling and using TetGen.
It is available at the following link:
http://www.tetgen.org

For more information on this product, contact :

  Hang Si
  Research Group of Numerical Mathematics and Scientific Computing
  Weierstrass Institute for Applied Analysis and Stochastics
  Mohrenstr. 39
  10117 Berlin, Germany

 Phone: +49 (0) 30-20372-446   Fax: +49 (0) 30-2044975
 EMail: <si@wias-berlin.de>
 Web Site: http://www.wias-berlin.de/~si

BEFORE INTALLING OR USING TetGen(R) READ the 
GENERAL LICENSE TERMS AND CONDITIONS

---

# Building TetGen on Windows #
**NOTE:** This repository already features a pre-compiled version of **TetGen** in;
```
\geovar\tetgen1.5.1\build\Debug\tetgen.exe
```
**IF** said version does not seem to operate properly, .dll files are missing, or a newer version is desired, follow these instructions;
> **WARNING** The following instructions have been tested for: **TetGen 1.5.1, CMake 3.13.2, and Visual Studio 2017**

0.  **Download the latest version of TetGen's build files**
    1.   [tetgen-WIAS](http://wias-berlin.de/software/index.jsp?id=TetGen&lang=1#Download)
    2.   [tetgen-github](https://github.com/ufz/tetgen)
> **STEP 0 IS OPTIONAL** Rebuilding the libraries provided in the repo may resolve most execution issues, errors, etc.

1.  **Download and install the following programs:**
    1.  [CMake](https://cmake.org/download/)
        1.  _Add CMake to Windows PATH variable_
    2.  [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
    
2.  **Build TetGen using CMake and Visual Studio**
    1.  From the start menu, execute/open the **Visual Studio Command Prompt** as **administrator**
      ```
      Either of the following prompts work;
      C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat
      C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat
      ```
    2.  **Move to the TetGen directory within this repo**
      ```
      cd C:\...\...\PD3D\geovar\tetgen1.5.1
      ```
    3.  **Remove existing "build" directory**
      ```
      rmdir build /s
      ```
      > **NOTE** re-building may not overwrite old build directory, **deleting is essential**
    4.  **Create and move into new "build" directory**
      ```
      mkdir build
      cd build
      ```
    5.  **Execute CMake**
      ```
      cmake ..
      ```
      ![cmake_results](https://github.com/pd3d/geovar/blob/win2/tetgen1.5.1/cmake_results.PNG)
    
    6.  **Open Visual Studio Solution**
    
      The execution of **CMake** results in the creation of "Project" and "Solution" files readable by **Visual Studio**
    
     
---
