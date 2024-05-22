import math

def custom_function(x, a, b, c, t):
    return (a * x) + b - (c / (x - t))

def custom_function2(x, a, b, c, t, i = 0):
    if (a == 0 and b == 0 and c == 0 and t == 0):
        return 0
    if (t == x or a < 0):
        return 0
    try :
      return ((x + a*t - b + math.sqrt(x**2 + a**2 * t**2 + b**2 - 2*x*a*t - 2*x*b + 2*a*t*b + 4*a*c)) / (2*a))
    except ValueError:
        print("i: ", i)
        return ((x + a*t - b) / (2*a))
