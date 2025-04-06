## Class containing all details that KiCad needs to generate symbol
import ast
import inspect
class PopulateKiCadDetails:
    def __init__(self):
        self.KiCadDetails = {
            "ModelDescriptionFile": None, # Link to Function documentation
            "RectangleEndX": 29.21, # Coordinates of top right rectangle corner
            "RectangleEndY": 5.08, # Coordinated of top right rectangle corner
        }

    def populateDetails(self, File, InputCount, OutputCount):
        details = self.KiCadDetails.copy()
        details["ModelDescription"] = File
        EdgeOffset = 1.27
        InputSpacing = 2.54
        details["RectangleEndX"] = 29.21
        details["RectangleEndY"] = EdgeOffset*2 + InputCount*InputSpacing

        return details

    def blockSize(self, InputCount, OutputCount):
        portCount = max(InputCount, OutputCount)
        EdgeOffset = 1.27
        InputSpacing = 2.54
        details = {"RectangleEndX": 29.21, "RectangleEndY":0}

        details["RectangleEndY"] = EdgeOffset*2 + InputCount*InputSpacing

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
                    return keys 