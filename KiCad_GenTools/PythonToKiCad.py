from KiCadDetails import PopulateKiCadDetails

import ast
import os
import SampleFunctions
import inspect

# Each loop iteration, a new function is pulled from the SampleFunctions.py
for name, func in inspect.getmembers(SampleFunctions, inspect.isfunction):

    # Define empty dict
    functionDetails = {}

    # Log the function name
    functionDetails["Name"] = list({name})[0] # This logs the actual string
    print(functionDetails["Name"])
    #print(functionDetails["Name"][0]) # Adding the [0] prints the actual string, which is the first one in the list



    DM = PopulateKiCadDetails() # Initiate instance of the module

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

    print("test of hidden function")
    returnFunctionName = DM.outputName(func)
    print(returnFunctionName)



    # Populate other function-specific details for KICad gen


    # Generate KiCad Model Description (individual .txt file)



