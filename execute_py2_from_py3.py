import subprocess

script = ["python","C:/Users/WOLF512/Documents/Gits/PD3D/geovar/_paraview_stl_vis.py"]
print( " ".join(script) )
process = subprocess.Popen(" ".join(script),
                                        shell=True,  
                                        env={"PYTHONPATH": "."})
