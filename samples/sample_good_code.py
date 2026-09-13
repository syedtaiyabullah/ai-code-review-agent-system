"""
Sample good code demonstrating best practices.
This code should receive minimal or no issues from the review agent.
"""

from typing import List, Optional
import os


def calculate_average(numbers: List[float]) -> float:
    """
    Calculate the average of numbers in a list.
    
    Args:
        numbers: List of numbers to average
        
    Returns:
        The average value, or 0.0 if list is empty
        
    Raises:
        TypeError: If numbers contains non-numeric values
    """
    if not numbers:
        return 0.0
    
    total = sum(numbers)  # Using built-in sum
    return total / len(numbers)


def get_user_by_id(user_id: int, db_connection) -> Optional[dict]:
    """
    Get user from database by ID using parameterized query.
    
    Args:
        user_id: The user's ID
        db_connection: Database connection object
        
    Returns:
        User dictionary or None if not found
    """
    # Security: Using parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE id = ?"
    result = db_connection.execute(query, (user_id,))
    return result.fetchone()


def process_file(filename: str) -> str:
    """
    Process a file and return its contents safely.
    
    Args:
        filename: Path to the file
        
    Returns:
        File contents as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    # Using context manager to ensure file is closed
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading file: {e}")


def find_max(arr: List[float]) -> Optional[float]:
    """
    Find maximum value in array.
    
    Args:
        arr: List of numbers
        
    Returns:
        Maximum value or None if array is empty
    """
    if not arr:
        return None
    
    return max(arr)  # Using built-in max


class BankAccount:
    """Bank account with balance management and validation."""
    
    def __init__(self, initial_balance: float = 0.0):
        """
        Initialize bank account.
        
        Args:
            initial_balance: Starting balance (must be non-negative)
            
        Raises:
            ValueError: If initial_balance is negative
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        """Get current balance."""
        return self._balance
    
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw amount from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful, False if insufficient funds
            
        Raises:
            ValueError: If amount is negative or zero
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self._balance:
            return False  # Insufficient funds
        
        self._balance -= amount
        return True
    
    def deposit(self, amount: float) -> None:
        """
        Deposit amount to account.
        
        Args:
            amount: Amount to deposit
            
        Raises:
            ValueError: If amount is negative or zero
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount


def search_items(items: List, target) -> int:
    """
    Search for target in items list efficiently.
    
    Args:
        items: List to search in
        target: Item to find
        
    Returns:
        Index of first occurrence or -1 if not found
    """
    try:
        return items.index(target)
    except ValueError:
        return -1


def main():
    """Main entry point of the script."""
    # Example usage
    numbers = [1.0, 2.0, 3.0, 4.0, 5.0]
    avg = calculate_average(numbers)
    print(f"Average: {avg}")
    
    # Test with empty list
    empty_avg = calculate_average([])
    print(f"Empty list average: {empty_avg}")
    
    # Bank account example
    account = BankAccount(initial_balance=1000.0)
    print(f"Initial balance: ${account.balance}")
    
    if account.withdraw(100.0):
        print(f"Withdrew $100. New balance: ${account.balance}")
    
    account.deposit(50.0)
    print(f"Deposited $50. New balance: ${account.balance}")


if __name__ == "__main__":
    main()
