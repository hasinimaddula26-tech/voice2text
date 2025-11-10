import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import threading

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 165)

def speak(text):
    """Speak text aloud"""
    engine.say(text)
    engine.runAndWait()

def listen_and_transcribe():
    """Record and convert voice to text"""
    with sr.Microphone() as source:
        speak("Listening now. Say 'exit' to stop.")
        text_box.insert(tk.END, "🎙 Listening...\n")
        text_box.see(tk.END)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            text_box.insert(tk.END, f"🗣 You said: {text}\n")
            text_box.see(tk.END)
            if "exit" in text.lower():
                speak("Goodbye!")
                window.destroy()
            else:
                speak("Got it.")
                results.append(text)
        except sr.WaitTimeoutError:
            text_box.insert(tk.END, "⏳ No speech detected. Stopping...\n")
            text_box.see(tk.END)
        except sr.UnknownValueError:
            text_box.insert(tk.END, "❌ Couldn't understand.\n")
            text_box.see(tk.END)
        except sr.RequestError:
            text_box.insert(tk.END, "⚠️ Network or API error.\n")
            text_box.see(tk.END)

def start_listening():
    threading.Thread(target=listen_and_transcribe).start()

def save_text():
    """Save transcribed text to file"""
    with open("voice_text_output.txt", "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
    speak("Text saved to file.")
    text_box.insert(tk.END, "✅ Saved to voice_text_output.txt\n")
    text_box.see(tk.END)

# GUI setup
window = tk.Tk()
window.title("🎤 Voice to Text App")
window.geometry("600x400")

results = []

label = tk.Label(window, text="🎙 Click 'Start Recording' and speak", font=("Arial", 14))
label.pack(pady=10)

text_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=15, font=("Consolas", 10))
text_box.pack(padx=10, pady=10)

start_btn = tk.Button(window, text="🎧 Start Recording", command=start_listening, bg="#4CAF50", fg="white", font=("Arial", 12))
start_btn.pack(pady=5)

save_btn = tk.Button(window, text="💾 Save Text", command=save_text, bg="#2196F3", fg="white", font=("Arial", 12))
save_btn.pack(pady=5)

window.mainloop()
