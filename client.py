import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import socketio
import requests
import threading
import time

API_URL = 'http://localhost:5000'
sio = socketio.Client()

current_user = None
current_room = None
message_box = None
message_input = None
room_label = None

BG_COLOR = "#0f0f0f"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#0066cc"
LIGHT_ACCENT = "#0088ff"
BUTTON_COLOR = "#0066cc"
DARK_BG = "#1a1a1a"
INPUT_BG = "#2d2d2d"


def setup_socket_events():
    global message_box, message_input, current_room
    
    @sio.on('connect')
    def on_connect():
        pass
    
    @sio.on('disconnect')
    def on_disconnect():
        pass
    
    @sio.on('receive_message')
    def handle_message(data):
        if message_box is None:
            return
        message_box.config(state=tk.NORMAL)
        if data['username'] == current_user['username']:
            message_box.insert(tk.END, "[YOU]: ", "own")
            message_box.insert(tk.END, data['message'] + "\n", "own")
        else:
            message_box.insert(tk.END, "[" + data['username'] + "]: ", "other")
            message_box.insert(tk.END, data['message'] + "\n", "other")
        message_box.see(tk.END)
        message_box.config(state=tk.DISABLED)
    
    @sio.on('user_joined')
    def on_user_joined(data):
        if message_box is None:
            return
        message_box.config(state=tk.NORMAL)
        message_box.insert(tk.END, ">> " + data['message'] + "\n", "system")
        message_box.see(tk.END)
        message_box.config(state=tk.DISABLED)


def connect_socket():
    try:
        sio.connect(API_URL)
        threading.Thread(target=sio.wait, daemon=True).start()
        setup_socket_events()
        return True
    except:
        messagebox.showerror("Error", "Cannot connect to server")
        return False


