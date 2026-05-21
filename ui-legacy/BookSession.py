from ui.Base import BaseUI

class BookSessionUI(BaseUI):
    """UI for booking sessions.

    Args:
        BaseUI (class): Base class for building wxWidget uis.
    """
    def __init__(self, user_id):
        super().__init__("GymPro: Book")
        self.user_id = user_id
        
        self._StartGridBuild()
        
        self._AddCalendar()
        self._AddButton("Book", event=self.__e_BookSessionButtonPressed)
        
        self._EndGridBuild()
    
    def __e_BookSessionButtonPressed(self, event):
        # Jamie: Write the date to the database
        pass