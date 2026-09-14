from tkinter import *
from tkinter import messagebox
from mydb import Database
from myapi import API

class NlpApp:
    def __init__(self):

        self.dbo = Database()
        self.apio = API()

        self.root = Tk()
        self.root.title("NLP App")
        try:
            self.root.iconbitmap("resources/favicon.ico")
        except Exception:
            pass
        self.root.geometry("400x650")
        self.root.config(bg="#493782")

        self.login_gui()
        self.root.mainloop()

    def login_gui(self):
        self.clear()

        self.nlp_label = Label(self.root, text="NLP App", font=("Arial", 24), bg="#493782", fg="white")
        self.nlp_label.pack(pady=20)

        self.login_label = Label(self.root, text="Login", font=("Arial", 18), bg="#493782", fg="white")
        self.login_label.pack(pady=4)

        self.username_label = Label(self.root, text="Username:", font=("Arial", 12), bg="#493782", fg="white")
        self.username_label.pack(pady=10)
        self.username_entry = Entry(self.root, font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.username_entry.pack(pady=5, ipady=4)

        self.password_label = Label(self.root, text="Password:", font=("Arial", 12), bg="#493782", fg="white")
        self.password_label.pack(pady=10)
        self.password_entry = Entry(self.root, show="*", font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.password_entry.pack(pady=5, ipady=4)

        self.login_button = Button(self.root, text="Login", command=self.perform_login, highlightthickness=8, pady=6)
        self.login_button.pack(pady=24)

        self.register_label = Button(self.root, text="Don't have an account? Register", font=("Arial", 12), bg="#493782", fg="black", command=self.register_gui)
        self.register_label.pack(pady=10)

    def perform_login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        response = self.dbo.search(email, password)

        if response:
            messagebox.showinfo('success', 'Login successful')
            self.home_gui()
        else:
            messagebox.showerror('error', 'Incorrect email/password')

    def register_gui(self):
        self.clear()

        self.nlp_label = Label(self.root, text="NLP App", font=("Arial", 24), bg="#493782", fg="white")
        self.nlp_label.pack(pady=20)

        self.register_label = Label(self.root, text="Register", font=("Arial", 18), bg="#493782", fg="white")
        self.register_label.pack(pady=4)

        self.name_label = Label(self.root, text="Name:", font=("Arial", 12), bg="#493782", fg="white")
        self.name_label.pack(pady=10)
        self.name_entry = Entry(self.root, font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.name_entry.pack(pady=5, ipady=4)

        self.email_label = Label(self.root, text="Email:", font=("Arial", 12), bg="#493782", fg="white")
        self.email_label.pack(pady=10)
        self.email_entry = Entry(self.root, font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.email_entry.pack(pady=5, ipady=4)

        self.password_label = Label(self.root, text="Password:", font=("Arial", 12), bg="#493782", fg="white")
        self.password_label.pack(pady=10)
        self.password_entry = Entry(self.root, show="*", font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.password_entry.pack(pady=5, ipady=4)

        self.register_button = Button(self.root, text="Register", command=self.perform_register, highlightthickness=8, pady=6)
        self.register_button.pack(pady=24)

        self.login_redirect_btn = Button(self.root, text="Already have an account? Login", font=("Arial", 12), bg="#493782", fg="black", command=self.login_gui)
        self.login_redirect_btn.pack(pady=10)

    def perform_register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        response = self.dbo.add_data(name, email, password)

        if response:
            messagebox.showinfo('success', 'Registration successful')
            self.home_gui()
        else:
            messagebox.showerror('error', 'Email already exists')

    def home_gui(self):
        self.clear()

        self.nlp_label = Label(self.root, text="NLP App", font=("Arial", 24), bg="#493782", fg="white")
        self.nlp_label.pack(pady=20)

        self.sentiment_button = Button(self.root, text="Sentiment Analysis", font=("Arial", 12), fg="black", width=20, pady=10, command=self.sentiment_gui)
        self.sentiment_button.pack(pady=10)

        self.emotional_analysis = Button(self.root, text="Emotion Analysis", font=("Arial", 12), fg="black", width=20, pady=10, command=self.emotion_gui)
        self.emotional_analysis.pack(pady=10)

        self.language_analysis = Button(self.root, text="Language Analysis", font=("Arial", 12), fg="black", width=20, pady=10, command=self.language_gui)
        self.language_analysis.pack(pady=10)

        self.logout = Button(self.root, text="Logout", font=("Arial", 12), fg="black", pady=8, command=self.login_gui)
        self.logout.pack(pady=60)

    def sentiment_gui(self):
        self.clear()

        self.nlp_label = Label(self.root, text="NLP App", font=("Arial", 24), bg="#493782", fg="white")
        self.nlp_label.pack(pady=20)

        self.sentiment_label = Label(self.root, text="Sentiment Analysis", font=("Arial", 18), bg="#493782", fg="white")
        self.sentiment_label.pack(pady=4)

        self.text_label = Label(self.root, text="Enter Text:", font=("Arial", 12), bg="#493782", fg="white")
        self.text_label.pack(pady=10)
        self.sentiment_entry = Entry(self.root, font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.sentiment_entry.pack(pady=5, ipady=4)

        self.analyze_button = Button(self.root, text="Analyze Sentiment", command=self.perform_sentiment_analysis, highlightthickness=8, pady=6)
        self.analyze_button.pack(pady=16)

        self.sentiment_result = Label(self.root, text="", font=("Arial", 12), bg="#493782", fg="white")
        self.sentiment_result.pack(pady=10)

        self.back_button = Button(self.root, text="Back to Home", font=("Arial", 12), bg="#493782", fg="black", command=self.home_gui)
        self.back_button.pack(pady=10)

    def perform_sentiment_analysis(self):
        text = self.sentiment_entry.get()
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text")
            return
        response = self.apio.sentiment_analysis(text)
        txt = ""
        for k, v in response['sentiment'].items():
            txt += f"{k.capitalize()} -> {int(v * 100)}%\n"
        self.sentiment_result.config(text=txt)

    def emotion_gui(self):
        self.clear()

        self.nlp_label = Label(self.root, text="NLP App", font=("Arial", 24), bg="#493782", fg="white")
        self.nlp_label.pack(pady=20)

        self.emotion_label = Label(self.root, text="Emotion Analysis", font=("Arial", 18), bg="#493782", fg="white")
        self.emotion_label.pack(pady=4)

        self.text_label = Label(self.root, text="Enter Text:", font=("Arial", 12), bg="#493782", fg="white")
        self.text_label.pack(pady=10)
        self.text_entry = Entry(self.root, font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.text_entry.pack(pady=5, ipady=4)

        self.analyze_button = Button(self.root, text="Analyze Emotion", command=self.perform_emotion_analysis, highlightthickness=8, pady=6)
        self.analyze_button.pack(pady=16)

        self.emotion_result = Label(self.root, text="", font=("Arial", 12), bg="#493782", fg="white")
        self.emotion_result.pack(pady=10)

        self.back_button = Button(self.root, text="Back to Home", font=("Arial", 12), bg="#493782", fg="black", command=self.home_gui)
        self.back_button.pack(pady=10)

    def perform_emotion_analysis(self):
        text = self.text_entry.get()
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text")
            return
        response = self.apio.emotion_analysis(text)
        txt = ""
        for k, v in response['emotion'].items():
            txt += f"{k} -> {int(v * 100)}%\n"
        self.emotion_result.config(text=txt)

    def language_gui(self):
        self.clear()

        self.nlp_label = Label(self.root, text="NLP App", font=("Arial", 24), bg="#493782", fg="white")
        self.nlp_label.pack(pady=20)

        self.lang_label = Label(self.root, text="Language Analysis", font=("Arial", 18), bg="#493782", fg="white")
        self.lang_label.pack(pady=4)

        self.text_label = Label(self.root, text="Enter Text:", font=("Arial", 12), bg="#493782", fg="white")
        self.text_label.pack(pady=10)
        self.lang_entry = Entry(self.root, font=("Arial", 12), fg="black", bg="#DBD2F7", highlightthickness=2)
        self.lang_entry.pack(pady=5, ipady=4)

        self.analyze_button = Button(self.root, text="Analyze Language", command=self.perform_language_analysis, highlightthickness=8, pady=6)
        self.analyze_button.pack(pady=16)

        self.lang_result = Label(self.root, text="", font=("Arial", 12, "bold"), bg="#493782", fg="white")
        self.lang_result.pack(pady=10)

        self.back_button = Button(self.root, text="Back to Home", font=("Arial", 12), bg="#493782", fg="black", command=self.home_gui)
        self.back_button.pack(pady=10)

    def perform_language_analysis(self):
        text = self.lang_entry.get()
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text")
            return
        response = self.apio.language_analysis(text)
        txt = f"Detected Language:\n{response['language']} ({response['code']})"
        self.lang_result.config(text=txt)

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

if __name__ == "__main__":
    nlp = NlpApp()