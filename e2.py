import fuzzylite as fl
import matplotlib.pyplot as plt
import numpy as np

# === Definición del motor difuso ===
engine = fl.Engine(
    name="TipCalculator",
    input_variables=[
        fl.InputVariable(
            name="service",
            minimum=0.0,
            maximum=10.0,
            lock_range=False,
            terms=[
                fl.Gaussian("poor", 0.0, 1.5),
                fl.Gaussian("good", 5.0, 1.5),
                fl.Gaussian("excellent", 10.0, 1.5),
            ],
        ),
        fl.InputVariable(
            name="food",
            minimum=0.0,
            maximum=10.0,
            lock_range=False,
            terms=[
                fl.Trapezoid("rancid", 0.0, 0.0, 1.0, 3.0),
                fl.Trapezoid("delicious", 7.0, 9.0, 10.0, 10.0),
            ],
        )
    ],
    output_variables=[
        fl.OutputVariable(
            name="tip",
            minimum=0.0,
            maximum=35.0,
            lock_range=False,
            lock_previous=False,
            default_value=fl.nan,
            aggregation=fl.Maximum(),
            defuzzifier=fl.Centroid(100),
            terms=[
                fl.Triangle("cheap", 0.0, 7.5, 15.0),
                fl.Triangle("average", 10.0, 17.5, 25.0),
                fl.Triangle("generous", 20.0, 27.5, 35.0),
            ],
        )
    ],
    rule_blocks=[
        fl.RuleBlock(
            name="mamdani",
            conjunction=fl.AlgebraicProduct(),
            disjunction=fl.AlgebraicSum(),
            implication=fl.AlgebraicProduct(),
            activation=fl.General(),
            rules=[
                fl.Rule.create("if service is poor or food is rancid then tip is cheap"),
                fl.Rule.create("if service is good then tip is average"),
                fl.Rule.create("if service is excellent or food is delicious then tip is generous"),
            ],
        )
    ]
)

# === Probar el motor con valores específicos ===
engine.input_variable("service").value = 2.0
engine.input_variable("food").value = 7.0
engine.process()

print("y =", engine.output_variable("tip").value)             # valor numérico
print("ỹ =", engine.output_variable("tip").fuzzy_value())     # valor difuso (porcentajes de pertenencia)

# === Graficar las funciones de membresía de 'tip' ===
tip = engine.output_variable("tip")
x = np.linspace(tip.minimum, tip.maximum, 1000)

plt.figure(figsize=(8, 5))
for term in tip.terms:
    y = [term.membership(xi) for xi in x]
    plt.plot(x, y, label=term.name)

plt.title("Funciones de membresía - Tip")
plt.xlabel("Propina")
plt.ylabel("Pertenencia")
plt.legend()
plt.grid(True)
plt.show()
