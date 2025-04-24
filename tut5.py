import cmath
import math


def plant_tf(w, k=4, T=0.1):
    # Calculate the exponential term e^(-jwT)
    exp_term = cmath.exp(-1j * w * T)
    # Calculate the denominator (jω + 1)
    denominator = 1j * w + 1
    # Compute the transfer function
    result = (k * exp_term) / denominator
    return result


def delay(w):
    T = 0.1
    return cmath.exp(-1j * w * T)
    


def print_complex(z):
    magnitude = 20 * math.log10(abs(z))

    # Calculate phase (in radians)
    phase_radians = cmath.phase(z)

    # Convert phase to degrees
    phase_degrees = math.degrees(phase_radians)
    print(f"Magnitude: {magnitude}")
    print(f"Phase (in degrees): {phase_degrees}")



for w in [0.1, 1, 2, 10, 150]:

    open_loop = plant_tf(w)
    d = delay(w)
    i = 1/(1j * w)


    # Output the results
    print("------------------------------------------------")
    print(f"Frequency: {w} rad.s^-1")
    print("")
    print("Coordinate:")
    print_complex(open_loop)
    print("")
    print("Width:")
    print_complex(d)
    print("")
    print("Integrator effect:")
    print_complex(i)
    print("------------------------------------------------")
    print("")
