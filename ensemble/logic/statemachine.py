class StateMachine:
    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.run()
    # Template method:
    def runAll(self, inputs):
            self.currentState = self.currentState.next_state(inputs)
            self.currentState.run()
