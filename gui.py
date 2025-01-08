from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QComboBox, QListWidget, QWidget, QHBoxLayout, QMessageBox, QCheckBox, QDialog, QListWidgetItem)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import grn

class GRNGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GRN Operations")
        self.setGeometry(100, 100, 1200, 700)

        # Initialize GRN object
        self.my_grn = grn.grn()
        self.regulators = []
        self.products = []

        # Main Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Regulator Section
        self.regulator_layout = QHBoxLayout()
        self.regulator_name_label = QLabel("Name:")
        self.regulator_name_input = QLineEdit()
        self.regulator_type_label = QLabel("Type:")
        self.regulator_type_combo = QComboBox()
        self.regulator_type_combo.addItems(["1", "-1"])
        self.regulator_kd_label = QLabel("Kd:")
        self.regulator_kd_input = QLineEdit()
        self.regulator_n_label = QLabel("n:")
        self.regulator_n_input = QLineEdit()
        self.add_regulator_button = QPushButton("Add Regulator")
        self.add_regulator_button.clicked.connect(self.add_regulator)

        self.regulator_layout.addWidget(self.regulator_name_label)
        self.regulator_layout.addWidget(self.regulator_name_input)
        self.regulator_layout.addWidget(self.regulator_type_label)
        self.regulator_layout.addWidget(self.regulator_type_combo)
        self.regulator_layout.addWidget(self.regulator_kd_label)
        self.regulator_layout.addWidget(self.regulator_kd_input)
        self.regulator_layout.addWidget(self.regulator_n_label)
        self.regulator_layout.addWidget(self.regulator_n_input)
        self.regulator_layout.addWidget(self.add_regulator_button)
        self.layout.addLayout(self.regulator_layout)

        # Product Section
        self.product_layout = QHBoxLayout()
        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.product_delta_label = QLabel("Delta:")
        self.product_delta_input = QLineEdit()
        self.add_product_button = QPushButton("Add Product")
        self.add_product_button.clicked.connect(self.add_product)

        self.product_layout.addWidget(self.product_name_label)
        self.product_layout.addWidget(self.product_name_input)
        self.product_layout.addWidget(self.product_delta_label)
        self.product_layout.addWidget(self.product_delta_input)
        self.product_layout.addWidget(self.add_product_button)
        self.layout.addLayout(self.product_layout)

        # Regulators and Products List Section
        self.selection_layout = QHBoxLayout()

        self.regulator_list_label = QLabel("Select Regulators:")
        self.regulator_selection_list = QListWidget()
        self.regulator_selection_list.setFixedHeight(150)
        self.regulator_selection_list.setSelectionMode(QListWidget.MultiSelection)

        self.product_list_label = QLabel("Select Products:")
        self.product_selection_list = QListWidget()
        self.product_selection_list.setFixedHeight(150)
        self.product_selection_list.setSelectionMode(QListWidget.MultiSelection)

        self.selection_layout.addWidget(self.regulator_list_label)
        self.selection_layout.addWidget(self.regulator_selection_list)
        self.selection_layout.addWidget(self.product_list_label)
        self.selection_layout.addWidget(self.product_selection_list)

        self.layout.addLayout(self.selection_layout)

        # Gene Creation Section
        self.gene_layout = QHBoxLayout()
        self.alpha_label = QLabel("Alpha:")
        self.alpha_input = QLineEdit()
        self.logic_type_label = QLabel("Logic Type:")
        self.logic_type_combo = QComboBox()
        self.logic_type_combo.addItems(["and", "or", "mixed"])
        self.create_gene_button = QPushButton("Create Gene")
        self.create_gene_button.clicked.connect(self.create_gene)

        self.gene_layout.addWidget(self.alpha_label)
        self.gene_layout.addWidget(self.alpha_input)
        self.gene_layout.addWidget(self.logic_type_label)
        self.gene_layout.addWidget(self.logic_type_combo)
        self.gene_layout.addWidget(self.create_gene_button)
        self.layout.addLayout(self.gene_layout)

        # Created Genes Section
        self.gene_list_layout = QHBoxLayout()

        self.gene_list_label = QLabel("Created Genes:")
        self.gene_list = QListWidget()
        self.gene_list.setFixedWidth(300)

        self.gene_list_layout.addWidget(self.gene_list_label)
        self.gene_list_layout.addWidget(self.gene_list)

        # Network Visualization Section
        self.network_layout = QVBoxLayout()
        self.network_canvas = FigureCanvas(plt.figure())
        self.network_layout.addWidget(self.network_canvas)

        self.layout.addLayout(self.gene_list_layout)
        self.layout.addLayout(self.network_layout)

    def add_regulator(self):
        name = self.regulator_name_input.text().strip()
        try:
            if not name or not name[0].isalpha():
                raise ValueError("Regulator name must start with a letter.")

            reg_type = int(self.regulator_type_combo.currentText())
            kd = int(self.regulator_kd_input.text().strip())
            n = int(self.regulator_n_input.text().strip())

            regulator = {"name": name, "type": reg_type, "Kd": kd, "n": n}
            self.my_grn.add_input_species(name)
            self.regulators.append(regulator)

            list_item = QListWidgetItem(f"{name} (Type: {reg_type}, Kd: {kd}, n: {n})")
            self.regulator_selection_list.addItem(list_item)

            self.my_grn.add_input_species(name)  # Add input species to the GRN

            # Clear inputs
            self.regulator_name_input.clear()
            self.regulator_kd_input.clear()
            self.regulator_n_input.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def add_product(self):
        name = self.product_name_input.text().strip()
        try:
            if not name or not name[0].isalpha():
                raise ValueError("Product name must start with a letter.")

            delta = float(self.product_delta_input.text().strip())
            self.my_grn.add_species(name, delta)
            self.products.append({"name": name, "delta": delta})

            list_item = QListWidgetItem(f"{name} (Delta: {delta})")
            self.product_selection_list.addItem(list_item)

            # Clear inputs
            self.product_name_input.clear()
            self.product_delta_input.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def create_gene(self):
        try:
            alpha = int(self.alpha_input.text().strip())
            logic_type = self.logic_type_combo.currentText()

            selected_regulators = [self.regulators[idx.row()] for idx in self.regulator_selection_list.selectedIndexes()]
            selected_products = [self.products[idx.row()] for idx in self.product_selection_list.selectedIndexes()]

            if not selected_regulators or not selected_products:
                raise ValueError("Please select at least one regulator and one product.")

            self.my_grn.add_gene(alpha, selected_regulators, selected_products, logic_type=logic_type)

            regulator_names = [reg["name"] for reg in selected_regulators]
            product_names = [prod["name"] for prod in selected_products]
            gene_description = (f"Alpha: {alpha}, Logic Type: {logic_type}, Regulators: {', '.join(regulator_names)}, "
                                f"Products: {', '.join(product_names)}")
            self.gene_list.addItem(gene_description)

            # Clear inputs
            self.alpha_input.clear()
            self.regulator_selection_list.clearSelection()
            self.product_selection_list.clearSelection()

            QMessageBox.information(self, "Success", "Gene created successfully.")
            self.update_network_visualization()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_network_visualization(self):
        plt.clf()
        self.my_grn.plot_network()
        self.network_canvas.draw()

if __name__ == "__main__":
    app = QApplication([])
    gui = GRNGUI()
    gui.show()
    app.exec_()
