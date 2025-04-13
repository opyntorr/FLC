import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# === Variables de entrada ===
service = ctrl.Antecedent(np.arange(0, 11, 0.1), 'service')
food = ctrl.Antecedent(np.arange(0, 11, 0.1), 'food')

# === Variable de salida (con funciones gaussianas) ===
tip = ctrl.Consequent(np.arange(-10, 35, 0.1), 'tip')

# === Funciones de membresía para inputs ===
service['poor'] = fuzz.trimf(service.universe, [0, 0, 5])
service['good'] = fuzz.trimf(service.universe, [0, 5, 10])
service['excellent'] = fuzz.trimf(service.universe, [5, 10, 10])

food['rancid'] = fuzz.trimf(food.universe, [0, 0, 5])
food['delicious'] = fuzz.trimf(food.universe, [5, 10, 10])

# === Funciones gaussianas para la salida tip ===
tip['low'] = fuzz.gaussmf(tip.universe, 0.0, 3.0)
tip['medium'] = fuzz.gaussmf(tip.universe, 12.5, 3.0)
tip['high'] = fuzz.gaussmf(tip.universe, 25.0, 3.0)

# === Reglas ===
rule1 = ctrl.Rule(service['poor'] | food['rancid'], tip['low'])
rule2 = ctrl.Rule(service['good'], tip['medium'])
rule3 = ctrl.Rule(service['excellent'] | food['delicious'], tip['high'])

# === Sistema de control ===
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# === Probar con valores específicos ===
tipping.input['service'] = 2.0
tipping.input['food'] = 7.0

# === Procesar ===
tipping.compute()

# === Resultado ===
print("y =", tipping.output['tip'])

# Obtener valor de salida
y = tipping.output['tip']

# Calcular pertenencias a cada término
μ_low = fuzz.gaussmf(y, 0.0, 3.0)
μ_medium = fuzz.gaussmf(y, 12.5, 3.0)
μ_high = fuzz.gaussmf(y, 25.0, 3.0)

# Imprimir resultados
print(f"y = {y:.2f}")
print(f"Pertenencia a 'low': {μ_low:.3f}")
print(f"Pertenencia a 'medium': {μ_medium:.3f}")
print(f"Pertenencia a 'high': {μ_high:.3f}")

# === Graficar las funciones de membresía de tip ===
tip.view()
plt.show()
