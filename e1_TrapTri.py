import fuzzylite as fl

engine = fl.Engine(
    name="TipCalculator",

    input_variables=[
        fl.InputVariable(
            name="service",
            minimum=0.0,
            maximum=10.0,
            lock_range=False,
            terms=[
                fl.Trapezoid("poor", 0.0, 0.0, 2.5, 5.0),
                fl.Triangle("good", 2.5, 5.0, 7.5),
                fl.Trapezoid("excellent", 5.0, 7.5, 10.0, 10.0),
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
            maximum=30.0,
            lock_range=False,
            lock_previous=False,
            default_value=fl.nan,
            aggregation=fl.Maximum(),
            defuzzifier=fl.Centroid(100),
            terms=[
                fl.Triangle("cheap", 0.0, 5.0, 10.0),
                fl.Triangle("average", 10.0, 15.0, 20.0),
                fl.Triangle("generous", 20.0, 25.0, 30.0),
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

# Testing the engine for a given rating of service and food
engine.input_variable("service"). value = 2.0
engine.input_variable("food" ).value = 7.0
engine.process ()
print("y=", engine.output_variable("tip") .value)
print ("ỹ =", engine.output_variable("tip").fuzzy_value())