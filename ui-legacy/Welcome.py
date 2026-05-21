import wx

from ui.CardInput import CardInputUI
from ui.Dashboard import UserDashboardUI
from ui.MembershipManagement import MembershipManagementUI

# INTERNAL IMPORTS
from .Base import BaseUI

# UNDERSCORE DEFINITIONS
#     - _ = Protected
#     - __ = Private
    
# PARENT ROOT GUI
class WelcomeUI(BaseUI):
    """Root UI that leads to every other UI

    Args:
        BaseUI (class): BaseUI framework for building quick and beautiful UIs with wxWidgets.
    """
    def __init__(self):
        # ^ is the Bitwise XOR operation. By XORing default frame style with resizing we remove resizing.
        super().__init__("GymPro: Welcome")
        
        self._StartGridBuild()
        
        self._AddText("Welcome to GymPro", span=(1, 2))
        
        self._AddText("Email: ")
        self.email_field = self._AddTextbox((1, 1))
        
        self._AddText("Password: ")
        self.password_field = self._AddTextbox((2, 1))
        
        widget_login_button = self._AddButton("Login / Register", span=(1, 2), event=self.__e_onLoginButtonPress)

        self._EndGridBuild()
    
    def __e_onLoginButtonPress(self, event):
        # Jamie: Implement user login / register here
        
        user_id = 0
        email = self.email_field.GetValue()
        password = self.password_field.GetValue()
        
        
        # Once the user is logged in / registered, run this code.
        # in DashboardGUI() pass in the user ID returned by the database.
        self.next_gui = UserDashboardUI(user_id)
        self.next_gui.Show()
        self.Destroy()
        