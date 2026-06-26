from pathlib import Path
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QMainWindow,
    QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget, QPushButton, QFileDialog, QMessageBox
)
from chart_widget import SalesChartWidget
from data_loader import get_categories, filter_by_category, load_sales_data, summarize_data

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supermarket Sales Dashboard")
        self.resize(1100, 700)

        self.csv_path = Path(__file__).parent / "data" / "supermarket_sales.csv"
        self.df = load_sales_data(self.csv_path)

        self.setup_ui()
        self.update_dashboard()

    def setup_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("City:"))
        self.category_filter = QComboBox()
        self.category_filter.addItems(get_categories(self.df))
        self.category_filter.currentTextChanged.connect(self.update_dashboard)
        filter_layout.addWidget(self.category_filter)

        filter_layout.addWidget(QLabel("Jenis Chart:"))
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Bar Chart", "Line Chart", "Pie Chart"])
        self.chart_type.currentTextChanged.connect(self.update_dashboard)
        filter_layout.addWidget(self.chart_type)

        filter_layout.addStretch()

        self.btn_refresh = QPushButton("Refresh Data")
        self.btn_refresh.clicked.connect(self.refresh_data)
        filter_layout.addWidget(self.btn_refresh)

        self.btn_export = QPushButton("Export Chart (PNG)")
        self.btn_export.clicked.connect(self.export_chart)
        filter_layout.addWidget(self.btn_export)

        main_layout.addLayout(filter_layout)

        self.summary_label = QLabel()
        main_layout.addWidget(self.summary_label)

        content_layout = QHBoxLayout()

        self.table = QTableWidget()
        content_layout.addWidget(self.table, stretch=2)

        self.chart = SalesChartWidget()
        content_layout.addWidget(self.chart, stretch=3)

        main_layout.addLayout(content_layout)

    def update_dashboard(self):
        selected_category = self.category_filter.currentText()
        chart_type = self.chart_type.currentText()

        filtered_df = filter_by_category(self.df, selected_category)
        summary = summarize_data(filtered_df)

        self.update_summary(filtered_df)
        self.update_table(filtered_df)
        self.chart.plot(summary, chart_type, f"Penjualan per Product Line - {selected_category}")

    def update_summary(self, df):
        total_sales = df["Total"].sum()
        total_rows = len(df)
        total_products = df["Product line"].nunique()

        self.summary_label.setText(
            f"Total pendapatan: $ {total_sales:,.2f} | "
            f"Jumlah transaksi: {total_rows} | "
            f"Kategori produk: {total_products}"
        )

    def update_table(self, df):
        columns = ["Invoice ID", "City", "Customer type", "Product line", "Total"]

        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for row_index, row in df.reset_index(drop=True).iterrows():
            for col_index, column in enumerate(columns):
                value = row[column]
                if column == "Total":
                    value = f"$ {value:,.2f}"
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()

    def refresh_data(self):
        self.df = load_sales_data(self.csv_path)
        
        current_category = self.category_filter.currentText()
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItems(get_categories(self.df))
        
        if current_category in [self.category_filter.itemText(i) for i in range(self.category_filter.count())]:
            self.category_filter.setCurrentText(current_category)
            
        self.category_filter.blockSignals(False)
        self.update_dashboard()

    def export_chart(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Simpan Chart", "", "PNG Image (*.png)"
        )
        if filepath:
            success = self.chart.export_png(filepath)
            if success:
                QMessageBox.information(self, "Sukses", "Chart berhasil disimpan!")
            else:
                QMessageBox.critical(self, "Error", "Gagal menyimpan chart.")