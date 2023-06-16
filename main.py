from tkinter import *
import model
## from [chat coding] import [whatever that isneeded like]

BG_COLOR = "#BD8E4C"
BG_WHITE = "#FFFFFF"
TEXT_BLACK = "#000000"
TEXT_WHITE = "#FFFFFF"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatBotGUI:

  def __init__(self):
    self.window = Tk()
    self._setup_main_window()

  def run(self):
    self.window.mainloop()

  def _setup_main_window(self):
    self.window.title("MahallahBot")
    self.window.resizable(width=False, height=False)
    self.window.configure(width=470, height=650, bg=BG_COLOR)
    
    # Head Label
    head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_WHITE,
                       text="MahallahBot\nFor Male Mahallah Only", font=FONT_BOLD, pady=10)
    head_label.place(relwidth=1)

    # Text Widget
    self.text_widget = Text(self.window, width=20, height=2,
                            bg=BG_WHITE, fg=TEXT_BLACK, font=FONT,
                            padx=5, pady=5)
    self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
    self.text_widget.configure(cursor="arrow", state=DISABLED)

    #disclaimer message
    disclaimer_msg = "Disclaimer: This chatbot does not support female Mahallah Q&A\n"
    self.text_widget.configure(state=NORMAL)
    self.text_widget.insert(END, disclaimer_msg)
    self.text_widget.configure(state=DISABLED)
    
    # Scroll Bar
    scrollbar = Scrollbar(self.text_widget)
    scrollbar.place(relheight=1, relx=0.974)
    scrollbar.configure(command=self.text_widget.yview)
    
    # Bottom Label
    bottom_label = Label(self.window, bg=BG_COLOR, height=80)
    bottom_label.place(relwidth=1, rely=0.825)
    
    # Message Entry Box
    self.msg_entry = Entry(bottom_label, bg=BG_WHITE, fg=TEXT_BLACK,
                           font=FONT)
    self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008,
                         relx=0.011)
    self.msg_entry.focus()
    self.msg_entry.bind("<Return>", self._on_enter_pressed)
    
    # Send Button
    send_button = Button(bottom_label, text="Send", font=FONT_BOLD,
                         width=20, bg=BG_WHITE, command=lambda: self._on_enter_pressed(None))
    send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

  def _on_enter_pressed(self, event):
    msg = self.msg_entry.get()
    self._insert_message(msg, "You")
    
  def _insert_message(self, msg, sender):
    if not msg:
      return
    
    self.msg_entry.delete(0, END)
    msg1 = f"{sender}: {msg}\n\n"
    self.text_widget.configure(state=NORMAL)
    self.text_widget.insert(END, msg1)
    self.text_widget.configure(state=DISABLED)
    
    # calling chat from main.py
    bot_response = model.chat(inp=msg)
    msg2 = f"Mahallah Bot: {bot_response}\n\n"
    self.text_widget.configure(state=NORMAL)
    self.text_widget.insert(END, msg2)
    self.text_widget.configure(state=DISABLED)
    
    self.text_widget.see(END)

if __name__ == "__main__":
  app = ChatBotGUI()
  app.run()