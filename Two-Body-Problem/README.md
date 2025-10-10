## Overview

In classical mechanics, the two-body problem is to calculate and predict the motion of two massive bodies that are orbitting each other in space.
The program visualizes this using python library, Pygame. There are available presets, and a custom mode where parameters can be manually tuned via on-screen sliders.

----

## How it works

### The Two-Body Problem

The two-body problem describes the motion of two point masses 𝑚1 and 𝑚2 interacting through Newton’s law of universal gravitation:
> F₁₂ = -G * m₁ * m₂ / |r₂ - r₁|³ * (r₂ - r₁)


By Newton’s second law (F = m * a), the coupled differential equations of motion are:

> m₁ * d²r₁/dt² = F₁₂

> m₂ * d²r₂/dt² = -F₁₂


The center of mass (barycenter) moves uniformly in the absence of external forces, allowing the problem to reduce to a single relative-motion equation using the reduced mass:

> μ * d²r/dt² = -G * m₁ * m₂ / r³ * r

> μ = (m₁ * m₂) / (m₁ + m₂)


The analytical solutions are conic sections — circles, ellipses, parabolas, or hyperbolas — depending on the total mechanical energy:

> E = ½ * μ * v² - G * m₁ * m₂ / r


Where:

> `E < 0` → Bound orbit (elliptical or circular)

> `E = 0` → Parabolic escape trajectory

> `E > 0` → Hyperbolic flyby

## Implementation
### 1. Differential Equation Setup

The simulation defines the two-body system using:

> `def two_body_ode(t, y, G, m1, m2):`


This computes the accelerations of both bodies based on the inverse-square gravitational law and returns:

> dr/dt = v

> dv/dt = a

### 2. Numerical Integration

To evolve the system in time, the following solver is used:

```
solve_ivp(..., method='RK45')`
```

This applies the Runge–Kutta 4/5 adaptive step integrator, providing high numerical stability and precision. However there may be better methods as this cannot guarantee to fully preserve energy or angular momentum.

### 3. Visualization and Scaling

`pygame` handles real-time rendering. Each body’s position is transformed from physical coordinates to screen coordinates using:

```python
def to_screen_coords(pos, com, scale):
    x, y = pos
    cx, cy = com
    return int((WIDTH - SIDEBAR_WIDTH) / 2 + (x - cx) * scale), int(HEIGHT / 2 - (y - cy) * scale)
```
This performs three operations:

Translation: 
- Subtracts the center of mass (cx, cy) so that the barycenter remains visually fixed at the center of the window.

Scaling: 
- Multiplies by scale to map physical distances to pixels.

Screen Alignment:
- (WIDTH - SIDEBAR_WIDTH)/2 and HEIGHT/2 center the coordinate system on screen.
- The negative sign in the y-term flips the vertical axis since pygame’s y-coordinates increase downward.



| **Preset** | **Description** | **Physical Interpretation (Equations)** |
|---|---:|---|
| **Circular Orbit** | Two-body system where each mass traces a circular path about the barycenter. | `G*m1*m2/r^2 = m1*v1^2/r1 = m2*v2^2/r2`<br>`v = sqrt(G*(m1 + m2)/r)` |
| **Elliptical Orbit** | Bound two-body system (eccentricity 0 < e < 1). | `1/r = (1 + e*cos(theta)) / (a*(1 - e^2))`<br>`epsilon = -G*(m1+m2)/(2*a)`<br>`h = sqrt(G*(m1+m2)*a*(1 - e^2))` |
| **Spinning Pair** | Equal-mass binary symmetric about barycenter. | `m1 = m2 => r1 = r2 = r/2`<br>`v = sqrt(G*(2*m)/r)`<br>`L_total = m*r*v` |
| **Other (Custom)** | Customizable initial conditions; solved numerically. |  |

----
## To use

Prerequisites
- Python 3.6 or higher

### Setup
Clone this repository or download the files:
```shell
git clone <repository-url>
cd "Bacon Cypher"
```

Create a virtual environment

``` 
python -m venv .venv
```

Enable virtual environment

On Windows:
```
.venv\Scripts\activate
```

On macOS/Linux:
```
source .venv/bin/activate
```

To run the following program, make sure all packages are installed:
```
pip install -r requirements.txt
```

Finally: 
```
python main.py
```

## Extension ideas
- Include energy and angular momentum visualization
- Support pause/resume and reset buttons