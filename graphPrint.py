import fuzzylite as fl
import matplotlib.pyplot as plt
import numpy as np

# === Variable de entrada 'service' ===
service = fl.InputVariable(
    name="tip",
    minimum=0.0,
    maximum=35.0,
    lock_range=False,
    terms=[
        fl.Triangle("cheap", 0.0, 7.5, 15.0),
        fl.Triangle("average", 10.0, 17.5, 25.0),
        fl.Triangle("generous", 20.0, 27.5, 35.0),
    ],
)

# === Crear eje X ===
x = np.linspace(service.minimum, service.maximum, 1000)

# === Graficar cada término ===
plt.figure(figsize=(8, 5))
for term in service.terms:
    y = [term.membership(xi) for xi in x]
    plt.plot(x, y, label=term.name)

# === Formato de la gráfica ===
plt.title("Funciones de membresía - Service")
plt.xlabel("Nivel de servicio")
plt.ylabel("Pertenencia")
plt.legend()
plt.grid(True)
plt.show()
