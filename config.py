from enum import Enum

TOKEN = '5181103933:AAG4SaRyyqC4AytezzrD-x8h-nl9TLkja1w'
db_file = "database.vdb"


class States(Enum):
    S_START = "0"
    S_SEND_PIC = "1"
    S_SEND_STYLE = "2"
    S_PROCESSING = "3"


class Messages(Enum):
    #Errors
    E_SEND_PIC = "Error in get image"
    E_SEND_STYLE = "Error in get style"
    E_PROCESSING = "Error in processing"
    #Messages
    M_START = "I'm style bot. I can transfer style from one picture to another." \
              " Please send me one and I'll show you the depth of the rabbit hole." \
              "(Use /reset if something goes wrong)"
    M_SEND_PIC = "Should I repeat?!! SEND ME PICTURE please."
    M_PIC_RECIVED = "Got it. Now send me something stylish."
    M_SEND_STYLE = "Now send me something stylish."
    M_STYLE_RECIVED = "Good choice."
    M_PROCESSING = "Wait a minute. I'm not a supercomputer."
    M_RESULT = "Done!"
    M_END = "See you later. (Use /start again)"
    M_HELP = "/start to start than follow the instructions \n" \
             "/reset for strange situations \n" \
             "/help for ... I don't know. You've just used it..."



class IS_PROCESSING:
    def __init__(self):
        self.is_processing = False

    def __str__(self):
        return str(self.is_processing)

    def change(self, new_state):
        assert isinstance(new_state,bool)
        self.is_processing = new_state

is_processing = IS_PROCESSING()