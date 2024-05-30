import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def load_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if not filepath:
        return
    try:
        global df
        df = pd.read_excel(filepath)
        if validate_data(df):
            process_data(df)
        else:
            messagebox.showerror("Error", "Invalid data format.")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading file: {e}")

def validate_data(df):
    required_columns = {'User', 'Date', 'Command', 'Gateway', 'Fixture'}
    if not required_columns.issubset(df.columns):
        return False
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except Exception:
            return False
    return True

def process_data(df):
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        df['time_diff'] = df['Date'].diff().dt.total_seconds().div(60).fillna(0)
        df['cycle'] = (df['time_diff'] > 40).cumsum()
        
        global cycles
        cycles = df.groupby('cycle').agg(
            horaminima=('Date', 'min'),
            horamaxima=('Date', 'max'),
            comandosEnviados=('Command', 'count')
        ).reset_index(drop=True)
        
        cycles['tiempotranscurrido'] = (cycles['horamaxima'] - cycles['horaminima']).dt.total_seconds() / 60
        
        display_results(cycles)
    except Exception as e:
        messagebox.showerror("Error", f"Error processing data: {e}")

def display_results(cycles):
    for row in tree.get_children():
        tree.delete(row)
    
    for idx, row in cycles.iterrows():
        tree.insert("", "end", values=(
            row['horaminima'], row['horamaxima'],
            f"{row['tiempotranscurrido']:.2f}",
            row['comandosEnviados']
        ))

def save_to_excel():
    if cycles.empty:
        messagebox.showwarning("Warning", "No data to save. Please load and process a file first.")
        return
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if not filepath:
        return

    try:
        cycles.to_excel(filepath, index=False)
        messagebox.showinfo("Success", f"File saved successfully: {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")

def save_fixture_analysis_to_excel():
    if fixtures.empty:
        messagebox.showwarning("Warning", "No fixture analysis data to save. Please analyze fixture commands first.")
        return
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if not filepath:
        return

    try:
        fixtures.to_excel(filepath, index=False)
        messagebox.showinfo("Success", f"File saved successfully: {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")

def analyze_fixture_commands():
    if cycles.empty:
        messagebox.showwarning("Warning", "No data to analyze. Please load and process a file first.")
        return
    
    try:
        min_commands = command_min_entry.get()
        max_commands = command_max_entry.get()
        
        if min_commands and not min_commands.isdigit():
            messagebox.showerror("Error", "Minimum commands value should be an integer.")
            return
        
        if max_commands and not max_commands.isdigit():
            messagebox.showerror("Error", "Maximum commands value should be an integer.")
            return
        
        min_commands = int(min_commands) if min_commands else None
        max_commands = int(max_commands) if max_commands else None
        
        # Ensure the 'cycle' column is in df before performing the analysis
        global df
        if 'cycle' not in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values(by='Date')
            df['time_diff'] = df['Date'].diff().dt.total_seconds().div(60).fillna(0)
            df['cycle'] = (df['time_diff'] > 40).cumsum()
        
        fixture_analysis = df.groupby(['cycle', 'Fixture']).size().reset_index(name='CommandCount')
        
        if min_commands is not None and max_commands is not None:
            filtered_fixtures = fixture_analysis[
                (fixture_analysis['CommandCount'] >= min_commands) & 
                (fixture_analysis['CommandCount'] <= max_commands)
            ]
        elif min_commands is not None:
            filtered_fixtures = fixture_analysis[fixture_analysis['CommandCount'] == min_commands]
        else:
            messagebox.showerror("Error", "Please specify a valid range or exact value for command count.")
            return
        
        global fixtures
        fixtures = filtered_fixtures
        display_fixture_analysis_results(filtered_fixtures)
    except Exception as e:
        messagebox.showerror("Error", f"Error analyzing fixture commands: {e}")

def display_fixture_analysis_results(fixtures):
    for row in tree_analysis.get_children():
        tree_analysis.delete(row)

    for idx, row in fixtures.iterrows():
        tree_analysis.insert("", "end", values=(
            row['cycle'], row['Fixture'], row['CommandCount']
        ))

root = tk.Tk()
root.title("Cycle Analysis")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Button(frame, text="Load Excel File", command=load_file).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame, text="Save to Excel", command=save_to_excel).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame, text="Analyze Fixture Commands", command=analyze_fixture_commands).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(frame, text="Save Fixture Analysis to Excel", command=save_fixture_analysis_to_excel).grid(row=0, column=3, padx=5, pady=5)

ttk.Label(frame, text="Min Commands:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
command_min_entry = ttk.Entry(frame, width=10)
command_min_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(frame, text="Max Commands:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
command_max_entry = ttk.Entry(frame, width=10)
command_max_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

columns = ("horaminima", "horamaxima", "tiempotranscurrido", "comandosEnviados")
tree = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.W)

tree.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

analysis_columns = ("cycle", "fixture", "CommandCount")
tree_analysis = ttk.Treeview(frame, columns=analysis_columns, show="headings")
for col in analysis_columns:
    tree_analysis.heading(col, text=col)
    tree_analysis.column(col, anchor=tk.W)

tree_analysis.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

cycles = pd.DataFrame()  # Global variable to store the cycles DataFrame
df = pd.DataFrame()  # Global variable to store the original DataFrame
fixtures = pd.DataFrame()  # Global variable to store the fixture analysis results

root.mainloop()
