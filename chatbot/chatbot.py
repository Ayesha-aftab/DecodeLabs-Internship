import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import sqlite3

# =========================
# DATABASE SETUP
# =========================
conn = sqlite3.connect("chat_history.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    message TEXT,
    time TEXT
)''')
conn.commit()

# =========================
# AI RESPONSE LOGIC
# =========================
def get_ai_response(user_input):
    user_input = user_input.lower().strip()

    if not user_input:
        return "I didn't catch that. Could you type something?"
    elif "hello" in user_input or "hi" in user_input:
        return "Hello! 👋 How can I help you today?"
    elif "your name" in user_input:
        return "I am your decodelabs Chatbot 🤖"
    elif "time" in user_input:
        return "The current time is " + datetime.now().strftime("%I:%M %p")
    elif "date" in user_input:
        return "Today's date is " + datetime.now().strftime("%B %d, %Y")
    elif "bye" in user_input or "exit" in user_input:
        return "exit"
    elif "ai" in user_input:
        return "(AI MODE Placeholder) Connect an LLM API here for advanced smart responses."
    else:
        return "I am still learning, but I'm here to help! 🤖"

def save_chat(sender, message):
    cursor.execute("INSERT INTO chats (sender, message, time) VALUES (?, ?, ?)",
                   (sender, message, datetime.now().strftime("%H:%M:%S")))
    conn.commit()

# =========================
# MAIN APP & UI DESIGN
# =========================
root = tk.Tk()
root.title("decodelabs Chatbot")
root.geometry("500x700")
root.configure(bg="#0f172a")  # Deep slate background

# Theme Palettes
DARK_THEME = {
    "bg": "#0f172a", "header": "#1e293b", "chat_bg": "#111827", 
    "chat_fg": "#f8fafc", "entry_bg": "#1e293b", "entry_fg": "#ffffff",
    "btn_bg": "#3b82f6", "btn_fg": "#ffffff"
}

LIGHT_THEME = {
    "bg": "#f1f5f9", "header": "#ffffff", "chat_bg": "#ffffff", 
    "chat_fg": "#0f172a", "entry_bg": "#e2e8f0", "entry_fg": "#0f172a",
    "btn_bg": "#2563eb", "btn_fg": "#ffffff"
}

current_theme = "dark"

# =========================
# THEME TOGGLE FUNCTION
# =========================
def toggle_theme():
    global current_theme
    t = LIGHT_THEME if current_theme == "dark" else DARK_THEME
    current_theme = "light" if current_theme == "dark" else "dark"
    
    root.configure(bg=t["bg"])
    header.configure(bg=t["header"])
    header_label.configure(bg=t["header"], fg=t["chat_fg"])
    theme_btn.configure(bg=t["entry_bg"], fg=t["chat_fg"])
    chat_area.configure(bg=t["chat_bg"], fg=t["chat_fg"])
    input_frame.configure(bg=t["bg"])
    entry.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["entry_fg"])
    send_btn.configure(bg=t["btn_bg"], fg=t["btn_fg"])

# =========================
# HEADER COMPONENT
# =========================
header = tk.Frame(root, bg=DARK_THEME["header"], height=70)
header.pack(fill=tk.X, ipady=10)
header.pack_propagate(False)

header_label = tk.Label(header, text="decodelabs Chatbot",
                        fg=DARK_THEME["chat_fg"], bg=DARK_THEME["header"],
                        font=("Segoe UI", 16, "bold"))
header_label.pack(side=tk.LEFT, padx=20, pady=10)

theme_btn = tk.Button(header, text="🌓", font=("Segoe UI", 12),
                      bg=DARK_THEME["entry_bg"], fg=DARK_THEME["chat_fg"],
                      bd=0, cursor="hand2", activebackground="#334155", command=toggle_theme)
theme_btn.pack(side=tk.RIGHT, padx=20, pady=10)

# =========================
# CHAT AREA WIDGET
# =========================
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD,
                                      font=("Segoe UI", 11),
                                      bg=DARK_THEME["chat_bg"], fg=DARK_THEME["chat_fg"],
                                      bd=0, highlightthickness=0, padx=15, pady=15)
chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
chat_area.config(state=tk.DISABLED)

# Custom Text Tags for layout bubbles
chat_area.tag_configure("User_Header", foreground="#94a3b8", font=("Segoe UI", 9, "bold"))
chat_area.tag_configure("Bot_Header", foreground="#3b82f6", font=("Segoe UI", 9, "bold"))
chat_area.tag_configure("Msg_Body", spacing3=15)

# =========================
# MESSAGE RENDERING
# =========================
def add_message(sender, msg):
    chat_area.config(state=tk.NORMAL)
    time_now = datetime.now().strftime("%I:%M %p")
    
    if sender == "User":
        chat_area.insert(tk.END, f"🧑 You • {time_now}\n", "User_Header")
    else:
        chat_area.insert(tk.END, f"🤖 Bot • {time_now}\n", "Bot_Header")
        
    chat_area.insert(tk.END, f"{msg}\n\n", "Msg_Body")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)
    save_chat(sender, msg)

# =========================
# TYPING SIMULATION
# =========================
def handle_bot_reply(response):
    # Strip away the temporary placeholder text
    chat_area.config(state=tk.NORMAL)
    # Simple trick to clear "typing..." lines if implemented, or just post directly
    add_message("Bot", response)

def send_message():
    user_text = entry.get().strip()
    if not user_text:
        return

    add_message("User", user_text)
    entry.delete(0, tk.END)

    response = get_ai_response(user_text)

    if response == "exit":
        add_message("Bot", "Goodbye! Closing application... 👋")
        root.after(1500, root.destroy)
    else:
        # 400ms delay gives a natural software feel without locking UI threads
        root.after(400, lambda: handle_bot_reply(response))

# =========================
# MODERNIZE INPUT BAR
# =========================
input_frame = tk.Frame(root, bg=DARK_THEME["bg"])
input_frame.pack(fill=tk.X, padx=15, pady=(0, 20))

entry = tk.Entry(input_frame, font=("Segoe UI", 12),
                 bg=DARK_THEME["entry_bg"], fg=DARK_THEME["entry_fg"],
                 bd=0, highlightthickness=8, highlightbackground=DARK_THEME["entry_bg"],
                 highlightcolor=DARK_THEME["entry_bg"], insertbackground="white")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
entry.bind("<Return>", lambda event: send_message())

send_btn = tk.Button(input_frame, text="Send", font=("Segoe UI", 11, "bold"),
                     bg=DARK_THEME["btn_bg"], fg=DARK_THEME["btn_fg"],
                     bd=0, padx=20, cursor="hand2", activebackground="#2563eb",
                     command=send_message)
send_btn.pack(side=tk.RIGHT, padx=(10, 0), ipady=6)

# =========================
# INITIALIZATION
# =========================
add_message("Bot", "Welcome! I'm your premium local chatbot interface. Type a message below to begin. 🚀")

root.mainloop()