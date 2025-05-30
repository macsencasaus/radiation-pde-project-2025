# Radiation Transport Project

We are attempting to solve the radiation transport equation:

$$
\Omega \cdot \nabla_x \Psi(x, \Omega) + \sigma^t \Psi(x, \Omega) = \frac {\sigma^s} {|\mathbb{S}^2|} \int_{\mathbb{S}^2} \Psi(x, \Omega') \ d \Omega' + q(x).
$$

This project was made with Python 3.11.

## Installation

Install dependencies with
```
pip install -r requirements.txt
```
ideally into a fresh Python virtual environment.

## Testing

Pytest is used for unit testing and can be installed using pip on Windows or apt on Debian-based Linux distros.

Run unit tests with
```
pytest
```
The main file is solve_radiation_transport.py.