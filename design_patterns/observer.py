# Bad code!
# Less extensible version
class EmailService:
    def send_confirmation(self, order_id):
        return f"Sending the email confirmation of {order_id}"

class InventoryService:
    def update_stock(self, order_id):
        return f"Updating the stock for {order_id}"

class BadOrder:
    def __init__(self, order_id):
        self.order_id = order_id
        self.email_service = EmailService()
        self.inventory_stock = InventoryService()
    
    def complete_order(self):
        print(f"Order {self.order_id} completed.")
        # We manually call every service. 
        # If we add SMS, we must change this method!
        self.email_service.send_confirmation(self.order_id)
        self.inventory_stock.update_stock(self.order_id)

order  = BadOrder(1234)
order.complete_order()
 

# GOOD CODE: Observer Pattern
from abc import ABC, abstractmethod

# --- 1. INTERFACES ---
class Observer(ABC):
    @abstractmethod
    def update(self, order_id: int):
        pass

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass
        
    @abstractmethod
    def detach(self, observer: Observer):
        pass
        
    @abstractmethod
    def notify(self):
        pass


# --- 2. CONCRETE OBSERVERS (Subscribers) ---

class EmailService(Observer):
    def update(self, order_id: int):
        print(f"EmailService: Sending email for order {order_id}")

class InventoryService(Observer):
    def update(self, order_id: int):
        print(f"InventoryService: Updating stock for order {order_id}")

class InvoiceService(Observer):
    def update(self, order_id: int):
        print(f"InvoiceService: Generating invoice for order {order_id}")

# --- 3. CONCRETE SUBJECT (Publisher) ---
class Order(Subject):
    def __init__(self, order_id: int):
        self.order_id = order_id
        self._observers = [] # list of subscribers
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)    
    
    def notify(self):
        for observer in self._observers:
            observer.update(self.order_id)

    def complete_order(self):
        print(f"Order {self.order_id} has been completed")
        self.notify()

# --- CLIENT CODE --- 
order = Order(9999)

# create services
email_service = EmailService()
inventory_service = InventoryService()
invoice_service = InvoiceService()

# attach
order.attach(email_service)
order.attach(inventory_service)
order.attach(invoice_service)

order.complete_order()

# we can even "turn of" some funciontalites during a runtime e.g.
order.detach(email_service)
order.complete_order()

# PROS:
# + Loose coupling — Order does not depend on concrete services.
# + Open/Closed Principle — we can add SmsService without changing the Order class.
# + Runtime flexibility — observers can be attached or detached dynamically.
# + Good fit when multiple independent actions should happen after one event.

# CONS:
# - Can be overkill for simple flows.
# - Execution order can become implicit and fragile.
# - Errors in one observer may affect notification of the others if not handled.
# - Long-lived subjects may keep references to observers and prevent garbage collection if detach is forgotten.
# - Harder debugging: control flow is less explicit than direct method calls.