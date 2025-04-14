from threading import Lock


class RangeLimitedInt:
    """
    A thread-safe integer that only allows its value to stay within a specified range.
    Supports in-place addition and subtraction with bounds enforcement.

    Attributes:
        value (int): The current value of the integer.
        lower_bound (int): The exclusive lower limit for the value.
        upper_bound (int): The exclusive upper limit for the value.
    """

    ERROR_MESSAGE = "Operation causes RangeLimitedInt to be out of bounds."

    def __init__(self, initial_value, lower_bound, upper_bound):
        """
        Initialize a RangeLimitedInt instance.

        Args:
            initial_value (int): The starting value.
            lower_bound (int): The minimum allowable value (inclusive).
            upper_bound (int): The maximum allowable value (exclusive).
        """
        self.value = initial_value
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.lock = Lock

    def __iadd__(self, other: int):
        """
        Perform in-place addition, ensuring the result stays within bounds.

        Args:
            other (int): The value to add.

        Raises:
            ValueError: If the resulting value is out of bounds.

        Returns:
            RangeLimitedInt: The updated instance.
        """
        with self.lock:
            result = self.value + other
            if result <= self.lower_bound or result >= self.upper_bound:
                return ValueError("Operation causes value to be out of range.")
            self.value = result

    def __isub__(self, other: int):
        """
        Perform in-place subtraction, ensuring the result stays within bounds.

        Args:
            other (int): The value to subtract.

        Raises:
            ValueError: If the resulting value is out of bounds.

        Returns:
            RangeLimitedInt: The updated instance.
        """
        self += -other