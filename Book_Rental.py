import sqlite3
import tkinter as tk
from tkinter import Label
from tkinter import PhotoImage
from tkinter import font
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

def setup_database():
    conn = sqlite3.connect("rental_system.db")
    cursor = conn.cursor()

        # Create user table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                email TEXT NOT NULL,
                                password TEXT NOT NULL)''')

    conn.commit()
    conn.close()

    setup_database()

class Rental_System:
    def __init__(self,root):
        self.book_title = None
        self.root = root
        self.root.title("Login")
        self.root.configure(bg='white')


        self.login_frame = tk.Frame(self.root,width=300,height=500)
        self.signup_frame = tk.Frame(self.root,width=300,height=500)

        self.login_widget()
        self.signup_widget()


        self.login_frame.place(x=0,y=0)

    def login_widget(self):

        label_login = tk.Label(self.login_frame,text="Login",font=('calibre', 20, 'normal', 'bold'))
        label_login.place(x=100,y=0)

        email_label = tk.Label(self.login_frame,text="Email",font=('calibre', 10, 'normal'))
        email_label.place(x=25,y=60)

        self.login_entry_email = customtkinter.CTkEntry(self.login_frame,placeholder_text="Email",border_width=1,fg_color='white',width=250,height=35,border_color='grey',text_color='black')
        self.login_entry_email.place(x=25,y=85)

        password_label = tk.Label(self.login_frame, text="Password", font=('calibre', 10, 'normal'))
        password_label.place(x=25, y=130)

        self.login_entry_password = customtkinter.CTkEntry(self.login_frame, placeholder_text="Password", border_width=1,
                                             fg_color='white', width=250,height=35,border_color='grey',text_color='black')
        self.login_entry_password.place(x=25, y=155)

        login_btn = customtkinter.CTkButton(self.login_frame,text="Login", width=250, height=35,command=self.login)
        login_btn.place(x=25,y=210)

        underline_font = font.Font(family="Helvetica", size=10, underline=True)

        button_signup = tk.Button(self.login_frame,text="Create an account.",border=0,fg='blue',cursor="hand2",font=underline_font,command=self.show_signup_frame)
        button_signup.place(x=25, y=250)

        intro_label = tk.Label(self.login_frame,text="Discover a simple way to borrow \nbooks. Browse our collection, pick\nyour favorites, and enjoy flexible\n borrowing periods. With easy online\naccess and secure payments, finding\nyour next great read has never been\neasier.",font=('calibre', 10, 'normal'))
        intro_label.place(x=2,y=280,width=300,height=140)

    def signup_widget(self):

        label_signup = tk.Label(self.signup_frame, text="Signup", font=('calibre', 20, 'normal', 'bold'))
        label_signup.place(x=100, y=0)

        username_label = tk.Label(self.signup_frame, text="Username", font=('calibre', 10, 'normal'))
        username_label.place(x=25, y=60)

        self.signup_entry_username = customtkinter.CTkEntry(self.signup_frame, placeholder_text="Email", border_width=1,
                                                     fg_color='white', width=250, height=35, border_color='grey',
                                                     text_color='black')
        self.signup_entry_username.place(x=25, y=85)

        email_label = tk.Label(self.signup_frame, text="Email", font=('calibre', 10, 'normal'))
        email_label.place(x=25, y=130)

        self.signup_entry_email = customtkinter.CTkEntry(self.signup_frame, placeholder_text="Email", border_width=1,
                                                  fg_color='white', width=250, height=35, border_color='grey',
                                                  text_color='black')
        self.signup_entry_email.place(x=25, y=155)

        password_label = tk.Label(self.signup_frame, text="Password", font=('calibre', 10, 'normal'))
        password_label.place(x=25, y=200)

        self.signup_entry_password = customtkinter.CTkEntry(self.signup_frame, placeholder_text="Password", border_width=1,
                                                     fg_color='white', width=250, height=35, border_color='grey',
                                                     text_color='black')
        self.signup_entry_password.place(x=25, y=220)

        signup_btn = customtkinter.CTkButton(self.signup_frame, text="Signup", width=250, height=35,
                                             command=self.register)
        signup_btn.place(x=25, y=270)

        underline_font = font.Font(family="Helvetica", size=10, underline=True)

        button_login = tk.Button(self.signup_frame, text="Already have an account?", border=0, fg='blue', cursor="hand2",
                                 font=underline_font,command=self.show_login_frame)
        button_login.place(x=25, y=310)

        intro_label = tk.Label(self.signup_frame,
                               text="Discover a simple way to borrow \nbooks. Browse our collection, pick\nyour favorites, and enjoy flexible\n borrowing periods. With easy online\naccess and secure payments, finding\nyour next great read has never been\neasier.",
                               font=('calibre', 10, 'normal'))
        intro_label.place(x=2, y=340, width=300, height=140)

    def login(self):
        email = self.login_entry_email.get()
        password = self.login_entry_password.get()

        self.conn = sqlite3.connect(
            'rental_system.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM user WHERE email = ? AND password = ?', (email, password))
        row = self.cursor.fetchone()
        self.conn.close()

        if row:
            messagebox.showinfo("Login Info", "Welcome, you are logged in!")
            root.destroy()
            self.main()


        else:
            messagebox.showerror("Login Error", "Invalid Email or password")

    def register(self):
        username = self.signup_entry_username.get()
        password = self.signup_entry_password.get()
        email = self.signup_entry_email.get()

        conn = sqlite3.connect('rental_system.db')
        cursor = conn.cursor()

        if username == "" or password == "" or email == "":
            messagebox.showerror("Error", "Please fill in all fields!")
        else:
            try:
                cursor.execute('INSERT INTO user ( username, email, password) VALUES (?,?,?)', (username, email, password))
                conn.commit()
                messagebox.showinfo("Registration Info", "User registered successfully!")
                self.signup_frame.place_forget()
                self.login_frame.place(x=0, y=0)
            except sqlite3.IntegrityError:
                messagebox.showerror("Registration Error", "Username already exists")

            conn.close()

    def show_signup_frame(self):
        self.login_frame.place_forget()
        self.signup_frame.place(x=0,y=0)

    def show_login_frame(self):
        self.signup_frame.place_forget()
        self.login_frame.place(x=0, y=0)

    def main(self):
        self.main_window = tk.Tk()
        self.main_window.title("Main Window")
        self.main_window.geometry("300x500+500+150")
        self.main_window.resizable(0, 0)
        self.main_window.configure(bg='white')

        self.menu_image = PhotoImage(file='menu.png')
        self.menu_resized = self.menu_image.subsample(22, 22)
        self.close_image = PhotoImage(file='close.png')
        self.close_resized = self.close_image.subsample(4, 4)
        self.search_image = PhotoImage(file='search.png')
        self.search_resized = self.search_image.subsample(5, 5)

        # Frames
        top_frame = tk.Frame(self.main_window, bg='white')
        top_frame.pack(side=tk.TOP, fill=tk.X)
        top_frame.config(height=30)

        tagline_frame = tk.Frame(self.main_window,bg='white')
        tagline_frame.place(x=0, y=26, width=500, height=70)

        searchbar_frame = customtkinter.CTkFrame(self.main_window, width=250, height=30, border_width=0, corner_radius=20,
                                                 fg_color='#F0F0F0')
        searchbar_frame.place(x=25, y=100)
        searchbar_frame.configure(height=30)

        self.item_frame = tk.Frame(self.main_window,bg='white')
        self.item_frame.place(x=0,y=150,width=300,height=400)

        # Header
        self.toggle_btn = tk.Button(top_frame, image=self.menu_resized, command=self.show_menu, border=0, bg='white')
        self.toggle_btn.pack(side=tk.LEFT)

        title_lb = tk.Label(top_frame, text='BoBOOK Ka?', bg='white', font=("Arial Rounded MT Bold", 15))
        title_lb.place(x=80, y=0)

        # Tagline
        tagline = Label(tagline_frame, text="Thousands of books with different genre", font=("Arial", 10),bg='white')
        tagline2 = Label(tagline_frame, text="Waiting for you!", font=("Arial Rounded MT Bold", 15),bg='white')
        tagline.place(x=10, y=10)
        tagline2.place(x=10, y=30)

        # Search bar
        self.search_entry = tk.Entry(searchbar_frame, width=30, border=0,bg='#F0F0F0')
        self.search_entry.place(x=30, y=5, height=20)
        self.search_entry.bind("<Return>", self.perform_search)

        search_icon = Label(searchbar_frame,image=self.search_resized,bg='#F0F0F0')
        search_icon.place(x=5,y=3)

        self.items_container = customtkinter.CTkScrollableFrame(self.item_frame,width=290,height=310,fg_color='white')
        self.items_container.place(x=0,y=30)

        self.recommend_label = tk.Label(self.item_frame, text="Recommended Books",font=("calibre", 10, "bold"),bg='white')
        self.recommend_label.place(x=5,y=0)

        books = self.load_recommended_books()
        for book in books:
            cover_url = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg"
            response = requests.get(cover_url)
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            recommended_button = tk.Button(self.items_container, image=photo, text=book["title"], compound=tk.BOTTOM, bg='white',
                                    border=0, command=lambda b=book: self.open_book_details(b))
            recommended_button.image = photo  # Keep a reference to avoid garbage collection
            recommended_button.pack()

    # Show and close the menu bar
    def show_menu(self):
        def collapse_toggle_menu():
            toggle_menu_frame.destroy()
            self.toggle_btn.config(image=self.menu_resized)
            self.toggle_btn.config(command=self.show_menu)
            self.toggle_btn.config(bg='white')

        toggle_menu_frame = tk.Frame(self.main_window, bg='black')
        window_height = 500
        toggle_menu_frame.place(x=0, y=26, width=200, height=window_height)
        self.toggle_btn.config(bg='black')
        self.toggle_btn.config(image=self.close_resized)
        self.toggle_btn.config(command=collapse_toggle_menu)

        home_btn = tk.Button(toggle_menu_frame, text='Home', border=0, fg='white', bg='grey')
        home_btn.place(x=0, y=3, width=200, height=30)

    def load_recommended_books(self):
        url = "https://openlibrary.org/subjects/science_fiction.json?limit=8"
        response = requests.get(url)
        data = response.json()
        books = data['works']
        return books

    def search_books(self, title):
        url = f"https://openlibrary.org/search.json"
        params = {'title': title}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['docs']:
                self.display_books(data['docs'])
            else:
                messagebox.showinfo("No books found", "No books found for the given title.")
        else:
            messagebox.showerror("Error", "Failed to fetch data.")

    def perform_search(self, event=None):
        title = self.search_entry.get()
        self.search_books(title)

    def display_books(self, books):
        for widget in self.items_container.winfo_children():
            self.recommend_label.place_forget()
            widget.destroy()

        for i, book in enumerate(books[:8]):  # Show top 8 results
            title = book['title']

            if 'cover_i' in book:
                cover_id = book['cover_i']
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                response = requests.get(cover_url)
                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))
                    image.thumbnail((200, 200))
                    photo = ImageTk.PhotoImage(image)
                    book_button = tk.Button(self.items_container, image=photo, text=title, compound=tk.BOTTOM, bg='white',
                                            border=0,command=lambda b=book: self.open_book_details(b))
                    book_button.image = photo  # Keep a reference to avoid garbage collection
                    book_button.pack()
            else:
                cover_url = "No cover available"

    def open_book_details(self, book):
        details_window = tk.Tk()
        details_window.title(book['title'])
        details_window.geometry("300x500+500+150")
        details_window.resizable(0, 0)

        # Create a frame for book details
        details_frame = tk.Frame(details_window, bg="#F2F2F2", bd=2, relief="flat")
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Back Button (Top-Left)
        back_button = tk.Button(details_window, text="← Back", font=("Arial", 10, "bold"), bg="lightGray", fg="black",
                                padx=10, pady=5, command=details_window.destroy)
        back_button.place(x=10, y=10)  # Position at the top-left

        # Initialize cart count if not already set
        if not hasattr(self, "cart_count"):
             self.cart_count = 0

        # Load Book Cover
        if 'cover_i' in book:
            cover_url = f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg"
            response = requests.get(cover_url)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((150, 200))
                photo = ImageTk.PhotoImage(image)

                cover_label = tk.Label(details_frame, image=photo, bg='white')
                cover_label.image = photo  # Keep reference
                cover_label.pack(pady=10)

        # Book Title
        title_label = tk.Label(details_frame, text=book['title'], font=("Arial", 14, "bold"), bg='#F2F2F2', wraplength=350)
        title_label.pack(anchor="w", padx=10)

        # Author Name
        author_name = book.get('authors', [{'name': 'Unknown Author'}])[0]['name']
        author_label = tk.Label(details_frame, text=f"Author: {author_name}", font=("Arial", 10), bg='#F2F2F2')
        author_label.pack(anchor="w", padx=10)

        book_genre = tk.Label(details_frame, text="Genre: Fantasy, Drama, Action", font=('Arial', 10, 'bold'),bg="#F2F2F2")
        book_genre.pack(anchor="w", padx=10)

        # Fetch and Display Synopsis Dynamically
        synopsis_text = book.get('description', "No synopsis available for this book.")

        if isinstance(synopsis_text, dict):  # Sometimes OpenLibrary returns a dict
            synopsis_text = synopsis_text.get('value', "No synopsis available.")

        synopsis_label = tk.Label(details_frame, text=synopsis_text, font=('Arial', 9), wraplength=350, justify="left",
                                  bg="#F2F2F2")
        synopsis_label.pack(pady=(10, 10), padx=10)

    def add_to_cart(self, details_frame):

        self.cart_count += 1  # Increment cart count
        self.cart_count_label.config(text=str(self.cart_count))  # Update cart count display
        messagebox.showinfo("Rent Book", "Book added to cart for rental!")  # Show message

        # Buttons Frame (for Rent and Buy Now)
        buttons_frame = tk.Frame(details_frame, bg="#F2F2F2")
        buttons_frame.pack(pady=10)

        # Rent Button
        rent_button = tk.Button(buttons_frame, text="📖 Rent", font=("Arial", 10, "bold"),
                                bg="#E0E0E0", fg="black", padx=10, pady=5, width=10,
                                command=self.rent_action)
        rent_button.pack(side="left", padx=5)

        buy_button = tk.Button(buttons_frame, text="🛒 Buy Now", font=("Arial", 10, "bold"),
                               bg="#FFD700", fg="black", padx=10, pady=5, width=10,
                               command=self.buy_action)
        buy_button.pack(side="left", padx=5)


    def rent_action(self):
        messagebox.showinfo("Rent Book", "The book has been rented successfully!")

    def buy_action(self):
        messagebox.showinfo("Buy Book", "You have purchased the book successfully!")

root = tk.Tk()
app = Rental_System(root)
root.geometry("300x500+500+150")
root.resizable(0, 0)
# Run the application
root.mainloop()
