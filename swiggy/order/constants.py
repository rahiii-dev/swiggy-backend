PENDING = 1
CONFIRMED = 2
COOKING = 3
INDELIVERY = 4
DELIVERED = 5
CANCELLED=6

ORDER_STATUS = (
    (PENDING, 'Pending for restaurant to confirm'),
    (CONFIRMED, 'Restaurant Confirmed'),
    (COOKING, 'Cooking Your Cusine'),
    (INDELIVERY, 'Out For Delivery'),
    (DELIVERED, 'Delivered'),
    (CANCELLED, 'Yor Order is cancelled'),
)