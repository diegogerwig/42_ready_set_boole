def adder(a: int, b: int) -> int:
    """Suma dos números naturales. Complejidad: O(log n)[cite: 149, 152]."""
    while b != 0:
        carry = a & b # [cite: 154]
        a = a ^ b     # [cite: 156]
        b = carry << 1 # [cite: 157]
    return a