from enum import Enum

token = '5181103933:AAG4SaRyyqC4AytezzrD-x8h-nl9TLkja1w'
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
    M_SEND_PIC = "Отправьте изображение, На которе хотите наложить стиль"
    M_PIC_RECIVED = "Изображение получено. Теперь отправьте изображение стиля"
    M_SEND_STYLE = "Отправьте изображение стиля"
    M_STYLE_RECIVED = "Изображение стиля получено"
    M_PROCESSING = "Идёт обработка. Ждите"
    M_RESULT = "Вот ваш результат:"
    M_END = "Отлично! Если захочешь пообщаться снова - отправь команду /start."


class IS_PROCESSING:
    def __init__(self):
        self.is_processing = False

    def __str__(self):
        return str(self.is_processing)

    def change(self, new_state):
        assert isinstance(new_state,bool)
        self.is_processing = new_state

is_processing = IS_PROCESSING()