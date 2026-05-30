from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import sys

# ================= RESOURCE PATH ================= #

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ================= DATABASE CONNECTION ================= #

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ADITHYAN",
    database="railway_db"
)

cursor = con.cursor()

# ================= MAIN WINDOW ================= #

root = Tk()

root.title("Railway Ticket Booking System")

root.geometry("1400x750")

root.resizable(False, False)

# ================= BACKGROUND IMAGE ================= #

bg_image = Image.open(resource_path("train_bg.jpg"))

bg_image = bg_image.resize((1400, 750))

bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(root, image=bg_photo)

bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ================= TITLE ================= #

heading = Label(
    root,
    text="RAILWAY TICKET BOOKING SYSTEM",
    font=("Arial", 28, "bold"),
    bg="black",
    fg="cyan",
    padx=20,
    pady=10
)

heading.pack(pady=15)

# ================= MAIN FRAME ================= #

main_frame = Frame(
    root,
    bg="white",
    bd=5,
    relief=RIDGE
)

main_frame.place(x=40, y=100, width=550, height=620)

# ================= VARIABLES ================= #

name_var = StringVar()

train_var = StringVar()

seat_var = StringVar()

search_var = StringVar()

price_var = StringVar()

# ================= LABELS ================= #

Label(
    main_frame,
    text="Passenger Name",
    font=("Arial", 14, "bold"),
    bg="white"
).place(x=20, y=30)

Entry(
    main_frame,
    textvariable=name_var,
    font=("Arial", 14),
    width=25
).place(x=220, y=30)

Label(
    main_frame,
    text="Train Number",
    font=("Arial", 14, "bold"),
    bg="white"
).place(x=20, y=90)

Entry(
    main_frame,
    textvariable=train_var,
    font=("Arial", 14),
    width=25
).place(x=220, y=90)

Label(
    main_frame,
    text="Seats",
    font=("Arial", 14, "bold"),
    bg="white"
).place(x=20, y=150)

Entry(
    main_frame,
    textvariable=seat_var,
    font=("Arial", 14),
    width=25
).place(x=220, y=150)

Label(
    main_frame,
    text="Search Train",
    font=("Arial", 14, "bold"),
    bg="white"
).place(x=20, y=210)

Entry(
    main_frame,
    textvariable=search_var,
    font=("Arial", 14),
    width=25
).place(x=220, y=210)

# ================= CLEAR FIELDS ================= #

def clear_fields():

    name_var.set("")
    train_var.set("")
    seat_var.set("")
    search_var.set("")
    price_var.set("")

# ================= VIEW TRAINS ================= #

def view_trains():

    train_window = Toplevel(root)

    train_window.title("Available Trains")

    train_window.geometry("900x400")

    tree = ttk.Treeview(train_window)

    tree["columns"] = (
        "Train No",
        "Train Name",
        "Source",
        "Destination",
        "Seats",
        "Price"
    )

    tree.column("#0", width=0, stretch=NO)

    for col in tree["columns"]:

        tree.column(col, width=130, anchor=CENTER)

        tree.heading(col, text=col)

    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT * FROM trains")

    data = cursor.fetchall()

    for row in data:

        tree.insert("", END, values=row)

# ================= SEARCH TRAIN ================= #

def search_train():

    keyword = search_var.get()

    cursor.execute(
        "SELECT * FROM trains WHERE train_name LIKE %s",
        ('%' + keyword + '%',)
    )

    data = cursor.fetchall()

    if data:

        result = ""

        for row in data:

            result += f"Train No: {row[0]}\n"
            result += f"Train Name: {row[1]}\n"
            result += f"Route: {row[2]} ➜ {row[3]}\n"
            result += f"Seats Available: {row[4]}\n"
            result += f"Ticket Price: ₹{row[5]}\n"
            result += "--------------------------\n"

        messagebox.showinfo("Search Result", result)

    else:

        messagebox.showerror("Error", "Train Not Found")

# ================= CHECK SEATS ================= #

def check_seats():

    train_no = train_var.get()

    cursor.execute(
        "SELECT seats_available FROM trains WHERE train_no=%s",
        (train_no,)
    )

    result = cursor.fetchone()

    if result:

        messagebox.showinfo(
            "Seat Availability",
            f"Available Seats: {result[0]}"
        )

    else:

        messagebox.showerror("Error", "Train Not Found")

# ================= PRICE CALCULATOR ================= #

def calculate_price():

    train_no = train_var.get()

    seats = seat_var.get()

    if not seats.isdigit():

        messagebox.showerror("Error", "Enter Valid Seats")

        return

    cursor.execute(
        "SELECT ticket_price FROM trains WHERE train_no=%s",
        (train_no,)
    )

    result = cursor.fetchone()

    if result:

        total = int(seats) * result[0]

        price_var.set(f"Total Price : ₹{total}")

    else:

        messagebox.showerror("Error", "Train Not Found")

# ================= BOOK TICKET ================= #

