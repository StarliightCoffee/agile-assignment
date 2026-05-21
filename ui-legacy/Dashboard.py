
from ui.Base import BaseUI
from ui.SessionManagement import SessionManagementUI
from ui.MembershipManagement import MembershipManagementUI
from ui.ParkingManagement import ParkingManagement


class UserDashboardUI(BaseUI):
    def __init__(self, user_id : int):
        super().__init__("GymPro: Dashboard")
        self.user_id = user_id
        
        self._StartGridBuild()
        
        self._AddText("Statistics", underline=True)
        
        self._AddDivider()
        
        self._AddText("Management", underline=True)
        
        self._AddButton("Membership Management", event=self.__e_MembershipManagementPressed)
        self._AddButton("Parking Management", event=self.__e_ParkingManagementPressed)
        self._AddButton("Book a Session", event=self.__e_BookASessionPressed)
        self._AddButton("Delete Account ", event=self.__e_DeleteAccountPressed)
        
        self._EndGridBuild()
    
    def __e_MembershipManagementPressed(self, event):
        self.next_gui = MembershipManagementUI(self.user_id)
        self.next_gui.Show()
        
    def __e_ParkingManagementPressed(self, event):
        self.next_gui = ParkingManagement(self.user_id)
        self.next_gui.Show()
    def __e_BookASessionPressed(self, event):
        self.next_gui = SessionManagementUI(self.user_id)
        self.next_gui.Show()
    def __e_DeleteAccountPressed(self, event):
        pass