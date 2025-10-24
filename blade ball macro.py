import tkinter as tk
from tkinter import ttk
from pynput import keyboard, mouse
import time
import threading

class AutoClicker:
    def __init__(self):
        self.running = False
        self.mb4_pressed = False
        self.keyboard_controller = keyboard.Controller()
        self.click_thread = None
        self.mouse_listener = None
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("wdlj macro")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b2b')  # Dark background
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=10, font=('Helvetica', 10), background='#404040', foreground='white')
        style.configure("TLabel", font=('Helvetica', 12), background='#2b2b2b', foreground='white')
        
        # Create GUI elements
        self.status_label = ttk.Label(self.root, text="Status: Hold MB4 to start", style="TLabel")
        self.status_label.pack(pady=20)
        
        self.cps_label = ttk.Label(self.root, text="CPS: 200", style="TLabel")
        self.cps_label.pack(pady=10)
        
        self.toggle_button = ttk.Button(self.root, text="Hold MB4 to activate", command=self.toggle_clicking)
        self.toggle_button.pack(pady=20)
        
        # Background text
        self.bg_label = ttk.Label(self.root, text="wdlj", font=('Helvetica', 8), background='#2b2b2b', foreground='#666666')
        self.bg_label.pack(side='bottom', pady=5)
        
        # Bind F6 key to toggle
        self.root.bind('<F6>', lambda e: self.toggle_clicking())
        
        # Start mouse listener for MB4
        self.start_mouse_listener()
        
        # Cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_clicking(self):
        if not self.running:
            self.start_clicking()
        else:
            self.stop_clicking()

    def start_clicking(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Running (MB4 held)")
            self.click_thread = threading.Thread(target=self.auto_click)
            self.click_thread.start()

    def stop_clicking(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Hold MB4 to start")

    def start_mouse_listener(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    def on_mouse_click(self, x, y, button, pressed):
        # MB4 is typically mouse.Button.x1
        if button == mouse.Button.x1:
            self.mb4_pressed = pressed
            if pressed and not self.running:
                self.start_clicking()
            elif not pressed and self.running:
                self.stop_clicking()

    def auto_click(self):
        while self.running and self.mb4_pressed:
            self.keyboard_controller.press('f')
            self.keyboard_controller.release('f')
            time.sleep(0.005)  # 200 CPS
        # Stop if MB4 is released
        if self.running and not self.mb4_pressed:
            self.stop_clicking()

    def on_closing(self):
        self.running = False
        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join()
        if self.mouse_listener:
            self.mouse_listener.stop()
        self.root.destroy()

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Auto Clicker application...")
    try:
        auto_clicker = AutoClicker()
        print("GUI window created successfully!")
        auto_clicker.start()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")