def book_ticket():

    name = name_var.get()

    train_no = train_var.get()

    seats = seat_var.get()

    if name == "" or train_no == "" or seats == "":

        messagebox.showerror("Error", "All Fields Required")

        return

    if not seats.isdigit():

        messagebox.showerror("Error", "Seats Must Be Number")

        return

    seats = int(seats)

    cursor.execute(
        "SELECT seats_available, ticket_price FROM trains WHERE train_no=%s",
        (train_no,)
    )

    result = cursor.fetchone()

    if result:

        available = result[0]

        price = result[1]

        if seats > available:

            messagebox.showerror(
                "Error",
                "Not Enough Seats Available"
            )

            return

        total = seats * price

        cursor.execute(
            """
            INSERT INTO bookings
            (passenger_name, train_no, seats_booked, total_price)
            VALUES (%s, %s, %s, %s)
            """,
            (name, train_no, seats, total)
        )

        cursor.execute(
            """
            UPDATE trains
            SET seats_available = seats_available - %s
            WHERE train_no=%s
            """,
            (seats, train_no)
        )

        con.commit()

        booking_id = cursor.lastrowid

        messagebox.showinfo(
            "Success",
            f"Ticket Booked Successfully\n\n"
            f"Booking ID : {booking_id}\n"
            f"Total Price : ₹{total}"
        )

        clear_fields()

    else:

        messagebox.showerror("Error", "Train Not Found")

# ================= CANCEL TICKET ================= #

def cancel_ticket():

    cancel_window = Toplevel(root)

    cancel_window.title("Cancel Ticket")

    cancel_window.geometry("400x250")

    cancel_window.config(bg="white")

    Label(
        cancel_window,
        text="Enter Booking ID",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(pady=20)

    booking_entry = Entry(
        cancel_window,
        font=("Arial", 15)
    )

    booking_entry.pack(pady=10)

    def cancel_now():

        booking_id = booking_entry.get()

        cursor.execute(
            "SELECT train_no, seats_booked FROM bookings WHERE booking_id=%s",
            (booking_id,)
        )

        result = cursor.fetchone()

        if result:

            train_no = result[0]

            booked_seats = result[1]

            cursor.execute(
                """
                UPDATE trains
                SET seats_available = seats_available + %s
                WHERE train_no=%s
                """,
                (booked_seats, train_no)
            )

            cursor.execute(
                "DELETE FROM bookings WHERE booking_id=%s",
                (booking_id,)
            )

            con.commit()

            messagebox.showinfo(
                "Success",
                "Ticket Cancelled Successfully"
            )

            cancel_window.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Booking ID Not Found"
            )

    Button(
        cancel_window,
        text="Cancel Ticket",
        font=("Arial", 14, "bold"),
        bg="red",
        fg="white",
        command=cancel_now
    ).pack(pady=20)

# ================= VIEW BOOKINGS ================= #

def view_bookings():

    booking_window = Toplevel(root)

    booking_window.title("All Bookings")

    booking_window.geometry("850x400")

    tree = ttk.Treeview(booking_window)

    tree["columns"] = (
        "Booking ID",
        "Passenger Name",
        "Train No",
        "Seats",
        "Price"
    )

    tree.column("#0", width=0, stretch=NO)

    for col in tree["columns"]:

        tree.column(col, width=150, anchor=CENTER)

        tree.heading(col, text=col)

    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT * FROM bookings")

    data = cursor.fetchall()

    for row in data:

        tree.insert("", END, values=row)

# ================= BUTTONS ================= #

Button(
    main_frame,
    text="View Trains",
    font=("Arial", 14, "bold"),
    bg="#2196F3",
    fg="white",
    width=18,
    command=view_trains
).place(x=30, y=300)

Button(
    main_frame,
    text="Search Train",
    font=("Arial", 14, "bold"),
    bg="#009688",
    fg="white",
    width=18,
    command=search_train
).place(x=280, y=300)

Button(
    main_frame,
    text="Seat Availability",
    font=("Arial", 14, "bold"),
    bg="#673AB7",
    fg="white",
    width=18,
    command=check_seats
).place(x=30, y=370)

Button(
    main_frame,
    text="Price Calculator",
    font=("Arial", 14, "bold"),
    bg="#FF9800",
    fg="white",
    width=18,
    command=calculate_price
).place(x=280, y=370)

Button(
    main_frame,
    text="Book Ticket",
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    width=18,
    command=book_ticket
).place(x=30, y=440)

Button(
    main_frame,
    text="Cancel Ticket",
    font=("Arial", 14, "bold"),
    bg="#F44336",
    fg="white",
    width=18,
    command=cancel_ticket
).place(x=280, y=440)

Button(
    main_frame,
    text="View Bookings",
    font=("Arial", 14, "bold"),
    bg="#3F51B5",
    fg="white",
    width=40,
    command=view_bookings
).place(x=30, y=510)

Button(
    main_frame,
    text="Clear Fields",
    font=("Arial", 14, "bold"),
    bg="#607D8B",
    fg="white",
    width=40,
    command=clear_fields
).place(x=30, y=570)

# ================= PRICE LABEL ================= #

Label(
    root,
    textvariable=price_var,
    font=("Arial", 18, "bold"),
    bg="black",
    fg="yellow"
).place(x=850, y=220)

# ================= SIDE TEXT ================= #

welcome = Label(
    root,
    text="WELCOME TO INDIAN RAILWAYS",
    font=("Arial", 24, "bold"),
    bg="black",
    fg="white"
)

welcome.place(x=760, y=120)

# ================= FOOTER ================= #

footer = Label(
    root,
    text="Developed Using Python + Tkinter + MySQL",
    font=("Arial", 12, "bold"),
    bg="black",
    fg="white"
)

footer.pack(side=BOTTOM, fill=X)

# ================= MAIN LOOP ================= #

root.mainloop()