from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SalesChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(7, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot(self, summary, chart_type, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x_labels = summary["Product line"].astype(str).tolist()
        totals = summary["Total"].tolist()

        if chart_type == "Bar Chart":
            ax.bar(x_labels, totals, color="#2c7be5")
            ax.tick_params(axis='x', rotation=15)
        elif chart_type == "Line Chart":
            ax.plot(x_labels, totals, marker="o", linewidth=2, color="#00a676")
            ax.tick_params(axis='x', rotation=15)
        elif chart_type == "Pie Chart":
            ax.pie(totals, labels=x_labels, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")

        ax.set_title(title)

        if chart_type != "Pie Chart":
            ax.set_xlabel("Product Line")
            ax.set_ylabel("Total Penjualan (USD)")
            ax.grid(True, alpha=0.25)

        self.canvas.draw()
        
    def export_png(self, filepath):
        try:
            self.figure.savefig(filepath, dpi=300, bbox_inches='tight')
            return True
        except Exception as e:
            print(f"Error saving chart: {e}")
            return False