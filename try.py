import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import grn
import simulator
import numpy as np

class GRNGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GRN Modeling GUI")
        self.root.geometry("1200x800")

        # Initialize variables
        self.my_grn = grn.grn()

        # Top-level layout
        self.frame_top = tk.Frame(root, pady=10)
        self.frame_top.pack(fill=tk.X)

        # Buttons
        self.btn_load = tk.Button(self.frame_top, text="Load GRN", command=self.load_grn)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_add_species = tk.Button(self.frame_top, text="Add Species", command=self.add_species)
        self.btn_add_species.pack(side=tk.LEFT, padx=5)

        self.btn_add_gene = tk.Button(self.frame_top, text="Add Gene", command=self.add_gene)
        self.btn_add_gene.pack(side=tk.LEFT, padx=5)

        self.btn_run = tk.Button(self.frame_top, text="Run Simulation", command=self.run_simulation)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        self.btn_save = tk.Button(self.frame_top, text="Save Results", command=self.save_results)
        self.btn_save.pack(side=tk.LEFT, padx=5)

        # Parameters section
        self.frame_params = tk.LabelFrame(root, text="Simulation Settings", padx=10, pady=10)
        self.frame_params.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(self.frame_params, text="Parameter 1:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_param1 = tk.Entry(self.frame_params)
        self.entry_param1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_params, text="Parameter 2:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_param2 = tk.Entry(self.frame_params)
        self.entry_param2.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_params, text="Parameter 3:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_param3 = tk.Entry(self.frame_params)
        self.entry_param3.grid(row=2, column=1, padx=5, pady=5)

        # Species display section
        self.frame_species = tk.LabelFrame(root, text="Species Information")
        self.frame_species.pack(fill=tk.X, padx=10, pady=10)

        self.text_species = tk.Text(self.frame_species, height=5, width=50)
        self.text_species.pack(fill=tk.X)

        # Visualization frame
        self.frame_plot = tk.LabelFrame(root, text="Visualization")
        self.frame_plot.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_grn_from_json(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Load species
        for sp in data.get('species', []):
            name = sp.get('name', 'species')
            delta = sp.get('delta', 0.0)
            self.my_grn.add_species(name, delta)

        # Load genes
        for gene in data.get('genes', []):
            alpha = gene.get('alpha', 1.0)
            regulators = gene.get('regulators', [])
            products = gene.get('products', [])
            logic_type = gene.get('logic_type', 'and')
            self.my_grn.add_gene(alpha, regulators, products, logic_type)

        # Load input species
        for inp in data.get('input_species', []):
            self.my_grn.add_input_species(inp)

        # Display species
        self.text_species.delete("1.0", tk.END)
        self.text_species.insert(tk.END, "Loaded species:\n")
        for s in self.my_grn.species_names:
            self.text_species.insert(tk.END, f"  {s}\n")

    def load_grn(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if not filepath:
            return
        try:
            self.load_grn_from_json(filepath)
            messagebox.showinfo("Success", "Gene regulatory network loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")

    def add_species(self):
        species_window = tk.Toplevel(self.root)
        species_window.title("Add Species")

        tk.Label(species_window, text="Species Name:").grid(row=0, column=0, padx=5, pady=5)
        species_name = tk.Entry(species_window)
        species_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(species_window, text="Degradation Rate (Delta):").grid(row=1, column=0, padx=5, pady=5)
        species_delta = tk.Entry(species_window)
        species_delta.grid(row=1, column=1, padx=5, pady=5)

        def save_species():
            name = species_name.get()
            try:
                delta = float(species_delta.get())
                self.my_grn.add_species(name, delta)
                self.text_species.insert(tk.END, f"Added species: {name} (Delta: {delta})\n")
                species_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid degradation rate")

        tk.Button(species_window, text="Add", command=save_species).grid(row=2, column=0, columnspan=2, pady=10)

    def add_gene(self):
        gene_window = tk.Toplevel(self.root)
        gene_window.title("Add Gene")

        tk.Label(gene_window, text="Alpha:").grid(row=0, column=0, padx=5, pady=5)
        gene_alpha = tk.Entry(gene_window)
        gene_alpha.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(gene_window, text="Regulators (JSON):").grid(row=1, column=0, padx=5, pady=5)
        gene_regulators = tk.Entry(gene_window, width=50)
        gene_regulators.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(gene_window, text="Products (JSON):").grid(row=2, column=0, padx=5, pady=5)
        gene_products = tk.Entry(gene_window, width=50)
        gene_products.grid(row=2, column=1, padx=5, pady=5)

        def save_gene():
            try:
                alpha = float(gene_alpha.get())
                regulators = eval(gene_regulators.get())
                products = eval(gene_products.get())
                self.my_grn.add_gene(alpha, regulators, products)
                self.text_species.insert(tk.END, f"Added gene: Alpha={alpha}\n")
                gene_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(gene_window, text="Add", command=save_gene).grid(row=3, column=0, columnspan=2, pady=10)

    def plot_in_frame(self, fig):
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_simulation(self):
        try:
            param1 = self.validate_float_input(self.entry_param1.get(), "Parameter 1")
            param2 = self.validate_float_input(self.entry_param2.get(), "Parameter 2")
            param3 = self.validate_float_input(self.entry_param3.get(), "Parameter 3")

            # Simulate sequence
            simulation_results = simulator.simulate_sequence(
                self.my_grn, [(0, 0), (0, 100), (100, 0), (100, 100)], t_single=250
            )

            if len(simulation_results) == 2:
                T, Y = simulation_results
            else:
                raise ValueError("Unexpected output from simulate_sequence")

            # Plot results
            fig, ax = plt.subplots()
            ax.plot(T, Y)
            ax.set_title("Simulation Results")
            ax.set_xlabel("Time")
            ax.set_ylabel("Output")
            self.plot_in_frame(fig)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error during simulation: {e}")

    def validate_float_input(self, value, name):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"{name} must be a valid number.")

    def save_results(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                results = {
                    "species": self.my_grn.species_names,
                    "genes": self.my_grn.genes,
                    "parameters": {
                        "param1": self.entry_param1.get(),
                        "param2": self.entry_param2.get(),
                        "param3": self.entry_param3.get()
                    }
                }
                with open(filepath, 'w') as f:
                    json.dump(results, f, indent=4)
                messagebox.showinfo("Success", f"Results saved to: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving results: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GRNGUI(root)
    root.mainloop()
