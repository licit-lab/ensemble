========
Runtime
========

The general architecture of the system is composed by two main commands the first one the

Runtime Architecture
====================

The runtime architecture is represented as a state machine.

.. figure:: ../_static/runtime.png
    :width: 500px
    :align: center
    :height: 500px
    :alt: alternate text
    :figclass: align-center

The following are the general descriptions of the `states`:

* `Compliance`: All checkups to validate correct inputs to the runtime are validated.
* `Connect`: A connection between this API and the traffic simulator is opened
* `Initialize`: All value initializations for the scenario are set up
* `PreRoutine`: All required tasks before the interaction with the simulator are performed
* `Query`: All data is retrieved from the simulator and parsed to the API.
* `Control`: Information from the simulator is inserted for a control decision (Tactical/Operational)
* `Push`: Decisions from the control strategy are pushed back to the simulator
* `PostRoutine`: All tasks required after the step are performed here.
* `Terminate`: Indicates that the scenario was terminated
