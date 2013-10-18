import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from sql_connection import *
from add_customer import *
from find_customer import *

class ShopWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #create actions - these can be used in menus/toolbars etc.
        self.open_database = QAction("Open Database",self)
        self.close_database = QAction("Close Database",self)
        self.add_customer = QAction("Add Customer",self)
        self.browse_customers = QAction("Browse Customers",self)
        self.add_order = QAction("Add Order",self)
        self.browse_orders = QAction("Browse Orders",self)
        self.add_product = QAction("Add Product",self)
        self.browse_products = QAction("Browse Products",self)
        self.add_customer.setShortcuts("Ctrl+q")

        #create the menubar
        self.menu_bar = QMenuBar()
        self.database_menu = self.menu_bar.addMenu("Database")
        self.customer_menu = self.menu_bar.addMenu("Customer")
        self.order_menu = self.menu_bar.addMenu("Order")
        self.product_menu = self.menu_bar.addMenu("Product")
        #add the actions to the menubar
        self.database_menu.addAction(self.open_database)
        self.database_menu.addAction(self.close_database)
        self.customer_menu.addAction(self.add_customer)
        self.customer_menu.addAction(self.browse_customers)
        self.order_menu.addAction(self.add_order)
        self.order_menu.addAction(self.browse_orders)
        self.product_menu.addAction(self.add_product)
        self.product_menu.addAction(self.browse_products)

        #create toolbars
        self.database_toolbar = QToolBar("Manage Databases")
        self.customer_toolbar = QToolBar("Manage Customers")
        self.order_toolbar = QToolBar("Manage Orders")
        self.product_toolbar = QToolBar("Manage Products")
        #add actions to toolbars
        self.database_toolbar.addAction(self.open_database)
        self.database_toolbar.addAction(self.close_database)
        self.customer_toolbar.addAction(self.add_customer)
        self.customer_toolbar.addAction(self.browse_customers)
        self.order_toolbar.addAction(self.add_order)
        self.order_toolbar.addAction(self.browse_orders)
        self.product_toolbar.addAction(self.add_product)
        self.product_toolbar.addAction(self.browse_products)

        #add toolbars to window
        self.addToolBar(self.database_toolbar)
        self.addToolBar(self.customer_toolbar)
        self.addToolBar(self.order_toolbar)
        self.addToolBar(self.product_toolbar)

        #connections
        self.open_database.triggered.connect(self.open_database_file)
        self.add_customer.triggered.connect(self.add_customer_view)
        self.add_order.triggered.connect(self.add_order_view)

    def open_database_file(self):
        path = QFileDialog.getOpenFileName(caption="Open Database",filter="Database file (*.db *.dat)")
        self.connection = SQLConnection(path)
        self.connection.open_database()

    def add_customer_view(self):
        self.add_customer_widget = AddCustomerWidget()
        self.setCentralWidget(self.add_customer_widget)
        #connect the custom signal in the widget to our method
        self.add_customer_widget.customerAddedSignal.connect(self.process_save_customer)

    def process_save_customer(self):
        details = self.add_customer_widget.customer_details()
        self.connection.add_new_customer(details)
        self.add_customer_widget.clear_details()

    def add_order_view(self):
        self.add_order_widget = FindCustomerWidget(self.connection)
        self.setCentralWidget(self.add_order_widget)

if __name__ == "__main__":
    application  = QApplication(sys.argv)
    window = ShopWindow()
    window.show()
    window.raise_()
    application.exec_()
