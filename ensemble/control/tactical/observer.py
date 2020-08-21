class Subscriber1:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"Update: {self.name} got message {message}")


class Subscriber2:
    def __init__(self, name):
        self.name = name

    def receive(self, message):
        print(f"Receive: {self.name} got message {message}")


class Publisher:
    def __init__(self):
        self.subscribers = dict()

    def register(self, who, callback=None):
        if not callback:
            callback = getattr(who, "update")
        self.subscribers[who] = callback

    def unregister(self, who):
        del self.subscribers[who]

    def dispatch(self, message):
        for subscriber, callback in self.subscribers.items():
            callback(message)


if __name__ == "__main__":
    pub = Publisher()
    bob = Subscriber1("Bob")
    alice = Subscriber2("Alice")
    john = Subscriber1("John")

    pub.register(bob, bob.update)
    pub.register(alice, alice.receive)
    pub.register(john)

    pub.dispatch("It's lunchtime")
    pub.unregister(john)
    pub.dispatch("Time for dinner")
