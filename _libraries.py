"""
Libraries and Modules
"""

# onshape modules and libraries
from    onshapepy.play              import  *                           # Onshape API

# adapted onshape modules and libraries
import  _setup
import  _onshape
import  _morph
import  _mesh
import  _febio

# additional python modules and libraries
from    time                        import  sleep, time                 # Timers/delays
from    platform                    import  system                      # Running platform info
from    datetime                    import  datetime                    # Get date and time
from    argparse                    import  ArgumentParser              # Add input arguments to script
from    itertools                   import  product                     # Apply product rule on combinations
import  numpy                       as      np                          # Fast array creation
import  os, re   
