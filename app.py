import tkinter as tk
from tkinter import messagebox
import datetime
import threading

# pyttsx3 இல்லையென்றால் ஆப் எரர் ஆகாமல் இருக்க இந்த ஏற்பாடு
try:
    import pyttsx3
    voice_available = True
except ImportError:
    voice_available = False

# --- பாஸ்வேர்டு அமைப்புகள் ---
ADMIN_PASS = "admintest@123"
MEMBER_PASS = "membertest@123"

class GangBoysApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GANG BOYS 🥷")
        self.root.geometry("500x750")
        self.root.configure(bg="#000000")
        
        # நிதி மற்றும் தரவுகள்
        self.income_total = 0.0
        self.expense_total = 0.0
        self.announcement = "குழு உறுப்பினர்களுக்கு வணக்கம்!"
        
        self.login_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_page(self):
        self.clear_screen()
        tk.Label(self.root, text="GANG BOYS 🥷", font=("Arial", 30, "bold"), fg="#FFD700", bg="#000000").pack(pady=40)
        
        self.entries = {}
        fields = [("பெயர்", ""), ("தொலைபேசி", ""), ("பிறந்தநாள் (DD-MM)", ""), ("பாஸ்வேர்டு", "*")]
        
        for label_text, show_char in fields:
            tk.Label(self.root, text=label_text, fg="white", bg="#000000", font=("Arial", 11)).pack()
            ent = tk.Entry(self.root, width=30, show=show_char, font=("Arial", 12))
            ent.pack(pady=5)
            self.entries[label_text] = ent

        tk.Button(self.root, text="உள்நுழை", font=("Arial", 12, "bold"), bg="#FFD700", fg="black", 
                  width=15, command=self.process_login).pack(pady=30)

    def process_login(self):
        name = self.entries["பெயர்"].get()
        pwd = self.entries["பாஸ்வேர்டு"].get()
        dob = self.entries["பிறந்தநாள் (DD-MM)"].get()
        today = datetime.datetime.now().strftime("%d-%m")

        if pwd == ADMIN_PASS or pwd == MEMBER_PASS:
            is_admin = (pwd == ADMIN_PASS)
            if dob == today:
                self.birthday_wish(name, is_admin)
            else:
                self.home_page(name, is_admin)
        else:
            messagebox.showerror("பிழை", "தவறான பாஸ்வேர்டு!")

    def birthday_wish(self, name, is_admin):
        self.clear_screen()
        tk.Label(self.root, text="🎈🎈🎈\nஇனிய பிறந்தநாள் வாழ்த்துக்கள்!\n🎈🎈🎈", 
                 font=("Arial", 20, "bold"), fg="#FFD700", bg="#000000").pack(pady=50)
        tk.Label(self.root, text=name, font=("Arial", 40, "bold"), fg="white", bg="#000000").pack()

        def speak():
            if voice_available:
                try:
                    engine = pyttsx3.init()
                    engine.say(f"Happy Birthday {name}")
                    engine.runAndWait()
                except:
                    pass

        threading.Thread(target=speak).start()
        self.root.after(4000, lambda: self.home_page(name, is_admin))

    def home_page(self, name, is_admin):
        self.clear_screen()
        tk.Label(self.root, text="🥷 GB", fg="#FFD700", bg="#000000", font=("bold", 12)).place(x=450, y=10)
        
        welcome_frame = tk.Frame(self.root, bg="#FFD700", pady=10)
        welcome_frame.pack(fill="x")
        tk.Label(welcome_frame, text=f"வரவேற்கிறோம், {name}! 🥷", bg="#FFD700", fg="black", font=("Arial", 12, "bold")).pack()

        tk.Label(self.root, text=f"📢 {self.announcement}", fg="white", bg="#333", font=("Arial", 10)).pack(fill="x", pady=5)

        btn_frame = tk.Frame(self.root, bg="#000000")
        btn_frame.pack(pady=20)

        # மெனுக்கள்
        menus = [
            ("👗 ஆடை அளவுகள்", lambda: self.dress_sizes(name, is_admin)),
            ("💰 வரவு செலவு", lambda: self.finance_page(name, is_admin)),
            ("📦 புகார் பெட்டி", lambda: self.complaint_page(name, is_admin))
        ]

        for text, cmd in menus:
            tk.Button(btn_frame, text=text, width=25, pady=8, bg="#222", fg="white", font=("Arial", 11), command=cmd).pack(pady=5)

        if is_admin:
            tk.Button(btn_frame, text="🛡️ தலைவர் அறை", width=25, pady=8, bg="#8B0000", fg="white", 
                      font=("Arial", 11, "bold"), command=lambda: self.admin_room(name)).pack(pady=10)

    def dress_sizes(self, name, is_admin):
        self.clear_screen()
        tk.Label(self.root, text="ஆடை அளவுகள்", font=("bold", 18), bg="#FFD700", fg="black").pack(fill="x", pady=10)
        
        fields = ["சட்டை அளவு", "மார்பளவு", "கையின் நீளம்"]
        for f in fields:
            tk.Label(self.root, text=f, fg="white", bg="#000000").pack(pady=5)
            tk.Entry(self.root, width=20, font=("Arial", 12)).pack()
            
        tk.Button(self.root, text="சேமி", bg="green", fg="white", command=lambda: messagebox.showinfo("Saved", "சேமிக்கப்பட்டது!")).pack(pady=20)
        tk.Button(self.root, text="Back", command=lambda: self.home_page(name, is_admin)).pack()

    def finance_page(self, name, is_admin):
        self.clear_screen()
        tk.Label(self.root, text="வரவு செலவு", font=("bold", 18), bg="#FFD700", fg="black").pack(fill="x", pady=10)
        
        bal = self.income_total - self.expense_total
        tk.Label(self.root, text=f"கையிருப்பு: ₹{bal}", font=("Arial", 25, "bold"), fg="#00FF00", bg="#000000").pack(pady=20)
        
        tk.Label(self.root, text="தொகை உள்ளிடவும்:", fg="white", bg="#000000").pack()
        amt_ent = tk.Entry(self.root, font=("Arial", 12))
        amt_ent.pack(pady=5)

        def update_val(is_inc):
            try:
                val = float(amt_ent.get())
                now = datetime.datetime.now().strftime("%I:%M %p")
                if is_inc: self.income_total += val
                else: self.expense_total += val
                messagebox.showinfo("வெற்றி", f"நேரம்: {now}\nபதிவு செய்யப்பட்டது!")
                self.finance_page(name, is_admin)
            except ValueError:
                messagebox.showerror("பிழை", "எண்களை மட்டும் உள்ளிடவும்!")

        tk.Button(self.root, text="வரவு +", bg="blue", fg="white", width=12, command=lambda: update_val(True)).pack(pady=5)
        tk.Button(self.root, text="செலவு -", bg="red", fg="white", width=12, command=lambda: update_val(False)).pack(pady=5)
        tk.Button(self.root, text="Back", command=lambda: self.home_page(name, is_admin)).pack(pady=20)

    def admin_room(self, name):
        self.clear_screen()
        tk.Label(self.root, text="தலைவர் அறை", font=("bold", 18), bg="#8B0000", fg="white").pack(fill="x", pady=10)
        tk.Label(self.root, text="புதிய அறிவிப்பு:", fg="white", bg="#000000").pack(pady=10)
        e = tk.Entry(self.root, width=40); e.pack()
        
        def save():
            self.announcement = e.get()
            messagebox.showinfo("Admin", "அறிவிப்பு வெளியிடப்பட்டது!")

        tk.Button(self.root, text="Update", command=save).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.home_page(name, True)).pack()

    def complaint_page(self, name, is_admin):
        self.clear_screen()
        tk.Label(self.root, text="புகார் பெட்டி", font=("bold", 18), bg="white", fg="black").pack(fill="x", pady=10)
        tk.Text(self.root, height=5, width=40).pack(pady=10)
        tk.Button(self.root, text="Submit", command=lambda: messagebox.showinfo("Sent", "தலைவருக்கு அனுப்பப்பட்டது")).pack()
        tk.Button(self.root, text="Back", command=lambda: self.home_page(name, is_admin)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GangBoysApp(root)
    root.mainloop()
