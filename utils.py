def factor (n: int) -> list[int]:
  """
  Compute the prime factors of a given integer
  
  :param n: The integer to factor
  :return: A list of prime factors of n
  """

  factors= []
  if n <= 1:
    return factors

  while n % 2 == 0:
    factors.append(2)
    n //= 2
  
  divisor = 3
  while divisor**2 <= n:
    if n % divisor == 0:
      factors.append(divisor)
      n = n // divisor
    else: 
      divisor += 2

  if n > 1:
    factors.append(n) # After the loop, n is either 1 or the last prime factor

  return factors