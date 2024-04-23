import math

def custom_function(x, a, b, c, t):
    return (a * x) + b - (c / (x - t))

def custom_function2(x, a, b, c, t):
    # return (a-x-b-(math.sqrt((x-a+b)**2 + 4*a*(b*t-x*t+c))))/(-2*a)
    # return (-c + b * x - t * x + a * x ** 2)/(b - t + a * x)
    # return ((-(x - b + a*t) - math.sqrt((x - b + a*t)**2 + 4*a*(b*x + c -x*t))) / (-2*a))
    try :
        return ((x + a*t - b + math.sqrt(x**2 + a**2 * t**2 + b**2 - 2*x*a*t - 2*x*b + 2*a*t*b + 4*a*c)) / (2*a))
    except ValueError:
        return ((x + a*t - b) / (2*a))


# print(custom_function2(1, 1.187007890214598, -5.710606183008009, -1.7266992864636055, 7.222988454538003))
# print(custom_function2(1, 1.187007890214598, -5.710606183008009, -1.7266992864636055, 7.222988454538003))
# print(custom_function(0, 1.187007890214598, -5.710606183008009, -1.7266992864636055, 7.222988454538003))