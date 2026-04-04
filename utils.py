def all_divisors(n: int) -> list[int]:
    """Return all divisors of n (excluding 1)."""
    divisors = []
    
    for i in range(2, n + 1):  # just try every number
        if n % i == 0:
            divisors.append(i)
    
    return divisors