def send_login_request(username, password):
    try:
        response = requests.post(
            API_URL + '/api/auth/login',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200:
            return response.json()['user']
        else:
            messagebox.showerror("Error", response.json().get('message', 'Login failed'))
            return None
    except:
        messagebox.showerror("Error", "Connection failed")
        return None


def send_signup_request(username, email, password):
    try:
        response = requests.post(
            API_URL + '/api/auth/signup',
            json={'username': username, 'email': email, 'password': password}
        )
        if response.status_code == 201:
            return response.json()['user']
        else:
            messagebox.showerror("Error", response.json().get('message', 'Signup failed'))
            return None
    except:
        messagebox.showerror("Error", "Connection failed")
        return None


def login_screen(root):
    global current_user
    
    window = tk.Toplevel(root)
    window.title("Login")
    window.geometry("380x350")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)
    
    title_frame = tk.Frame(window, bg=ACCENT_COLOR, height=70)
    title_frame.pack(fill=tk.X)
    tk.Label(title_frame, text="Login", font=("Arial", 22, "bold"), fg=FG_COLOR, bg=ACCENT_COLOR).pack(pady=18)
    
    content_frame = tk.Frame(window, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
    
    tk.Label(content_frame, text="Username:", font=("Arial", 11, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(0, 6))
    username_input = tk.Entry(content_frame, width=35, font=("Arial", 11), bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0)
    username_input.pack(fill=tk.X, pady=(0, 15), ipady=8)
    
    tk.Label(content_frame, text="Password:", font=("Arial", 11, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(0, 6))
    password_input = tk.Entry(content_frame, width=35, font=("Arial", 11), show="•", bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0)
    password_input.pack(fill=tk.X, pady=(0, 25), ipady=8)
    
    def do_login():
        username = username_input.get().strip()
        password = password_input.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Fill all fields")
            return
        
        user = send_login_request(username, password)
        if user:
            current_user = user
            if connect_socket():
                time.sleep(0.2)
                window.destroy()
                show_chat_screen(root)
    
    button_frame = tk.Frame(content_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X)
    
    tk.Button(button_frame, text="Login", width=18, font=("Arial", 11, "bold"), 
              bg=BUTTON_COLOR, fg=FG_COLOR, command=do_login, relief=tk.FLAT, activebackground=LIGHT_ACCENT, activeforeground=FG_COLOR).pack(side=tk.LEFT, padx=(0, 8), ipady=6)
    tk.Button(button_frame, text="Cancel", width=18, font=("Arial", 11), 
              bg="#444444", fg=FG_COLOR, command=window.destroy, relief=tk.FLAT, activebackground="#555555").pack(side=tk.LEFT, ipady=6)


def signup_screen(root):
    global current_user
    
    window = tk.Toplevel(root)
    window.title("Sign Up")
    window.geometry("380x450")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)
    
    title_frame = tk.Frame(window, bg=ACCENT_COLOR, height=70)
    title_frame.pack(fill=tk.X)
    tk.Label(title_frame, text="Create Account", font=("Arial", 22, "bold"), fg=FG_COLOR, bg=ACCENT_COLOR).pack(pady=18)
    
    content_frame = tk.Frame(window, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
    
    tk.Label(content_frame, text="Username:", font=("Arial", 11, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(0, 6))
    username_input = tk.Entry(content_frame, width=35, font=("Arial", 11), bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0)
    username_input.pack(fill=tk.X, pady=(0, 12), ipady=8)
    
    tk.Label(content_frame, text="Email:", font=("Arial", 11, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(0, 6))
    email_input = tk.Entry(content_frame, width=35, font=("Arial", 11), bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0)
    email_input.pack(fill=tk.X, pady=(0, 12), ipady=8)
    
    tk.Label(content_frame, text="Password:", font=("Arial", 11, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(0, 6))
    password_input = tk.Entry(content_frame, width=35, font=("Arial", 11), show="•", bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0)
    password_input.pack(fill=tk.X, pady=(0, 25), ipady=8)
    
    def do_signup():
        username = username_input.get().strip()
        email = email_input.get().strip()
        password = password_input.get().strip()
        
        if not all([username, email, password]):
            messagebox.showerror("Error", "Fill all fields")
            return
        
        user = send_signup_request(username, email, password)
        if user:
            current_user = user
            if connect_socket():
                time.sleep(0.2)
                window.destroy()
                show_chat_screen(root)
    
    button_frame = tk.Frame(content_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X)
    
    tk.Button(button_frame, text="Sign Up", width=18, font=("Arial", 11, "bold"), 
              bg=BUTTON_COLOR, fg=FG_COLOR, command=do_signup, relief=tk.FLAT, activebackground=LIGHT_ACCENT, activeforeground=FG_COLOR).pack(side=tk.LEFT, padx=(0, 8), ipady=6)
    tk.Button(button_frame, text="Cancel", width=18, font=("Arial", 11), 
              bg="#444444", fg=FG_COLOR, command=window.destroy, relief=tk.FLAT, activebackground="#555555").pack(side=tk.LEFT, ipady=6)


def show_chat_screen(root):
    global current_room, message_box, message_input, room_label
    
    if current_room is None:
        current_room = "general"
    
    window = tk.Toplevel(root)
    window.title("Chat")
    window.geometry("700x750")
    window.configure(bg=BG_COLOR)
    
    header_frame = tk.Frame(window, bg=ACCENT_COLOR, height=80)
    header_frame.pack(fill=tk.X, side=tk.TOP)
    
    header_left = tk.Frame(header_frame, bg=ACCENT_COLOR)
    header_left.pack(side=tk.LEFT, padx=20, pady=15, fill=tk.Y)
    
    tk.Label(header_left, text="CHAT APP", font=("Arial", 16, "bold"), fg=FG_COLOR, bg=ACCENT_COLOR).pack(anchor="w")
    room_label = tk.Label(header_left, text="Room: " + current_room, font=("Arial", 11), fg="#cccccc", bg=ACCENT_COLOR)
    room_label.pack(anchor="w", pady=(5, 0))
    
    header_right = tk.Frame(header_frame, bg=ACCENT_COLOR)
    header_right.pack(side=tk.RIGHT, padx=20, pady=15)
    
    def change_room():
        dialog = tk.Toplevel(window)
        dialog.title("Switch Room")
        dialog.geometry("350x200")
        dialog.configure(bg=BG_COLOR)
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Enter room name:", font=("Arial", 11, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=15)
        room_input = tk.Entry(dialog, width=30, font=("Arial", 11), bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0)
        room_input.pack(padx=20, pady=10, ipady=8, fill=tk.X)
        room_input.insert(0, current_room)
        
        def join():
            global current_room
            new_room = room_input.get().strip()
            if new_room:
                current_room = new_room
                room_label.config(text="Room: " + new_room)
                message_box.config(state=tk.NORMAL)
                message_box.delete(1.0, tk.END)
                message_box.config(state=tk.DISABLED)
                sio.emit('join_room', {'room': new_room, 'username': current_user['username']})
                dialog.destroy()
        
        tk.Button(dialog, text="Join Room", font=("Arial", 11, "bold"), bg=BUTTON_COLOR, fg=FG_COLOR, 
                  command=join, relief=tk.FLAT).pack(pady=10, ipadx=30, ipady=6)
    
    tk.Button(header_right, text="Switch Room", font=("Arial", 10), bg=LIGHT_ACCENT, fg=FG_COLOR, 
              command=change_room, relief=tk.FLAT, activebackground=LIGHT_ACCENT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)
    
    message_box = scrolledtext.ScrolledText(window, height=22, width=85, font=("Arial", 10),
                                             bg="#1a1a1a", fg=FG_COLOR, state=tk.DISABLED, wrap=tk.WORD, bd=0)
    message_box.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)
    
    message_box.tag_config("system", foreground="#FFB84D", font=("Arial", 10, "italic"))
    message_box.tag_config("own", foreground="#4CAF50", font=("Arial", 10, "bold"))
    message_box.tag_config("other", foreground="#87CEEB", font=("Arial", 10))
    
    sio.emit('join_room', {'room': current_room, 'username': current_user['username']})
    
    input_frame = tk.Frame(window, bg=DARK_BG)
    input_frame.pack(fill=tk.X, padx=15, pady=10)
    
    message_input = tk.Entry(input_frame, width=70, font=("Arial", 11), 
                              bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0)
    message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
    
    def send_msg(event=None):
        msg = message_input.get().strip()
        if msg:
            sio.emit('send_message', {
                'room': current_room,
                'message': msg,
                'username': current_user['username'],
                'userId': current_user['id']
            })
            message_input.delete(0, tk.END)
    
    message_input.bind('<Return>', send_msg)
    
    tk.Button(input_frame, text="Send", font=("Arial", 11, "bold"), 
              bg=BUTTON_COLOR, fg=FG_COLOR, command=send_msg, relief=tk.FLAT, 
              activebackground=LIGHT_ACCENT, padx=25, pady=10).pack(side=tk.LEFT)


def main():
    root = tk.Tk()
    root.title("Chat App")
    root.geometry("550x500")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)
    
    header = tk.Frame(root, bg=ACCENT_COLOR, height=120)
    header.pack(fill=tk.X)
    
    tk.Label(header, text="CHAT APP", font=("Arial", 32, "bold"), fg=FG_COLOR, bg=ACCENT_COLOR).pack(pady=(25, 10))
    tk.Label(header, text="Real-time Messaging", font=("Arial", 12), fg="#cccccc", bg=ACCENT_COLOR).pack(pady=(0, 15))
    
    content = tk.Frame(root, bg=BG_COLOR)
    content.pack(fill=tk.BOTH, expand=True, padx=35, pady=40)
    
    tk.Label(content, text="Welcome", font=("Arial", 14, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=(0, 8))
    tk.Label(content, text="Choose an option to get started", font=("Arial", 10), fg="#999999", bg=BG_COLOR).pack(pady=(0, 35))
    
    button_frame = tk.Frame(content, bg=BG_COLOR)
    button_frame.pack(fill=tk.X)
    
    tk.Button(button_frame, text="Login", width=22, font=("Arial", 13, "bold"), 
              bg=BUTTON_COLOR, fg=FG_COLOR, command=lambda: login_screen(root), 
              relief=tk.FLAT, padx=20, pady=13, activebackground=LIGHT_ACCENT, activeforeground=FG_COLOR).pack(pady=12, fill=tk.X)
    
    tk.Button(button_frame, text="Sign Up", width=22, font=("Arial", 13, "bold"), 
              bg="#666666", fg=FG_COLOR, command=lambda: signup_screen(root), 
              relief=tk.FLAT, padx=20, pady=13, activebackground="#777777", activeforeground=FG_COLOR).pack(pady=12, fill=tk.X)
    
    root.mainloop()


if __name__ == '__main__':
    main()
