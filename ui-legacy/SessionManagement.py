from ui.BookSession import BookSessionUI
from ui.Base import BaseUI

class SessionManagementUI(BaseUI):
    def __init__(self, user_id):
        super().__init__("GymPro: Session Management")
        self.user_id = user_id
        
        self._StartGridBuild()
        
        self._AddButton("New Session", event=self.__e_BookSessionPressed)
        self._AddButton("View Booked Sessions", event=self.__e_ViewBookedSessionsPressed)
        self._AddButton("Cancel Session", event=self.__e_CancelSessionPressed)
        
        self._EndGridBuild()
    
    def __e_BookSessionPressed(self, event):
        self.next_gui = BookSessionUI(self.user_id)
        self.next_gui.Show()
        
    def __e_ViewBookedSessionsPressed(self, event):
        # Jamie!!!
        pass

    def __e_CancelSessionPressed(self, event):
        # Jamie
        # NOTE: This is going to be avery big headache...
        # Iterate over all he sessions, display them all, and let the user press on it to cancel it.
        # not sure if we'll be able to get it done.
        pass