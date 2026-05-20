import enum


class UserRole(enum.Enum):
    ADMIN = 'admin'
    GUEST = 'guest'


class OrderStatus(enum.Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
