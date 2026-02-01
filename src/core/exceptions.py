"""
Custom exceptions for the shipping charge estimator.
"""


class ShippingError(Exception):
    """Base exception for shipping-related errors."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(ShippingError):
    """Exception raised when a requested resource is not found."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ValidationError(ShippingError):
    """Exception raised for invalid input data."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
