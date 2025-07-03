import copy
import random

class Hat:
    def __init__(self, **balls):
        self.contents = []
        for color, count in balls.items():
            self.contents.extend([color] * count)

    def draw(self, num_balls_drawn):
        if num_balls_drawn >= len(self.contents):
            drawn = self.contents.copy()
            self.contents.clear()
            return drawn
        return [self.contents.pop(random.randrange(len(self.contents))) for _ in range(num_balls_drawn)]



def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    success_count = 0

    for _ in range(num_experiments):
        hat_copy = copy.deepcopy(hat)
        drawn_balls = hat_copy.draw(num_balls_drawn)

        drawn_count = {}
        for ball in drawn_balls:
            if ball in drawn_count:
                drawn_count[ball] += 1
            else:
                drawn_count[ball] = 1

        success = True
        for color, count in expected_balls.items():
            if drawn_count.get(color, 0) < count:
                success = False
                break

        if success:
            success_count += 1

    return success_count / num_experiments