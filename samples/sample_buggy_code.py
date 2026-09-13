"""
Sample buggy code for testing the AI Code Review Agent.
This code contains various bugs, security issues, and quality problems.
"""

def calculate_average(numbers):
    """Calculate average of numbers in a list."""
    sum = 0  # Bug: shadows built-in
    for num in numbers:
        sum += num
    return sum / len(numbers)  # Bug: division by zero if empty list


def get_user_by_id(user_id):
    """Get user from database by ID."""
    # Security: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return result


def process_file(filename):
    """Process a file and return contents."""
    # Bug: no error handling
    f = open(filename, 'r')  # Bug: file not closed (resource leak)
    data = f.read()
    return data


def find_max(arr):
    """Find maximum value in array."""
    max_val = arr[0]  # Bug: crashes if arr is empty
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val


def authenticate_user(username, password):
    """Authenticate user credentials."""
    # Security: hardcoded credentials
    admin_password = "admin123"
    
    if username == "admin" and password == admin_password:
        return True
    return False


class BankAccount:
    """Bank account with balance management."""
    
    def __init__(self, balance):
        self.balance = balance
    
    def withdraw(self, amount):
        """Withdraw amount from account."""
        # Bug: no validation for negative amounts or insufficient funds
        self.balance = self.balance - amount
        return self.balance
    
    def deposit(self, amount):
        """Deposit amount to account."""
        # Bug: allows negative deposits
        self.balance += amount


def search_items(items, target):
    """Search for target in items list."""
    # Performance: inefficient O(n²) search
    for i in range(len(items)):
        for j in range(len(items)):
            if items[i] == target and items[j] == target:
                return i
    return -1


# Quality: no main guard
print("Script started")
result = calculate_average([])  # Will crash!
