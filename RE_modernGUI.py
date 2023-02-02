import tkinter as tk
import tkinter
import customtkinter as ct
from tkinter import simpledialog
from tkinter.messagebox import askyesno, showinfo, showerror
from cryptography.fernet import Fernet
import cryptography
import pyperclip
import keyboard
import win10toast
from tkinter.filedialog import askopenfilename, asksaveasfile
import os
conversations = {}
class EncryptionSoftware():
    def __init__(self, key, enc, dec):
        self.key = key
        self.enc = enc
        self.dec = dec
        self.fern = Fernet(self.key)
    def files_enc(self):
        file_r = askopenfilename()
        if os.path.splitext(file_r)[-1] == '.txt':
            with open(os.path.abspath(file_r), 'r') as encfile:
                dat =  encfile.read().encode('utf-8')
        else:
            with open(os.path.abspath(file_r), 'rb') as encfile:
                dat =  encfile.read()
        file_w = asksaveasfile(mode='wb', defaultextension='.crypt')
        file_w.write(self.fern.encrypt(dat))
        file_w.close()
    def files_dec(self):
        file_r = askopenfilename()
        with open(os.path.abspath(file_r), 'rb') as encfile:
            dat =  encfile.read()
        file_w = asksaveasfile(mode='wb')
        file_w.write(self.fern.decrypt(dat))

    def encrypt(self, hotkey:bool = False, file:bool = False):
        data = pyperclip.paste().encode('utf-8') if hotkey else self.enc.get().encode('utf-8')
        pyperclip.copy(self.fern.encrypt(data).decode('utf-8'))
        n=win10toast.ToastNotifier()
        n.show_toast(title="Encrypt and chat", msg="message encrypted..paste to send encrypted message", threaded=True)
    def decrypt(self, hotkey:bool = False):
        try:
            data = pyperclip.paste().encode('utf-8')  if hotkey else self.dec.get().encode('utf-8')
            dec = str(self.fern.decrypt(data).decode('utf-8'))
        except cryptography.fernet.InvalidToken:
            showerror('An error occurred', f"On decrypting data, the following exception occured (probably the key or the message to be decrypted is invalid)")
            dec = "ERROR: <an error occured while decrypting this message>"
        pyperclip.copy(dec)
        n=win10toast.ToastNotifier()
        n.show_toast(title="Encrypt and chat", msg=f"decrypted message reads: {dec}", threaded=True)
        showinfo('decrypted message', f"decrypted message: \n {dec}")
ct.set_appearance_mode("dark")
root = ct.CTk()
root.geometry("800x400")
root.title("Encrypt and chat")
l1 = ct.CTkLabel(root, text="Encrypt and chat", font=("Segoe UI Variable", 25))
l1.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)
tabview = ct.CTkTabview(root, width=800)
tabview.pack(padx=20, pady=60)
showinfo("How to use?", """
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
decrypted text also appears on the notification shown after decyption\n
NEW!: You can now add new conversations by presing the new tab button""")
def keyret():
    answer = askyesno("new key", "do you require a new key?")
    if answer: 
        key = Fernet.generate_key()
    else:
        keydial = ct.CTkInputDialog(text="Type in your key:", title="Enter Key")
        keystr = keydial.get_input()
        if keystr is not None: key = keystr.encode('utf-8')
        else: root.quit()
    print(key)
    pyperclip.copy(str(key.decode('utf-8')))
    n=win10toast.ToastNotifier()
    n.show_toast(title="key copied", msg="key copied to clipboard!", duration = 3, threaded=True)
    return key
def changekeys():
    n_key = keyret()
    conversations[tabview.get()][0] = n_key
    conversations[tabview.get()][1].key = n_key
def ntab():
    conv = ct.CTkInputDialog(title="Conversation name", text="Enter a name for this conversation: ")
    conv_ret = conv.get_input()
    conv_name = conv_ret if conv_ret is not None or conv_ret != "" else f"Untitled conv {len(conversations)}"
    tabview.add(conv_name)
    kb = keyret()
    l1 = ct.CTkLabel(tabview.tab(conv_name), text="Data to Encrypt")
    l1.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)
    enc = ct.CTkEntry(master=tabview.tab(conv_name),
                               placeholder_text="Data to Encrypt",
                               width=240,
                               height=25,
                               border_width=2,
                               corner_radius=10)
    enc.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    l2 = ct.CTkLabel(tabview.tab(conv_name), text="Data to Decrypt")
    l2.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    dec = ct.CTkEntry(master=tabview.tab(conv_name),
                               placeholder_text="Data to Decrypt",
                               width=240,
                               height=25,
                               border_width=2,
                               corner_radius=10)
    dec.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    conversations[conv_name] = (kb, EncryptionSoftware(kb, enc, dec))
    button_1 = ct.CTkButton(tabview.tab(conv_name), text="New conversation", command=ntab)
    button_1.place(relx=0.9, rely=0.9, anchor=tkinter.CENTER)
    check1 = ct.CTkCheckBox(master=tabview.tab(conv_name), text="File")
    check1.place(relx=0.1, rely=0.9, anchor=tkinter.CENTER)
    button_2 = ct.CTkButton(tabview.tab(conv_name), text="Decrypt", command= conversations[tabview.get()][1].decrypt if check1 == 0 else conversations[tabview.get()][1].files_dec)
    button_2.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)
    button_3 = ct.CTkButton(tabview.tab(conv_name), text="Encrypt", command=conversations[tabview.get()][1].encrypt if check1 == 0 else conversations[tabview.get()][1].files_enc)
    button_3.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
    button_4 = ct.CTkButton(tabview.tab(conv_name), text="Regenerate key", command=changekeys)
    button_4.place(relx=0.3, rely=0.9, anchor=tkinter.CENTER)
ntab()
keyboard.add_hotkey("ctrl+e", conversations[tabview.get()][1].encrypt, args=(True, ))
keyboard.add_hotkey("ctrl+d", conversations[tabview.get()][1].decrypt, args=(True, ))
root.mainloop()
#  TODO: Add FILES encryption support
#  TODO: Add individual tabs handling support
#  TODO: Add a button to re-generate a new key for a convo
#  TODO: once we make RE encryption algo, change this algo to that
#  TODO: make proper UI for encryption and decryption so that people can use this app without the hotkeys