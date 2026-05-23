import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import datetime
import os
import sys
import subprocess
from fpdf import FPDF

DATA_FILE = "patients_data.csv"
COLUMNS = [
    "Registration Date", "Name", "Age", "Gender", "Contact",
    "Disease", "Payment Amount", "Payment Status",
    "Insurance Company", "Policy Number", "Mediclaim Details", "Attached Document"
]

def safe_str(val):
    if pd.isna(val):
        return ""
    s = str(val).strip()
    # Pandas occasionally parses empty CSV cells as the literal string "nan"
    return "" if s.lower() == 'nan' else s

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            # Ensure all expected columns exist in case the CSV was altered
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""
            return df
    except Exception as e:
        print(f"Warning: Could not load data cleanly. Error: {e}")
    return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    try:
        df.to_csv(DATA_FILE, index=False)
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save data. Ensure the file '{DATA_FILE}' is not open in another program.\nError: {e}")

def generate_patient_pdf(patient_data, filepath):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Patient Registration Record", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    for key, value in patient_data.items():
        val = safe_str(value)
        safe_val = val.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, f"{key}: {safe_val}")
    pdf.output(filepath)

def generate_table_pdf(df, filepath):
    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Patient Database Export", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 8)
    cols_to_print = ["Registration Date", "Name", "Disease", "Payment Status", "Insurance Company"]
    
    for col in cols_to_print:
        pdf.cell(55, 10, str(col), border=1)
    pdf.ln()
    
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        for col in cols_to_print:
            val = safe_str(row.get(col)).replace('\n', ' ')[:30]
            safe_val = val.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(55, 10, safe_val, border=1)
        pdf.ln()
        
    pdf.output(filepath)

def generate_excel(df, filepath):
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Patients')

class PatientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("👁️ Aditya Eye Clinic Patient Register")
        self.geometry("1200x800")
        
        # Define color palette
        self.BLUE = "#004b87"
        self.YELLOW = "#FFD700"
        self.WHITE = "#FFFFFF"
        
        self.configure(bg=self.WHITE)
        
        self.df = load_data()
        self.filtered_df = pd.DataFrame(columns=COLUMNS)
        
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern 2025 UI fonts
        FONT_MAIN = ("Segoe UI", 11)
        FONT_HEAD = ("Segoe UI", 22, "bold")
        FONT_SUB = ("Segoe UI", 12, "bold")
        
        style.configure("TFrame", background=self.WHITE)
        style.configure("TLabel", background=self.WHITE, foreground=self.BLUE, font=FONT_MAIN)
        style.configure("Header.TLabel", font=FONT_HEAD, foreground=self.BLUE, background=self.WHITE, padding=(0, 10))
        
        style.configure("TLabelframe", background=self.WHITE, bordercolor=self.BLUE, borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background=self.WHITE, foreground=self.BLUE, font=FONT_SUB)
        
        style.configure("TButton", background=self.YELLOW, foreground=self.BLUE, font=FONT_SUB, padding=(20, 10), borderwidth=0)
        style.map("TButton", background=[('active', self.BLUE)], foreground=[('active', self.WHITE)])
        
        style.configure("TEntry", fieldbackground=self.WHITE, foreground=self.BLUE, font=FONT_MAIN, padding=10, borderwidth=1, bordercolor=self.BLUE, lightcolor=self.BLUE, darkcolor=self.BLUE)
        style.configure("TCombobox", fieldbackground=self.WHITE, foreground=self.BLUE, font=FONT_MAIN, padding=10, borderwidth=1, bordercolor=self.BLUE, lightcolor=self.BLUE, darkcolor=self.BLUE)
        
        style.configure("TNotebook", background=self.WHITE, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.BLUE, foreground=self.WHITE, padding=[25, 12], font=FONT_SUB, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", self.YELLOW)], foreground=[("selected", self.BLUE)])
        
        style.configure("Treeview", background=self.WHITE, foreground=self.BLUE, rowheight=40, fieldbackground=self.WHITE, font=FONT_MAIN, borderwidth=0)
        style.configure("Treeview.Heading", background=self.BLUE, foreground=self.WHITE, font=FONT_SUB, borderwidth=0, padding=10)
        style.map("Treeview", background=[("selected", self.YELLOW)], foreground=[("selected", self.BLUE)])
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_reg = ttk.Frame(self.notebook)
        self.tab_db = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_reg, text="Registration Form")
        self.notebook.add(self.tab_db, text="Patient Database")
        
        self.build_registration_tab()
        self.build_database_tab()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.refresh_database_view()

    def build_registration_tab(self):
        f = ttk.Frame(self.tab_reg, padding=20)
        f.pack(fill='both', expand=True)
        
        ttk.Label(f, text="New Patient Registration", style="Header.TLabel").grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        self.v_name = tk.StringVar()
        self.v_age = tk.StringVar(value="0")
        self.v_gender = tk.StringVar()
        self.v_contact = tk.StringVar()
        self.v_pay_amt = tk.StringVar(value="0.0")
        self.v_pay_stat = tk.StringVar()
        self.v_ins_comp = tk.StringVar()
        self.v_pol_num = tk.StringVar()
        
        ttk.Label(f, text="Patient Name:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=self.v_name).grid(row=1, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Age:").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=self.v_age).grid(row=2, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Gender:").grid(row=3, column=0, sticky='w', pady=5)
        cb_gender = ttk.Combobox(f, textvariable=self.v_gender, values=["Male", "Female", "Other"], state="readonly")
        cb_gender.grid(row=3, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Contact Number:").grid(row=4, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=self.v_contact).grid(row=4, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Disease/Diagnosis:").grid(row=5, column=0, sticky='nw', pady=5)
        self.t_disease = tk.Text(f, height=4, width=30, bg=self.WHITE, fg=self.BLUE, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground=self.BLUE, highlightcolor=self.YELLOW)
        self.t_disease.grid(row=5, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(f, text="Payment Amount:").grid(row=1, column=2, sticky='w', padx=(20, 0), pady=5)
        ttk.Entry(f, textvariable=self.v_pay_amt).grid(row=1, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Payment Status:").grid(row=2, column=2, sticky='w', padx=(20, 0), pady=5)
        cb_pay = ttk.Combobox(f, textvariable=self.v_pay_stat, values=["Pending", "Paid", "Partially Paid"], state="readonly")
        cb_pay.grid(row=2, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Insurance Company:").grid(row=3, column=2, sticky='w', padx=(20, 0), pady=5)
        ttk.Entry(f, textvariable=self.v_ins_comp).grid(row=3, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Policy Number:").grid(row=4, column=2, sticky='w', padx=(20, 0), pady=5)
        ttk.Entry(f, textvariable=self.v_pol_num).grid(row=4, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Mediclaim Details:").grid(row=5, column=2, sticky='nw', padx=(20, 0), pady=5)
        self.t_mediclaim = tk.Text(f, height=4, width=30, bg=self.WHITE, fg=self.BLUE, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground=self.BLUE, highlightcolor=self.YELLOW)
        self.t_mediclaim.grid(row=5, column=3, sticky='ew', padx=5, pady=5)
        
        self.v_doc_path = tk.StringVar()
        ttk.Label(f, text="Attached Document:").grid(row=6, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=self.v_doc_path, state='readonly').grid(row=6, column=1, sticky='ew', padx=5)
        ttk.Button(f, text="Browse...", command=self.browse_document).grid(row=6, column=2, sticky='w', padx=(20, 0))
        
        ttk.Button(f, text="Register Patient", command=self.register_patient).grid(row=7, column=0, columnspan=2, pady=30, sticky='e', padx=10)
        ttk.Button(f, text="Clear Form", command=self.clear_registration_form).grid(row=7, column=2, columnspan=2, pady=30, sticky='w', padx=10)
        
        f.columnconfigure(1, weight=1)
        f.columnconfigure(3, weight=1)
        for i in range(8):
            f.rowconfigure(i, weight=1)

    def browse_document(self):
        filepath = filedialog.askopenfilename(title="Select Document")
        if filepath:
            self.v_doc_path.set(filepath)
            
    def clear_registration_form(self):
        self.v_name.set("")
        self.v_age.set("0")
        self.v_gender.set("")
        self.v_contact.set("")
        self.t_disease.delete("1.0", tk.END)
        self.v_pay_amt.set("0.0")
        self.v_pay_stat.set("")
        self.v_ins_comp.set("")
        self.v_pol_num.set("")
        self.t_mediclaim.delete("1.0", tk.END)
        self.v_doc_path.set("")

    def register_patient(self):
        name = self.v_name.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Patient Name is required.")
            return
            
        try:
            age_val = int(float(self.v_age.get().strip() or 0))
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid whole number.")
            return
            
        try:
            pay_amt_val = float(self.v_pay_amt.get().strip() or 0.0)
        except ValueError:
            messagebox.showerror("Validation Error", "Payment Amount must be a valid number.")
            return
            
        new_data = {
            "Registration Date": datetime.date.today().strftime("%Y-%m-%d"),
            "Name": name,
            "Age": age_val,
            "Gender": self.v_gender.get(),
            "Contact": self.v_contact.get(),
            "Disease": self.t_disease.get("1.0", tk.END).strip(),
            "Payment Amount": pay_amt_val,
            "Payment Status": self.v_pay_stat.get(),
            "Insurance Company": self.v_ins_comp.get(),
            "Policy Number": self.v_pol_num.get(),
            "Mediclaim Details": self.t_mediclaim.get("1.0", tk.END).strip(),
            "Attached Document": self.v_doc_path.get()
        }
        
        new_df = pd.DataFrame([new_data], columns=COLUMNS)
        if self.df.empty:
            self.df = new_df
        else:
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            
        save_data(self.df)
        messagebox.showinfo("Success", f"Patient {name} registered successfully!")
        
        self.clear_registration_form()

    def build_database_tab(self):
        f = ttk.Frame(self.tab_db, padding=10)
        f.pack(fill='both', expand=True)
        
        filter_frame = ttk.LabelFrame(f, text="Filter Data", padding=10)
        filter_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(filter_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.v_f_date = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.v_f_date, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Week:").grid(row=0, column=2, padx=5, pady=5)
        self.cb_f_week = ttk.Combobox(filter_frame, width=10, state="readonly")
        self.cb_f_week.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Month:").grid(row=0, column=4, padx=5, pady=5)
        self.cb_f_month = ttk.Combobox(filter_frame, width=10, state="readonly")
        self.cb_f_month.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Year:").grid(row=0, column=6, padx=5, pady=5)
        self.cb_f_year = ttk.Combobox(filter_frame, width=10, state="readonly")
        self.cb_f_year.grid(row=0, column=7, padx=5, pady=5)
        
        ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters).grid(row=0, column=8, padx=15, pady=5)
        ttk.Button(filter_frame, text="Clear", command=self.clear_filters).grid(row=0, column=9, padx=5, pady=5)
        
        columns = ("Date", "Name", "Disease", "Pay Status", "Insurance")
        self.tree = ttk.Treeview(f, columns=columns, show='headings', height=10)
        
        self.tree.heading("Date", text="Registration Date")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Disease", text="Disease")
        self.tree.heading("Pay Status", text="Payment Status")
        self.tree.heading("Insurance", text="Insurance")
        
        self.tree.column("Date", width=100)
        self.tree.column("Name", width=150)
        self.tree.column("Disease", width=200)
        self.tree.column("Pay Status", width=100)
        self.tree.column("Insurance", width=150)
        
        tree_scroll = ttk.Scrollbar(f, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(fill='both', expand=True, side='top')
        tree_scroll.pack(side='right', fill='y')
        
        export_frame = ttk.LabelFrame(f, text="Export & Downloads", padding=10)
        export_frame.pack(fill='x', pady=10)
        
        ttk.Button(export_frame, text="Download Filtered Table as Excel", command=self.download_excel).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(export_frame, text="Download Filtered Table as PDF", command=self.download_table_pdf).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(export_frame, text="Delete All Data", command=self.delete_all).grid(row=0, column=2, padx=(50, 5), pady=5)
        
        ttk.Label(export_frame, text="Download Individual Patient Record:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.cb_patients = ttk.Combobox(export_frame, state="readonly", width=25)
        self.cb_patients.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        ttk.Button(export_frame, text="Download Patient PDF", command=self.download_patient_pdf).grid(row=1, column=2, padx=5, pady=5)

        self.context_menu = tk.Menu(self, tearoff=0, bg=self.WHITE, fg=self.BLUE, font=("Segoe UI", 11))
        self.context_menu.add_command(label="Edit Patient", command=self.edit_selected)
        self.context_menu.add_command(label="Delete Patient", command=self.delete_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="View Attached Document", command=self.view_document)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        if sys.platform == "darwin":
            self.tree.bind("<Button-2>", self.show_context_menu)  # Support for MacOS right-click

    def on_tab_change(self, event):
        try:
            selected_tab = event.widget.select()
            tab_text = event.widget.tab(selected_tab, "text")
            if tab_text == "Patient Database":
                self.refresh_database_view()
        except tk.TclError:
            pass

    def show_context_menu(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def refresh_database_view(self):
        if not self.df.empty:
            df_dates = pd.to_datetime(self.df['Registration Date'], errors='coerce')
            
            weeks = sorted([int(x) for x in df_dates.dt.isocalendar().week.dropna().unique() if pd.notna(x)])
            months = sorted([int(x) for x in df_dates.dt.month.dropna().unique() if pd.notna(x)])
            years = sorted([int(x) for x in df_dates.dt.year.dropna().unique() if pd.notna(x)])
            
            self.cb_f_week['values'] = ["All"] + list(weeks)
            self.cb_f_month['values'] = ["All"] + list(months)
            self.cb_f_year['values'] = ["All"] + list(years)
            
            if not self.cb_f_week.get(): self.cb_f_week.set("All")
            if not self.cb_f_month.get(): self.cb_f_month.set("All")
            if not self.cb_f_year.get(): self.cb_f_year.set("All")
            
        else:
            self.cb_f_week['values'] = ["All"]
            self.cb_f_month['values'] = ["All"]
            self.cb_f_year['values'] = ["All"]
            self.cb_f_week.set("All")
            self.cb_f_month.set("All")
            self.cb_f_year.set("All")
            
        self.apply_filters()

    def clear_filters(self):
        self.v_search.set("")
        self.v_f_date.set("")
        self.cb_f_week.set("All")
        self.cb_f_month.set("All")
        self.cb_f_year.set("All")
        self.apply_filters()

    def apply_filters(self):
        self.filtered_df = self.df.copy()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        patient_list = []
        
        if not self.filtered_df.empty:
            self.filtered_df['TempDate'] = pd.to_datetime(self.filtered_df['Registration Date'], errors='coerce')
            
            f_date = self.v_f_date.get().strip()
            f_week = self.cb_f_week.get()
            f_month = self.cb_f_month.get()
            f_year = self.cb_f_year.get()
            
            if f_date:
                try:
                    target_date = pd.to_datetime(f_date).strftime('%Y-%m-%d')
                    mask = self.filtered_df['TempDate'].dt.strftime('%Y-%m-%d') == target_date
                    self.filtered_df = self.filtered_df[mask.fillna(False).astype(bool)]
                except Exception:
                    pass  # Ignore incomplete/invalid date inputs while user is typing
            if f_week and f_week != "All":
                mask = self.filtered_df['TempDate'].dt.isocalendar().week == int(float(f_week))
                self.filtered_df = self.filtered_df[mask.fillna(False).astype(bool)]
            if f_month and f_month != "All":
                mask = self.filtered_df['TempDate'].dt.month == int(float(f_month))
                self.filtered_df = self.filtered_df[mask.fillna(False).astype(bool)]
            if f_year and f_year != "All":
                mask = self.filtered_df['TempDate'].dt.year == int(float(f_year))
                self.filtered_df = self.filtered_df[mask.fillna(False).astype(bool)]
                
            self.filtered_df = self.filtered_df.drop(columns=['TempDate'])
            
            # --- SMART SEARCH FILTER LOGIC ---
            search_term = self.v_search.get().strip().lower()
            if search_term:
                mask = self.filtered_df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)
                self.filtered_df = self.filtered_df[mask]
                
            # --- LIVE KPI DASHBOARD LOGIC ---
            total_pts = len(self.filtered_df)
            total_rev = pd.to_numeric(self.filtered_df['Payment Amount'], errors='coerce').fillna(0).sum()
            pending_pts = len(self.filtered_df[self.filtered_df['Payment Status'].astype(str).str.lower() == 'pending'])
            self.v_kpi_patients.set(f"{total_pts:,}")
            self.v_kpi_revenue.set(f"₹ {total_rev:,.2f}")
            self.v_kpi_pending.set(f"{pending_pts:,}")
            
            patient_list = [str(name) for name in self.filtered_df['Name'].tolist() if pd.notna(name)]
            self.cb_patients['values'] = patient_list
            if patient_list:
                self.cb_patients.set(patient_list[0])
            else:
                self.cb_patients.set("")
                
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for index, row in self.filtered_df.iterrows():
            self.tree.insert("", tk.END, iid=str(index), values=(
                "" if pd.isna(row.get("Registration Date")) else str(row.get("Registration Date")),
                "" if pd.isna(row.get("Name")) else str(row.get("Name")),
                "" if pd.isna(row.get("Disease")) else str(row.get("Disease"))[:30],
                "" if pd.isna(row.get("Payment Status")) else str(row.get("Payment Status")),
                "" if pd.isna(row.get("Insurance Company")) else str(row.get("Insurance Company"))
            ))

    def get_selected_index(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient from the list first.")
            return None
        try:
            return int(selected[0])
        except (ValueError, TypeError):
            return None

    def delete_selected(self):
        index = self.get_selected_index()
        if index is not None:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient's record?"):
                self.df = self.df.drop(index).reset_index(drop=True)
                save_data(self.df)
                self.refresh_database_view()
                messagebox.showinfo("Success", "Record deleted successfully.")

    def delete_all(self):
        if messagebox.askyesno("Confirm Delete All", "Are you sure you want to delete ALL patient records? This action cannot be undone."):
            self.df = pd.DataFrame(columns=COLUMNS)
            save_data(self.df)
            self.refresh_database_view()
            messagebox.showinfo("Success", "All records have been cleared.")

    def view_document(self):
        index = self.get_selected_index()
        if index is not None:
            doc_path = safe_str(self.df.at[index, 'Attached Document'])
            if not doc_path or not os.path.exists(doc_path):
                messagebox.showinfo("Not Found", "No valid document attached or file no longer exists.")
            else:
                try:
                    if sys.platform == "win32":
                        os.startfile(doc_path)
                    elif sys.platform == "darwin":
                        subprocess.call(["open", doc_path])
                    else:
                        subprocess.call(["xdg-open", doc_path])
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open document: {e}")
                    
    def edit_selected(self):
        index = self.get_selected_index()
        if index is None: return
        if index not in self.df.index: return
        
        row = self.df.loc[index]
        
        edit_win = tk.Toplevel(self)
        edit_win.title(f"Edit Patient - {row.get('Name', '')}")
        edit_win.geometry("900x500")
        edit_win.configure(bg=self.WHITE)
        
        f = ttk.Frame(edit_win, padding=20)
        f.pack(fill='both', expand=True)
        
        v_name = tk.StringVar(value=safe_str(row.get('Name')))
        v_age = tk.StringVar(value=safe_str(row.get('Age')) or "0")
        v_gender = tk.StringVar(value=safe_str(row.get('Gender')))
        v_contact = tk.StringVar(value=safe_str(row.get('Contact')))
        v_pay_amt = tk.StringVar(value=safe_str(row.get('Payment Amount')) or "0.0")
        v_pay_stat = tk.StringVar(value=safe_str(row.get('Payment Status')))
        v_ins_comp = tk.StringVar(value=safe_str(row.get('Insurance Company')))
        v_pol_num = tk.StringVar(value=safe_str(row.get('Policy Number')))
        v_doc_path = tk.StringVar(value=safe_str(row.get('Attached Document')))
        
        ttk.Label(f, text="Patient Name:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=v_name).grid(row=0, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Age:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=v_age).grid(row=1, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Gender:").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Combobox(f, textvariable=v_gender, values=["Male", "Female", "Other"], state="readonly").grid(row=2, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Contact Number:").grid(row=3, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=v_contact).grid(row=3, column=1, sticky='ew', padx=5)
        
        ttk.Label(f, text="Disease/Diagnosis:").grid(row=4, column=0, sticky='nw', pady=5)
        t_disease = tk.Text(f, height=4, width=30, bg=self.WHITE, fg=self.BLUE, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground=self.BLUE, highlightcolor=self.YELLOW)
        t_disease.grid(row=4, column=1, sticky='ew', padx=5, pady=5)
        t_disease.insert("1.0", safe_str(row.get('Disease')))
        
        ttk.Label(f, text="Payment Amount:").grid(row=0, column=2, sticky='w', padx=(20, 0), pady=5)
        ttk.Entry(f, textvariable=v_pay_amt).grid(row=0, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Payment Status:").grid(row=1, column=2, sticky='w', padx=(20, 0), pady=5)
        ttk.Combobox(f, textvariable=v_pay_stat, values=["Pending", "Paid", "Partially Paid"], state="readonly").grid(row=1, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Insurance Company:").grid(row=2, column=2, sticky='w', padx=(20, 0), pady=5)
        ttk.Entry(f, textvariable=v_ins_comp).grid(row=2, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Policy Number:").grid(row=3, column=2, sticky='w', padx=(20, 0), pady=5)
        ttk.Entry(f, textvariable=v_pol_num).grid(row=3, column=3, sticky='ew', padx=5)
        
        ttk.Label(f, text="Mediclaim Details:").grid(row=4, column=2, sticky='nw', padx=(20, 0), pady=5)
        t_mediclaim = tk.Text(f, height=4, width=30, bg=self.WHITE, fg=self.BLUE, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground=self.BLUE, highlightcolor=self.YELLOW)
        t_mediclaim.grid(row=4, column=3, sticky='ew', padx=5, pady=5)
        t_mediclaim.insert("1.0", safe_str(row.get('Mediclaim Details')))
        
        ttk.Label(f, text="Attached Document:").grid(row=5, column=0, sticky='w', pady=5)
        ttk.Entry(f, textvariable=v_doc_path, state='readonly').grid(row=5, column=1, sticky='ew', padx=5)
        
        def browse_edit_doc():
            filepath = filedialog.askopenfilename(title="Select Document")
            if filepath:
                v_doc_path.set(filepath)
        
        ttk.Button(f, text="Browse...", command=browse_edit_doc).grid(row=5, column=2, sticky='w', padx=5)
        
        def save_edit():
            try:
                self.df.at[index, 'Age'] = int(float(v_age.get().strip() or 0))
                self.df.at[index, 'Payment Amount'] = float(v_pay_amt.get().strip() or 0.0)
            except ValueError:
                messagebox.showerror("Validation Error", "Age and Payment Amount must be valid numbers.", parent=edit_win)
                return
                
            self.df.at[index, 'Name'] = v_name.get().strip()
            self.df.at[index, 'Gender'] = v_gender.get()
            self.df.at[index, 'Contact'] = v_contact.get()
            self.df.at[index, 'Disease'] = t_disease.get("1.0", tk.END).strip()
            self.df.at[index, 'Payment Status'] = v_pay_stat.get()
            self.df.at[index, 'Insurance Company'] = v_ins_comp.get()
            self.df.at[index, 'Policy Number'] = v_pol_num.get()
            self.df.at[index, 'Mediclaim Details'] = t_mediclaim.get("1.0", tk.END).strip()
            self.df.at[index, 'Attached Document'] = v_doc_path.get()
            
            save_data(self.df)
            self.refresh_database_view()
            messagebox.showinfo("Success", "Patient record updated successfully!", parent=edit_win)
            edit_win.destroy()
            
        ttk.Button(f, text="Save Changes", command=save_edit).grid(row=6, column=0, columnspan=4, pady=20)
        
        f.columnconfigure(1, weight=1)
        f.columnconfigure(3, weight=1)

    def download_excel(self):
        if self.filtered_df.empty:
            messagebox.showwarning("Warning", "No data to export.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Save Database as Excel"
        )
        if filepath:
            try:
                generate_excel(self.filtered_df, filepath)
                messagebox.showinfo("Success", f"Data exported successfully to {filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save Excel file. Ensure it is not open in another program.\n\nError: {e}")

    def download_table_pdf(self):
        if self.filtered_df.empty:
            messagebox.showwarning("Warning", "No data to export.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Database as PDF"
        )
        if filepath:
            try:
                generate_table_pdf(self.filtered_df, filepath)
                messagebox.showinfo("Success", f"Data exported successfully to {filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save PDF. Ensure the file is not open elsewhere.\n\nError: {e}")

    def download_patient_pdf(self):
        selected_patient = self.cb_patients.get()
        if not selected_patient or self.filtered_df.empty:
            messagebox.showwarning("Warning", "Please select a patient first.")
            return
            
        patient_data = self.filtered_df[self.filtered_df['Name'] == selected_patient].iloc[0].to_dict()
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"{selected_patient}_record.pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title=f"Save {selected_patient}'s Record"
        )
        
        if filepath:
            try:
                generate_patient_pdf(patient_data, filepath)
                messagebox.showinfo("Success", f"Patient record saved successfully to {filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save PDF. Ensure the file is not open elsewhere.\n\nError: {e}")

if __name__ == '__main__':
    app = PatientApp()
    app.mainloop()