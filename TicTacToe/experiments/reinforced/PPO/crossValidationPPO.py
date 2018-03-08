from random import uniform
from datetime import datetime

from experiment import Experiment
from TicTacToe.experiments.reinforced.PPO.trainPPOPlayer import TrainPPOPlayer


class PPOCrossValidation(Experiment):

    def __init__(self, nested_experiment, steps):
        super(PPOCrossValidation, self).__init__()
        self.nested_experiment = nested_experiment
        self.steps = steps

    def reset(self):
        self.nested_experiment.reset()
        return self

    def run(self, iterations, lr_lower_boundary, lr_upper_boundary, clip_lower_boundary, clip_upper_boundary):

        results = []
        for i in range(iterations):
            LR = 10 ** uniform(lr_lower_boundary, lr_upper_boundary)
            CLIP = uniform(clip_lower_boundary, clip_upper_boundary)

            print("\nIteration %s/%s" % (i+1, iterations))
            print("Running CrossValidation for %s with lr: %s" % (self.nested_experiment.__class__.__name__, LR))

            self.nested_experiment.reset().run(lr=LR, clip=CLIP, steps=self.steps)
            results.append((self.nested_experiment.final_score, LR))

        return sorted(results, reverse=True)


if __name__ == '__main__':

    start = datetime.now()

    GAMES = 1000000
    EVALUATIONS = 1000
    STEPS = 32

    PLAYER = None  # PLAYER = Experiment.load_player("ReinforcePlayer using 3 layers pretrained on legal moves for 1000000 games.pth")

    experiment = PPOCrossValidation(TrainPPOPlayer(games=GAMES, evaluations=EVALUATIONS, pretrained_player=PLAYER), STEPS)

    results = experiment.run(5, -4, -6, 0.1, 0.5)

    print("\nFinal Reward - LR:")
    for res in results:
        print("%s - %s" % (res[0], res[1]))

    print("\nCrossvalidation complete, took: %s" % (datetime.now() - start))
