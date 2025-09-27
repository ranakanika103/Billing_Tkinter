import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3, datetime
from tkinter.font import Font

DB = "supermarket_bills.db"


# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS bills (
                        bill_no INTEGER PRIMARY KEY,
                        name TEXT,
                        contact TEXT,
                        details TEXT,
                        total REAL,
                        date TEXT
                    )""")
    conn.commit()
    conn.close()
init_db()

# ---------- PRODUCT DATA ----------
products = {
    "Drinks": {
        "Coca Cola": 40,
        "Pepsi": 35,
        "Fanta": 30,
        "Maza": 20,
        "Limca":30,
        "Dew":40
    },
    "Fruits": {
        "Apple": 100,
        "Banana": 60,
        "Mango": 120,
        "Grapes":80,
        "Orange":70,
        "Litchi":90,
        "Watermelon":50
    },
    "Snacks": {
        "Chips": 20,
        "Biscuits": 50,
        "Namkeen": 70,
        "Kit-Kat":20,
        "Diary Milk":40,
        "Kurkure":10,
        "Takatak":20

    },
    "Dry Fruits": {
        "Almonds":179,
        "Cashews":230,
        "Raisins":198,
        "Walnuts":472,
        "Dates":340,
        "Figs":140
    },
    "Vegetables": {
        "Tomatoes":80,
        "Carrots":60,
        "Broccoli":70,
        "Potatoes": 70,
        "Onion":100,
        "Beans":60
    }
}

# ---------- MAIN APP ----------
class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Billing System")
        self.root.geometry("950x600")
        self.root.config(bg="#f0b6d9")

        self.cart = []
        self.total_amount = 0
        self.bill_no = tk.IntVar(value=self.new_bill_no())

        # -------- HEADER --------
        tk.Label(root, text="SUPERMARKET BILLING SYSTEM",
                 font=("Times New Roman", 20, "bold"),
                 bg="#E6F7FF", fg="black").pack(pady=10)

        # -------- CUSTOMER DETAILS --------
        frame_top = tk.Frame(root, bg="#f0b6d9")
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Name:", bg="#f0b6d9").grid(row=0, column=0, padx=10)
        self.entry_name = tk.Entry(frame_top)
        self.entry_name.grid(row=0, column=1, padx=10)

        tk.Label(frame_top, text="Contact:", bg="#f0b6d9").grid(row=0, column=2, padx=10)
        self.entry_contact = tk.Entry(frame_top)
        self.entry_contact.grid(row=0, column=3, padx=10)

        # -------- PRODUCT SELECTION --------
        frame_mid = tk.Frame(root, bg="#f0b6d9")
        frame_mid.pack(pady=15)

        tk.Label(frame_mid, text="Category", bg="#f0b6d9").grid(row=0, column=0, padx=10)
        self.category = ttk.Combobox(frame_mid, values=list(products.keys()), state="readonly", width=15)
        self.category.grid(row=0, column=1, padx=10)
        self.category.bind("<<ComboboxSelected>>", self.update_subcategories)

        tk.Label(frame_mid, text="Subcategory", bg="#f0b6d9").grid(row=0, column=2, padx=10)
        self.subcategory = ttk.Combobox(frame_mid, state="readonly", width=15)
        self.subcategory.grid(row=0, column=3, padx=10)
        self.subcategory.bind("<<ComboboxSelected>>", self.show_price)

        tk.Label(frame_mid, text="Price", bg="#f0b6d9").grid(row=0, column=4, padx=10)
        self.price_var = tk.StringVar()
        self.entry_price = tk.Entry(frame_mid, textvariable=self.price_var, state="readonly", width=10)
        self.entry_price.grid(row=0, column=5, padx=10)

        tk.Label(frame_mid, text="Quantity", bg="#f0b6d9").grid(row=0, column=6, padx=10)
        self.entry_qty = tk.Entry(frame_mid, width=10)
        self.entry_qty.grid(row=0, column=7, padx=10)

        tk.Button(frame_mid, text="Add Item", command=self.add_item, bg="#90be6d").grid(row=0, column=8, padx=15)

        # -------- BILL AREA --------
        frame_bill = tk.Frame(root, bg="black", bd=2, relief="ridge")
        frame_bill.place(x=200, y=150, width=480, height=380)

        self.txt_bill = tk.Text(frame_bill, font=("Courier", 10),bg="#E6F7FF")
        self.txt_bill.pack(fill="both", expand=1)

        # -------- ACTION BUTTONS --------
        frame_btn = tk.Frame(root, bg="#f0b6d9")
        frame_btn.pack(side="bottom", pady=10)

        tk.Button(frame_btn, text="Generate Bill", command=self.generate_bill, bg="#90be6d").pack(side="left", padx=10)
        tk.Button(frame_btn, text="Save Bill", command=self.save_bill, bg="#f9c74f").pack(side="left", padx=10)
        tk.Button(frame_btn, text="Search Bill", command=self.search_bill, bg="#f9844a").pack(side="left", padx=10)
        tk.Button(frame_btn, text="Exit", command=self.root.quit, bg="#e63946").pack(side="left", padx=10)

    # -------- Update subcategories --------
    def update_subcategories(self, event=None):
        category = self.category.get()
        if category in products:
            self.subcategory["values"] = list(products[category].keys())
            self.subcategory.set("")
            self.price_var.set("")

    # -------- Show price when subcategory selected --------
    def show_price(self, event=None):
        category = self.category.get()
        sub = self.subcategory.get()
        if sub in products.get(category, {}):
            self.price_var.set(products[category][sub])

    # -------- Add item to cart --------
    def add_item(self):
        category = self.category.get()
        product = self.subcategory.get()
        if not product:
            messagebox.showerror("Error", "Please select a product")
            return
        try:
            qty = int(self.entry_qty.get())
        except:
            messagebox.showerror("Error", "Enter valid quantity")
            return
        price = products[category][product]
        self.cart.append([product, price, qty])
        messagebox.showinfo("Added", f"{product} x{qty} added to cart")
        self.entry_qty.delete(0, tk.END)

    # -------- Generate Bill --------
    def generate_bill(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty!")
            return

        self.txt_bill.delete(1.0, tk.END)
        self.txt_bill.insert(tk.END, "         SUPERMARKET BILLING SYSTEM\n\n")
        self.txt_bill.insert(tk.END, f"Bill No: {self.bill_no.get()}\n")
        self.txt_bill.insert(tk.END, f"Customer: {self.entry_name.get()} | Phone: {self.entry_contact.get()}\n")
        self.txt_bill.insert(tk.END, "-"*40 + "\n")
        self.txt_bill.insert(tk.END, f"{'Product':15}{'Price':7}{'Qty':5}{'Amount':10}\n")
        self.txt_bill.insert(tk.END, "-"*40 + "\n")

        total = 0
        for product, price, qty in self.cart:
            cost = price * qty
            self.txt_bill.insert(tk.END, f"{product:15}{price:<7}{qty:<5}{cost:<10}\n")
            total += cost

        tax = round(total*0.05, 2)
        grand_total = total + tax

        self.txt_bill.insert(tk.END, "-"*40 + "\n\n")
        self.txt_bill.insert(tk.END, f"Sub Amount: Rs.{total}\nTax (5%): Rs.{tax}\nTotal: Rs.{grand_total}\n")
        self.total_amount = grand_total

    # -------- Save Bill --------
    def save_bill(self):
        if not hasattr(self, "total_amount"):
            messagebox.showerror("Error", "Generate bill first!")
            return
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO bills VALUES (?,?,?,?,?,?)",
                    (self.bill_no.get(),
                     self.entry_name.get(),
                     self.entry_contact.get(),
                     str(self.cart),
                     self.total_amount,
                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", f"Bill {self.bill_no.get()} saved!")
        self.bill_no.set(self.new_bill_no())
        self.cart.clear()

    # -------- Search Bill --------
    def search_bill(self):
        bill_no = simpledialog.askinteger("Search", "Enter Bill Number:")
        if not bill_no:
            return
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT * FROM bills WHERE bill_no=?", (bill_no,))
        res = cur.fetchone()
        conn.close()

        if res:
            self.txt_bill.delete(1.0, tk.END)
            self.txt_bill.insert(tk.END, f"Bill No: {res[0]}\nName: {res[1]}\nContact: {res[2]}\n")
            self.txt_bill.insert(tk.END, f"Items: {res[3]}\nTotal: Rs.{res[4]}\nDate: {res[5]}\n")
        else:
            messagebox.showerror("Error", "Bill not found!")

    # -------- Generate new Bill Number --------
    def new_bill_no(self):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT MAX(bill_no) FROM bills")
        res = cur.fetchone()[0]
        conn.close()
        return (res or 1000) + 1


# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()