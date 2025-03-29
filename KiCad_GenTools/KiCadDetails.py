## Class containing all details that KiCad needs to generate symbol
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