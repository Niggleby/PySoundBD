import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import json

# Konfigurationsdatei
CONFIG_FILE = "config.json"
SOUND_DIR = "sounds"

# Tkinter GUI erstellen
class SoundboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soundboard")
        self.load_config()
        
        # Buttons zum Abspielen der Sounds
        self.load_sounds()
        self.create_ui()
    
    def create_ui(self):
        tk.Button(self.root, text="Sound hinzufügen", command=self.add_sound).pack()
        self.sound_frame = tk.Frame(self.root)
        self.sound_frame.pack()
        self.refresh_buttons()
    
    def load_sounds(self):
        if not os.path.exists(SOUND_DIR):
            os.makedirs(SOUND_DIR)
        self.sounds = [f for f in os.listdir(SOUND_DIR) if f.endswith((".mp3", ".wav"))]
    
    def play_sound(self, sound):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(SOUND_DIR, sound))
        pygame.mixer.music.play()
    
    def refresh_buttons(self):
        for widget in self.sound_frame.winfo_children():
            widget.destroy()
        for sound in self.sounds:
            tk.Button(self.sound_frame, text=sound, command=lambda s=sound: self.play_sound(s)).pack()
    
    def add_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            file_name = os.path.basename(file_path)
            os.rename(file_path, os.path.join(SOUND_DIR, file_name))
            self.load_sounds()
            self.refresh_buttons()
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                self.config = json.load(file)
        else:
            self.config = {}
            self.save_config()
    
    def save_config(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.config, file)

# Start
if __name__ == "__main__":
    root = tk.Tk()
    app = SoundboardApp(root)
    root.mainloop()
