from KiCadDetails import PopulateKiCadDetails

import ast
import os
import SampleFunctions
import inspect

# Each loop iteration, a new function is pulled from the SampleFunctions.py
for name, func in inspect.getmembers(SampleFunctions, inspect.isfunction):

    # Define empty dict
    functionDetails = {}

    # Extract information from the function
    signature = inspect.signature(func)
    params = signature.parameters
    return_annotation = signature.return_annotation

    print({return_annotation})
    # Cyclically extract input parameters
    #for value in params.values():
    #    print(value)
    functionDetails["inputList"] = list(params.values())
    functionDetails["inputCount"] = len(functionDetails["inputList"])


    # To make the values available, you can convert them into a list
    exportedList = list(params.values())
    print(functionDetails["inputList"][0])
    print(functionDetails["inputCount"])

    # Populate other function-specific details for KICad gen


    # Generate KiCad Model Description (individual .txt file)



