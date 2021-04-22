# Do not modify these lines
__winc_id__ = '7b9401ad7f544be2a23321292dd61cb6'
__human_name__ = 'arguments'

# Add your code after this line

# part 1
def greet (name: str, greeting: str ='Hello, <name>!') -> str:
    return greeting.replace('<name>', name)

print (greet('Bob'))
print (greet('Bob', 'Hi <name>'))

# part 2
def force (mass: float, body: str = 'earth'):
    celestial_bodies = {
        'sun': 274.0,
        'jupiter': 24.9,
        'neptune': 11.2,
        'saturn': 10.4,
        'earth': 9.8,
        'uranus': 8.9,
        'venus': 8.9,
        'mars': 3.7,
        'mercury': 3.7,
        'moon': 1.6,
        'pluto': 0.6
    }
    return mass * celestial_bodies[body]

print (force(2))

#part 3
def pull (m1: float, m2: float, d: float):
    return (6.674 * 10**-11) * ((m1 * m2)/ d**2)

print (pull(0.1, 5.972 * 10**24, 6.371 * 10**6))
print (pull(800.0, 1500.0, 3.0))