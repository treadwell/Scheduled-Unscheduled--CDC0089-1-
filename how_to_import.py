# option 1 

main.py
scripts/ # this works if scripts/ is on your path, in this case in the local folder
-- __init__.py # can be blank
-- script1.py
-- script2.py

import scripts
# or
from scripts import script1 
from scripts.script1 import my_fn
from scripts.script1 import my_fn as mf

# option 2

# in the import file
import sys
sys.path.append("./scripts")
import script1
import script2

