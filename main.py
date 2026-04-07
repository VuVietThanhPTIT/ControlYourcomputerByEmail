import threading
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from PIL import ImageGrab

from recieve_email import ReceiveEmail
from send_email import Send


def screen_shot():
    image = ImageGrab.grab()
    return image


class MailWatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mail Control Computer App")
        self.root.geometry("640x420")

        self.receiver = ReceiveEmail()
        self.sender = Send()

        self.running = False
        self.worker = None
        self.poll_interval = 3.0
        self.last_seen_command = None

        self.command_subject_var = tk.StringVar(value="cmd")
        self.interval_var = tk.StringVar(value="3")

        self._build_ui()

    def _build_ui(self):
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=12, pady=10)

        tk.Label(top, text="Subject lenh:").grid(row=0, column=0, sticky="w")
        tk.Entry(top, textvariable=self.command_subject_var, width=16).grid(row=0, column=1, padx=8)

        tk.Label(top, text="Thoi gian doc mail (giay):").grid(row=0, column=2, sticky="w")
        tk.Entry(top, textvariable=self.interval_var, width=8).grid(row=0, column=3, padx=8)

        tk.Button(top, text="Cap nhat thoi gian", command=self.update_interval).grid(row=0, column=4, padx=8)

        actions = tk.Frame(self.root)
        actions.pack(fill="x", padx=12)

        self.start_btn = tk.Button(actions, text="Start", width=10, command=self.start)
        self.start_btn.pack(side="left")

        self.stop_btn = tk.Button(actions, text="Stop", width=10, command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=8)

        self.status_label = tk.Label(actions, text=f"Status: Stopped | Interval: {self.poll_interval}s", fg="red")
        self.status_label.pack(side="left", padx=10)

        self.log_box = ScrolledText(self.root, height=18)
        self.log_box.pack(fill="both", expand=True, padx=12, pady=12)
        self.log_box.configure(state="disabled")

    def _log(self, message):
        now = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{now}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _safe_log(self, message):
        self.root.after(0, lambda: self._log(message))

    def update_interval(self):
        try:
            value = float(self.interval_var.get().strip())
            if value <= 0:
                raise ValueError
            self.poll_interval = value
            self.status_label.configure(
                text=f"Status: {'Running' if self.running else 'Stopped'} | Interval: {self.poll_interval}s"
            )
            self._log(f"Da cap nhat thoi gian doc mail: {self.poll_interval}s")
        except ValueError:
            messagebox.showerror("Loi", "Nhap so giay hop le > 0")

    def start(self):
        if self.running:
            return

        self.update_interval()
        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text=f"Status: Running | Interval: {self.poll_interval}s", fg="green")
        self._log("Da bat watcher")

        self.worker = threading.Thread(target=self._watch_loop, daemon=True)
        self.worker.start()

    def stop(self):
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text=f"Status: Stopped | Interval: {self.poll_interval}s", fg="red")
        self._log("Da dung watcher")

    def _watch_loop(self):
        while self.running:
            try:
                sender, subject = self.receiver.read_latest_body()
                cmd = self.command_subject_var.get().strip().lower()
                current = (sender.strip().lower(), subject.strip().lower())

                if current != self.last_seen_command:
                    self.last_seen_command = current
                    self._safe_log(f"Mail moi: from={sender} | subject={subject}")

                    if subject.strip().lower() == cmd:
                        self.sender.send_image(subject="screenshot", image=screen_shot())
                        self._safe_log("Da gui screenshot")
            except Exception as ex:
                self._safe_log(f"Loi: {ex}")

            time.sleep(self.poll_interval)


def main():
    root = tk.Tk()
    app = MailWatcherApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop(), root.destroy()))
    root.mainloop()


# class Keylogger:
#     def __init__(self, interval , email = email_sender, password = key , log = ""):
#         self.interval = interval
#         self.email = email
#         self.password = password
#         self.log = log
        

    # def append_to_log(self, string):
    #     self.log = self.log + string

    # def process_key_press(self, key):
    #     try:
    #         current_key = str(key.char)
    #     except AttributeError:
    #         if key == key.space:
    #             current_key = " "
    #         elif key == key.esc:
             
    #             return False
    #         else:
    #             current_key = " " + str(key) + " "
    #     self.append_to_log(current_key)

    # def report(self):
    #     if self.log != "":
            
    #         # print(f"\n[REPORTING TO EMAIL]:\n{self.log}")
    #         self.log = "" # Reset log sau khi gửi
        
    #     timer = threading.Timer(self.interval, self.report)
    #     timer.start()

    # def start(self):
    #     keyboard_listener = keyboard.Listener(on_press=self.process_key_press)
    #     with keyboard_listener:
    #         self.report()
    #         keyboard_listener.join()

if __name__ == "__main__":
    main()
        

