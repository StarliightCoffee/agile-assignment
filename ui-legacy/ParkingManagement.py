from .Base import BaseUI

class ParkingManagement(BaseUI):
    def __init__(self, user_id):
        super().__init__("Parking Management")
        self.user_id = user_id
        
        self._StartGridBuild()
        
        self._AddText("License Plate: ")
        self.w_license_plate_field = self._AddTextbox(pos=(0, 1))
        
        self._AddButton("Park / Unpark", span=(1, 2), event=self.__e_ParkButtonPressed)
        
        self._EndGridBuild()
    
    def __GetParkingStatus(self):
        # Jamie: Pass database information and return the status w/ license plate.
        pass

    def __e_ParkButtonPressed(self, event):
        license_plate = self.w_license_plate_field.GetValue()
        pass