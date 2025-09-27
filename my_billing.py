# importing a libraries
import tkinter as Tk


def generate_bill():
    # blank text to print bill
    bill_text=""
    # total bill
    total=0

    # loop to go through all items
    for i in LABELS:

        # getting quantity of each item
        a = LABELS[i][2].get() 

        # creating a place holder - if a =0 or none or error
        qty = None

        # checking if quantity is a number
        if str(a).strip().isdigit():

            # if quantity is a number, then assinging it to qty
            qty = int(str(LABELS[i][2].get()).strip())

        # if quantity is error or blank
        qty = qty or 0

        # generating total bill
        total += LABELS[i][1] * qty

        # adding all the item, their names, price, quantity and total
        bill_text += f'\n {i}  :  {LABELS[i][1]} x {qty} = {LABELS[i][1] * qty}\n '
        
    # grand total    
    bill_text += f"\n Total bill is ₹{total} "
    print(bill_text)


WINDOW_SIZE_X = 600
WINDOW_SIZE_Y = 300
center = WINDOW_SIZE_X//2

#creating a window
root =Tk.Tk()


#######################################
############# root functions ##########
#######################################


# resizing window
root.geometry(f"{WINDOW_SIZE_X}x{WINDOW_SIZE_Y}")

# changing title
root.title("Billing System")


# no resize
#print(help(root.resizable))
root.resizable(True,False) # (width,height)


#######################################
############# widgits(label) functions ##########
#######################################


################ TITLE ##################

SOFTWARE_TITLE = "BILLING SYSTEM"
myTitle = Tk.Label(text=SOFTWARE_TITLE ,font = ("arial", 12))
myTitle.place(x= center-(len(SOFTWARE_TITLE)*6//2), y=20)

#L_NAME = Tk.Label(root,text="ITEMS NAME",fg="pink",bg = "black" , font =("Times New Roman",14))
#L_NAME.place(x=15 ,y=50)

#L_PRICE = Tk.Label(root,text="PRICE")
#L_PRICE.place(x=150 ,y=50)

#L_QUANTITY = Tk.Label(root,text="QUANTITY")
#L_QUANTITY.place(x=250 ,y=50)

LABELS ={}

items = {"Namkeen" : 50, "SoftDrink": 40, "chips": 20}

for i in items:
    LABELS[i] = [Tk.Label(text = f"{i}", font=("arial", 12, "bold")), items[i], Tk.Entry()]




B_Total =Tk.Button(text="Calculate Bill", font=("arial", 12), command=generate_bill)
B_Total.place(x=250, y=250)



Label_position_x= 12
Label_position_y= 100
increment=0


for i in LABELS:
# print(LABELS[i])
# LABELS have Label object at index 0
# LABELS have price at index 1
# LABELS have entry(quantity) at index 2

   # placing the labels at position according to x and y axies
    LABELS[i][0].place(x=Label_position_x, y= Label_position_y + increment)
   
   # placing the price at position according to x and y
    Tk.Label(text=f"₹{LABELS[i][1]}", font=("arial",10)).place(x=Label_position_x + 150 , y= Label_position_y + increment)
   
   # placing the entry at position according to x and y
    LABELS[i][2].place(x=Label_position_x +250 , y= Label_position_y + increment)
   
   # placing every item after 40 pixels below the precdeing
    increment +=40

# running the window
root.mainloop()



