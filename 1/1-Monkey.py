class MonkeyBananaProblem:
    def __init__(self, monkey, banana, box):
        self.monkey = monkey
        self.banana = banana
        self.box = box
        self.monkey_on_box = False
        self.has_banana = False
        self.step = 0

    def Monkey_go_box(self):
        self.step += 1
        print(f"step: {self.step} Monkey goes to {self.box} from {self.monkey}")
        self.monkey = self.box

    def Monkey_move_box(self):
        self.step += 1
        print(f"step: {self.step} Monkey catches the box from {self.box} to {self.banana}")
        self.box = self.banana
        self.monkey = self.banana

    def Monkey_on_box(self):
        self.step += 1
        print(f"step: {self.step} Monkey climbs the box.")
        self.monkey_on_box = True

    def Monkey_get_banana(self):
        self.step += 1
        print(f"step: {self.step} Monkey gets the banana!")
        self.has_banana = True

    def solve(self):
        if self.monkey != self.box:
            self.Monkey_go_box()
        if self.box != self.banana:
            self.Monkey_move_box()
        if not self.monkey_on_box:
            self.Monkey_on_box()
        if not self.has_banana:
            self.Monkey_get_banana()

monkey, banana, box = map(int, input().split())
problem = MonkeyBananaProblem(monkey, banana, box)
problem.solve()