## Class containing all details that KiCad needs to generate symbol
import ast
import inspect
import math
class PopulateKiCadDetails:
    def __init__(self):
        self.KiCadDetails = {
            "ModelDescriptionFile": None, # Link to Function documentation
            "RectangleEndX": 29.21, # Coordinates of top right rectangle corner
            "RectangleEndY": 5.08, # Coordinated of top right rectangle corner
        }

        self.EdgeOffset = 1.27
        self.InputSpacing = 2.54

    def populateDetails(self, File, InputCount, OutputCount):
        details = self.KiCadDetails.copy()
        details["ModelDescription"] = File
        details["RectangleEndX"] = 29.21
        details["RectangleEndY"] = self.EdgeOffset*2 + InputCount*self.InputSpacing

        return details

    def blockSize(self, InputCount, OutputCount):
        portCount = max(InputCount, OutputCount)

        details = {"RectangleEndX": 29.21, "RectangleEndY":0}

        details["RectangleEndY"] = self.EdgeOffset*2 + InputCount*self.InputSpacing

        return details

    def outputName(self, funcName):
        functionSource = inspect.getsource(funcName)
        tree = ast.parse(functionSource)
        returnName = 0
        for node in ast.walk(tree):
            # Traverse the called function (line by line)

            if isinstance(node, ast.Return):
                # Line with the Return function is found
                # Log the variable defined as Return
                returnDetected = node.value

                # Check the data type of the Return
                if isinstance(returnDetected, ast.Name):
                    returnName = returnDetected.id

                elif isinstance(returnDetected, ast.BinOp):
                    returnName = ast.dump(returnDetected, indent=4)

                else:
                    print("Return value type:", type(returnDetected).__name__)
                    print(ast.dump(returnDetected))
                    returnName = 0

        return returnName

    def outputStructure(self, funcName):
        # Return all dict components of the function 'return'
        functionSource = inspect.getsource(funcName)
        tree = ast.parse(functionSource)

        for node in ast.walk(tree):
            # Traverse the called function (line by line)
            if isinstance(node, ast.Assign):
                # Looks for any assign operation in the function
                # The function has to be formatted to have output dict assigned to 'output'
                if (isinstance(node.targets[0], ast.Name) and
                        node.targets[0].id == 'output' and
                        isinstance(node.value, ast.Dict)):
                    keys = []
                    for key in node.value.keys:
                        if isinstance(key, ast.Constant):  # Python 3.8+
                            keys.append(key.value)
                    return list(keys)
    # The limitation is that you need to decide how you want to interact with the functino
    # If you want all the output components than using 'return name' makes sense
    # If you want just one output, then the 'return name' should be more descriptive than output

    def datasheetImport(self, funcName):
        # Return all dict components of the function 'return'
        functionSource = inspect.getsource(funcName)
        tree = ast.parse(functionSource)

        for node in ast.walk(tree):
            # Traverse the called function (line by line)
            if isinstance(node, ast.Assign):
                # Looks for any assign operation in the function
                # The function has to be formatted to have output dict assigned to 'output'
                if (isinstance(node.targets[0], ast.Name) and
                        node.targets[0].id == 'Datasheet' ):
                    return node.value.value


    def populateFunctionDetails(self, functionDetails, file):

        # Calculate the block width based on the longest input and output name (count characters)
        width = 29.21
        name = functionDetails["Name"]
        link = functionDetails["Datasheet"]
        height = functionDetails["height"]
        functionName = functionDetails["Name"]
        inputList = functionDetails["inputList"]
        outputList = functionDetails["OutputList"]
        inputCount = functionDetails["inputCount"]
        outputCount = functionDetails["outputCount"]

        self.blocDescription(file, functionName, link, height, width)
        self.pinDescription(file, functionName, inputList, outputList, outputCount, height, width)

        return 0

    def blocDescription(self, file, functionName, link, height, width):
        file.write(f'  (symbol "{functionName}" (pin_numbers hide) (in_bom yes) (on_board yes)\n')
        file.write(f'    (property "Reference" "DS?" (id 0) (at -6.35 2.54 0)\n')
        file.write(f'      (effects (font (size 1.27 1.27)))\n')
        file.write(f'    )\n')
        # Label symbol
        file.write(f'    (property "Value" "{functionName}" (id 1) (at 0 7.62 0)\n')
        file.write(f'      (effects (font (size 1.27 1.27)))\n')
        file.write(f'    )\n')
        # Define PCB footprint (N/A)
        file.write(f'    (property "Footprint" "" (id 2) (at 0 0 0)\n')
        file.write(f'      (effects (font (size 1.27 1.27)) hide)\n')
        file.write(f'    )\n')
        # Define documentation location
        file.write(f'    (property "Datasheet" "{link}" (id 3) (at 0 0 0)\n')
        file.write(f'      (effects (font (size 1.27 1.27)) hide)\n')
        file.write(f'    )\n')
        # Define symbol shape
        file.write(f'    (symbol "{functionName}_0_1"\n')
        file.write(f'      (rectangle (start 0 0) (end {width} {height["RectangleEndY"]})\n')
        file.write(f'        (stroke (width 0) (type default) (color 0 0 0 0))')
        file.write(f'        (fill (type background))\n')
        file.write(f'      )\n')
        file.write(f'    )\n')

        return 0

    def pinDescription(self, file, functionName, inPinList, outputData, outputLabel, height, width):

        # Define header
        file.write(f'    (symbol "{functionName}_1_1"\n')
        # Define inputs
        for inputNumber in range(len(inPinList)):
            pinOffset = self.EdgeOffset + inputNumber * self.InputSpacing
            file.write(f'      (pin input line (at -2.54 {pinOffset} 0) (length 2.54)\n')
            file.write(f'        (name "{inPinList[inputNumber]}" (effects (font (size 1 1))))\n')
            file.write(f'        (number "" (effects (font (size 1 1))))\n')
            file.write(f'      )\n')
        # Define outputs
        if outputLabel == 1:
            # There is no extended output dict passed by the function, use the return label
            outputLocationHorizontal = width + 2.54
            test = type(height)
            outputLocationVertical = ((math.floor((height["RectangleEndY"] - (2*self.EdgeOffset))/2))*self.InputSpacing)+self.EdgeOffset
            file.write(f'      (pin output line (at {outputLocationHorizontal} {outputLocationVertical} 180) (length 2.54)\n')
            file.write(f'        (name "{outputLabel}" (effects (font (size 1 1))))\n')
            file.write(f'        (number "" (effects (font (size 1 1))))\n')
            file.write(f'      )\n')
        else:
            for outputCount in range(len(outputData)):
                horizontalOffset = width+2.54
                verticalOffset = self.EdgeOffset+outputCount*self.InputSpacing
                file.write(f'      (pin output line (at {horizontalOffset} {verticalOffset} 180) (length 2.54)\n')
                file.write(f'        (name "{outputData[outputCount]}" (effects (font (size 1 1))))\n')
                file.write(f'        (number "" (effects (font (size 1 1))))\n')
                file.write(f'      )\n')

        file.write("    )\n")
        file.write("  )\n")
        return 0