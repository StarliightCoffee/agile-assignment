import wx

from ui.Base import BaseUI

# TODO: Validate card information. Right now the user can input whatever they want.

class CardInputUI(BaseUI):
    def __init__(self, user_id):
        super().__init__("GymPro: Input Card Details")
        self.user_id = user_id
        
        self._StartGridBuild()
        
        self._AddText("Card Number: ")
        self.card_number_field = self._AddTextbox((0, 1))
        
        self._AddText("CVC: ")
        self.cvc_field = self._AddTextbox((1, 1))
        
        self._AddText("Expiry: ")
        self.expiry_field = self._AddTextbox((2, 1))
        
        self._AddButton("Submit", event=self.__e_CardSubmitPressed, span=(1, 2))
        
        self._EndGridBuild()
    
    def __e_CardSubmitPressed(self, event):
        # Jamie: Implement passing data to the database.
        card_number = self.card_number_field.GetValue()
        cvc = self.cvc_field.GetValue()
        expiry = self.expiry_field.GetValue()
        
        
        pass