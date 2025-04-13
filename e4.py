import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# === Universos ===
sensor_range = np.arange(0, 11, 0.1)  # 0 = cerca, 10 = lejos
motor_range = np.arange(0, 10, 0.1)   # 0 = reversa, 9 = adelante

# === Variables de entrada ===
left_sensor = ctrl.Antecedent(sensor_range, 'left_sensor')
front_sensor = ctrl.Antecedent(sensor_range, 'front_sensor')
right_sensor = ctrl.Antecedent(sensor_range, 'right_sensor')

# === Variables de salida ===
left_motor = ctrl.Consequent(motor_range, 'left_motor')
right_motor = ctrl.Consequent(motor_range, 'right_motor')

# === Funciones de membresía para sensores ===
left_sensor['near'] = fuzz.trapmf(sensor_range, [0, 0, 3, 5])
left_sensor['far']  = fuzz.trapmf(sensor_range, [4, 6, 10, 10])
front_sensor['near'] = fuzz.trapmf(sensor_range, [0, 0, 3, 5])
front_sensor['far']  = fuzz.trapmf(sensor_range, [4, 6, 10, 10])
right_sensor['near'] = fuzz.trapmf(sensor_range, [0, 0, 3, 5])
right_sensor['far']  = fuzz.trapmf(sensor_range, [4, 6, 10, 10])

# === Funciones de membresía para motores ===
left_motor['reverse'] = fuzz.trapmf(motor_range, [6, 7, 9, 9])
left_motor['forward'] = fuzz.trapmf(motor_range, [0, 0, 3, 4])
right_motor['reverse'] = fuzz.trapmf(motor_range, [6, 7, 9, 9])
right_motor['forward'] = fuzz.trapmf(motor_range, [0, 0, 3, 4])

# === Reglas de comportamiento reactivo (según tabla del artículo de Rusu) ===
rules = [
    ctrl.Rule(left_sensor['far'] & front_sensor['far'] & right_sensor['far'],
              (left_motor['forward'], right_motor['forward'])),

    ctrl.Rule(left_sensor['far'] & front_sensor['far'] & right_sensor['near'],
              (left_motor['reverse'], right_motor['forward'])),

    ctrl.Rule(left_sensor['far'] & front_sensor['near'] & right_sensor['far'],
              (left_motor['forward'], right_motor['reverse'])),

    ctrl.Rule(left_sensor['far'] & front_sensor['near'] & right_sensor['near'],
              (left_motor['reverse'], right_motor['reverse'])),

    ctrl.Rule(left_sensor['near'] & front_sensor['far'] & right_sensor['far'],
              (left_motor['forward'], right_motor['reverse'])),

    ctrl.Rule(left_sensor['near'] & front_sensor['far'] & right_sensor['near'],
              (left_motor['reverse'], right_motor['reverse'])),

    ctrl.Rule(left_sensor['near'] & front_sensor['near'] & right_sensor['far'],
              (left_motor['reverse'], right_motor['reverse'])),

    ctrl.Rule(left_sensor['near'] & front_sensor['near'] & right_sensor['near'],
              (left_motor['reverse'], right_motor['reverse'])),
]

# === Sistema de control ===
robot_ctrl = ctrl.ControlSystem(rules)
robot_sim = ctrl.ControlSystemSimulation(robot_ctrl)

# Simulación con sensores activados
robot_sim.input['left_sensor'] = 2.0
robot_sim.input['front_sensor'] = 8.0
robot_sim.input['right_sensor'] = 8.0

# Ejecutar lógica difusa
robot_sim.compute()

# Mostrar resultados
print(f"Velocidad del motor izquierdo: {robot_sim.output['left_motor']:.2f}")
print(f"Velocidad del motor derecho: {robot_sim.output['right_motor']:.2f}")

# Ver funciones de entrada
left_sensor.view()
front_sensor.view()
right_sensor.view()

# Ver funciones de salida
left_motor.view(sim=robot_sim)
right_motor.view(sim=robot_sim)

plt.show()