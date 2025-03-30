from KiCadDetails import PopulateKiCadDetails

import ast
import os
import SampleFunctions
import inspect

functions_list = [name for name, obj in inspect.getmembers(SampleFunctions, inspect.isfunction)]

print(functions_list)


