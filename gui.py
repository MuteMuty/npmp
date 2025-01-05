import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import sys

from grn import grn
import simulator

root = tk.Tk()
root.title("GReNMlin GUI")
root.geometry("900x700")

current_grn = None

def load_grn_from_json(filepath):
    new_grn = grn()
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Load species
    for sp in data.get('species', []):
        name = sp.get('name', 'species')
        delta = sp.get('delta', 0.0)
        new_grn.add_species(name, delta)

    # Load genes
    for gene in data.get('genes', []):
        alpha = gene.get('alpha', 1.0)
        regulators = gene.get('regulators', [])
        products = gene.get('products', [])
        logic_type = gene.get('logic_type', 'and')
        new_grn.add_gene(alpha, regulators, products, logic_type)

    # Load input species
    for inp in data.get('input_species', []):
        new_grn.add_input_species(inp)

    # Load parameters (param1/param2/param3)
    params = data.get('params', {})
    entry_param1.delete(0, tk.END)
    entry_param1.insert(0, str(params.get('param1', 0.0)))
    entry_param2.delete(0, tk.END)
    entry_param2.insert(0, str(params.get('param2', 0.0)))
    entry_param3.delete(0, tk.END)
    entry_param3.insert(0, str(params.get('param3', 0.0)))

    # Show species in a text field
    text_species.delete("1.0", tk.END)
    text_species.insert(tk.END, "Loaded species:\n")
    for s in new_grn.species_names:
        text_species.insert(tk.END, f"  {s}\n")

    return new_grn

def load_grn():
    global current_grn
    filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
    if not filepath:
        return
    try:
        current_grn = load_grn_from_json(filepath)
        if current_grn:
            messagebox.showinfo("Datoteka naložena", "Gensko regulatorno omrežje je uspešno naloženo.")
        else:
            messagebox.showerror("Napaka", "Datoteke ni bilo mogoče naložiti.")
    except Exception as e:
        messagebox.showerror("Napaka", f"Napaka pri nalaganju datoteke: {e}")

def plot_in_frame(fig, frame):
    # Clear old widgets
    for widget in frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def run_simulation():
    global current_grn
    if not current_grn:
        messagebox.showerror("Napaka", "Najprej naloži gensko regulatorno omrežje!")
        return
    try:
        param1 = float(entry_param1.get())
        param2 = float(entry_param2.get())
        param3 = float(entry_param3.get())
        # Example: run simulation and generate a figure
        # Replace with the real simulation function as needed.
        fig = plt.figure()
        current_grn.plot_network()
        ax = fig.gca()
        ax.set_title(f"Simulacija s parametri: {param1}, {param2}, {param3}")
        plot_in_frame(fig, frame_plot)
    except Exception as e:
        messagebox.showerror("Napaka", f"Napaka pri simulaciji: {e}")

def save_results():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if filepath:
        try:
            # Serialize results or model as needed
            with open(filepath, 'w') as f:
                f.write("Shranjeni podatki...")  # Replace with actual data
            messagebox.showinfo("Shranjevanje", f"Rezultati so shranjeni na: {filepath}")
        except Exception as e:
            messagebox.showerror("Napaka", f"Napaka pri shranjevanju rezultatov: {e}")

# Top Buttons Row
frame_top = tk.Frame(root, pady=10)
frame_top.pack(fill=tk.X)

btn_load = tk.Button(frame_top, text="Naloži GRN", command=load_grn)
btn_load.pack(side=tk.LEFT, padx=5)

btn_run = tk.Button(frame_top, text="Zaženi simulacijo", command=run_simulation)
btn_run.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(frame_top, text="Shrani rezultate", command=save_results)
btn_save.pack(side=tk.LEFT, padx=5)

# Parameters
frame_params = tk.LabelFrame(root, text="Nastavitve simulacije", padx=10, pady=10)
frame_params.pack(fill=tk.X, padx=10, pady=10)

tk.Label(frame_params, text="Parameter 1:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_param1 = tk.Entry(frame_params)
entry_param1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_params, text="Parameter 2:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_param2 = tk.Entry(frame_params)
entry_param2.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_params, text="Parameter 3:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_param3 = tk.Entry(frame_params)
entry_param3.grid(row=2, column=1, padx=5, pady=5)

# Species Display
frame_species = tk.LabelFrame(root, text="Species Information")
frame_species.pack(fill=tk.X, padx=10, pady=10)
text_species = tk.Text(frame_species, height=5, width=50)
text_species.pack(fill=tk.X)

# Plot Frame at Bottom
frame_plot = tk.LabelFrame(root, text="Vizualizacija")
frame_plot.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()