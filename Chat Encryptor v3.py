from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt
from cryptography.fernet import Fernet
import pyperclip, win10toast, keyboard

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(250, 250)
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Chat Encrytion Software")
        self.label=QLabel(parent=self,text='<h1>Chat Encryptor</h1')
        layout.addWidget(self.label, alignment= Qt.AlignmentFlag.AlignCenter)
        self.label=QLabel(parent=self,text='Enter key sent by host:-')
        layout.addWidget(self.label, alignment= Qt.AlignmentFlag.AlignCenter)
        self.input = QLineEdit()
        self.input.setFixedWidth(150)
        key=self.input.text()
        layout.addWidget(self.input, alignment= Qt.AlignmentFlag.AlignCenter)
        def ok():
            print(ok)
        def encrypt():
            data = pyperclip.paste().encode('utf-8')
            fern = Fernet(key)
            pyperclip.copy(fern.encrypt(data).decode('utf-8'))
            n=win10toast.ToastNotifier()
            n.show_toast(title="Encrypt and chat", msg="message encrypted..paste to send encrypted message")
        def decrypt():
            try:
                data = pyperclip.paste().encode('utf-8')
                fer = Fernet(key)
                dec = str(fer.decrypt(data).decode('utf-8'))
            except Exception as e:
                err='An error occurred', f"On decrypting data, the following exception occured (probably the key or the message to be decrypted is invalid): \n {e}"
                error_msg=QMessageBox(text=err)
                error_msg.setIcon(QMessageBox.Icon.Critical)
                error_msg.exec()
                dec = "ERROR: <an error occured while decrypting this message>"
                pyperclip.copy(dec)
                n=win10toast.ToastNotifier()
                n.show_toast(title="Encrypt and chat", msg=f"decrypted message reads: {dec}")
                text='decrypted message', f"deccrypted message: \n {dec}"
                decrypted_msg=QMessageBox(text=text)
                decrypted_msg.setIcon(QMessageBox.Icon.Information)
                decrypted_msg.exec()
        keyboard.add_hotkey("ctrl+e", encrypt)
        keyboard.add_hotkey("ctrl+d", decrypt)
        
        #Instruction Dialog
        msg=QMessageBox(text="""
Instructions on how to use the program:\n
Key is copied to your clipboard after you either ask for a new key or type the new key into dialog box.\n
To use the program. share the program with your friends and ask them to download and set it up. once thats done, run the program\n
this time when the dialog asks if u require a new key. select "yes" and then the new key will be copied to your clipboard.\n
share the new key with your friends over a secure channel\n
Once the deired recipient recieves the key, they have to run the program and select "no" at the prompt asking you "if u require a new key".\n
once they select "no" they will have to type in the key sent by you and finally run the program by clicking "ok".
 and then use the following steps to encrypt or decrypt.\n
to encrypt: select and copy (ctrl+c) the text to encrypt and press ctrl+e to encrypt.. press ctrl+V to paste the encrypted data\n
to decrypt: select and paste (ctrl+c) the text to decrypt and press ctrl+d to decrypt.. then press ctrl+v to see the decrypted text\n
decrypted text also appears on the notification shown after decyption\n""",parent=self)
        msg.setWindowTitle("Usage Instructions")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
        
        #Key Gen Dialog
        msg=QMessageBox(parent=self,text="Do you require a new key?")
        msg.setWindowTitle("Key Generation")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        ret=msg.exec()
        if ret==16384:
            key = Fernet.generate_key()
            pyperclip.copy(str(key.decode('utf-8')))
            text='Your key is :\n {} \n It has been copied to clipboard for you already'.format(key)
            key_msg=QMessageBox(parent=self,text=text)
            key_msg.setWindowTitle("Key Gen")
            key_msg.setIcon(QMessageBox.Icon.Warning)
            key_msg.exec()            


app = QApplication([])
window = Window()
window.show()
app.exec()
