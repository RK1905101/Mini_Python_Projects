import tkinter as tk

def exit():
    window.destroy()


def convert():
    c = e1.get()
    d = c.split(".")
    count = 3
    sum = 0
    for i in d:
        sum = sum + int(i)*(256**count)
        count = count - 1
    # print(sum)
    t1.config(state='normal')
    t1.delete('1.0', tk.END)
    t1.insert(tk.END, sum)
    t1.config(state='disabled')

window = tk.Tk()
window.geometry("300x250")
window.config(bg="#000000")
# window.resizable(width=False, height=False)
window.title('IPv4 to Decimal!')

l1 = tk.Label(window, text="IPv4 to decimal IP", font=("Arial", 15), fg="#00FF08", bg="black")
l2 = tk.Label(window, text="Enter IPv4: ", font=("Arial", 10, "bold"), fg="black", bg="#00FF08")
l3 = tk.Label(window, text="Decimal IP: ", font=("Arial", 10, "bold"), fg="black", bg="#00FF08")

# empty_l1 = tk.Label(window, bg="#A569BD")
# empty_l2 = tk.Label(window, bg="#A569BD")

e1 = tk.Entry(window, font=('Arial', 15))

btn1 = tk.Button(window, text="Convert!!!", font=("Arial", 10), command=convert)
btn2 = tk.Button(window, text="Exit application", font=("Arial", 10), command=exit)

t1 = tk.Text(window, state="disabled", width=15, height=0, font=("Arial",15))

l1.pack()
l2.pack()
e1.pack()
# empty_l1.pack()
btn1.pack()
l3.pack()
t1.pack()
# empty_l2.pack()
btn2.pack()

window.mainloop()
