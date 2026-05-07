# implementation of singleton in Python 
class DatabaseConnection:
    _instance = None
    def __new__(cls, *args, **kwargs):
        # if the instance doesn't exists we create it 
        if cls._instance is None:
            print("Creating the ONLY instance")
            cls._instance = super().__new__(cls)
            cls._instance.connection_string = "jdbc:postgresql://localhost:5432/mydb"
        return cls._instance

# --- CLIENT CODE ---

# Let's try to create multiple databases
db1 = DatabaseConnection()
db2 = DatabaseConnection()
db3 = DatabaseConnection()

# They look like separate variables, but they are exactly the same object!
print(f"db1 is db2? {db1 is db2}") # Returns: True
print(f"db2 is db3? {db2 is db3}") # Returns: True

# Changing state in one variable changes it for all of them
db1.connection_string = "New Connection String!"
print(db3.connection_string) # Returns: "New Connection String!"

# PROS:
# + Ensures that only one instance of a class exists.
# + Provides a single shared access point to some resource.
# + Can be useful for configuration, logging, or shared managers.

# CONS:
# - Introduces global state.
# - Can make testing harder because state is shared between tests.
# - Can hide dependencies instead of passing them explicitly.
# - Basic implementation is not thread-safe : by mistake we can creare two instances.
# - In real applications, dependency injection is often a cleaner solution.