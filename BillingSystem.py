import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
import os
import subprocess

# Constants
TVA_RATE = 0.2  # Example TVA rate (20%)
ADDITIONAL_FEES = 5.0  # Flat additional fees (change as needed)

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")

        # Store items and prices
        self.items = [("Item 1", 10.0), ("Item 2", 20.0), ("Item 3", 15.0)]
        self.order = []

        # Interface elements
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Items:").pack()

        # Add items with checkboxes
        for item, price in self.items:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(self.root, text=f"{item} - ${price}", variable=var)
            checkbox.pack()
            self.order.append((item, price, var))

        # Calculate and print buttons
        tk.Button(self.root, text="Calculate Total", command=self.calculate_total).pack(pady=5)
        tk.Button(self.root, text="Download and Print Ticket", command=self.download_and_print_ticket).pack(pady=5)
        
        # Display result
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def calculate_total(self):
        subtotal = sum(price for item, price, var in self.order if var.get())
        tva = subtotal * TVA_RATE
        total = subtotal + tva + ADDITIONAL_FEES

        # Display the result
        self.result_label.config(text=f"Subtotal: ${subtotal:.2f}, TVA: ${tva:.2f}, Total: ${total:.2f}")
        self.subtotal, self.tva, self.total = subtotal, tva, total

    def download_and_print_ticket(self):
        # Prompt the user to select a location to save the ticket
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if save_path:
            # Generate a PDF ticket
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)

            # Ticket details
            pdf.cell(0, 10, "Billing Ticket", ln=True, align="C")
            pdf.cell(0, 10, "-"*30, ln=True, align="C")

            for item, price, var in self.order:
                if var.get():
                    pdf.cell(0, 10, f"{item}: ${price:.2f}", ln=True)

            pdf.cell(0, 10, f"Subtotal: ${self.subtotal:.2f}", ln=True)
            pdf.cell(0, 10, f"TVA ({TVA_RATE*100}%): ${self.tva:.2f}", ln=True)
            pdf.cell(0, 10, f"Additional Fees: ${ADDITIONAL_FEES:.2f}", ln=True)
            pdf.cell(0, 10, f"Total: ${self.total:.2f}", ln=True)

            # Save the ticket to the selected path
            pdf.output(save_path)
            self.result_label.config(text=f"Ticket saved as {save_path}")

            # Print the file using subprocess for cross-platform compatibility
            try:
                if os.name == 'nt':  # Windows
                    subprocess.run(['print', save_path], check=True, shell=True)
                else:  # Linux / macOS
                    subprocess.run(['lp', save_path], check=True)
                
                self.result_label.config(text=f"Ticket printed and saved at {save_path}")
            except Exception as e:
                self.result_label.config(text=f"Error printing ticket: {e}")

# Run the application
root = tk.Tk()
app = BillingSystem(root)
root.mainloop()
