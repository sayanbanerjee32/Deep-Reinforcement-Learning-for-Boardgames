from datetime import datetime
from random import random

from experiment import Experiment
from TicTacToe.players.base_players import RandomPlayer, NovicePlayer, ExperiencedPlayer
from TicTacToe.players.reinforcePlayer import ReinforcePlayer, PGStrategy
from TicTacToe.environment.game import TicTacToe
from TicTacToe.environment.evaluation import evaluate_against_base_players
from plotting import Printer


class TrainReinforcePlayer(Experiment):

    def __init__(self, games, evaluations, pretrained_player, opponent):
        super(TrainReinforcePlayer, self).__init__()
        self.games = games
        self.evaluations = evaluations
        self.pretrained_player = pretrained_player.copy(shared_weights=False) if pretrained_player else None
        self.opponent = opponent

        self.__plotter__.line3_name = "opponent score"

    def reset(self):
        self.__init__(games=self.games, evaluations=self.evaluations, pretrained_player=self.pretrained_player, opponent=self.opponent)
        return self

    def run(self, lr, batch_size, silent=False):

        self.player1 = self.pretrained_player if self.pretrained_player else ReinforcePlayer(PGStrategy, lr=lr, batch_size=batch_size)
        self.player2 = self.opponent()

        self.simulation = TicTacToe([self.player1, self.player2])

        games_per_evaluation = self.games // self.evaluations
        start_time = datetime.now()
        for episode in range(1, self.evaluations+1):
            # train
            self.player1.strategy.train, self.player1.strategy.model.training = True, True  # training mode

            results, losses = self.simulation.run_simulations(games_per_evaluation)
            self.add_loss(sum(losses) / len(losses))    # losses are interesting during training

            # evaluate
            self.player1.strategy.train, self.player1.strategy.model.training = False, False  # eval mode
            main_score = evaluate_against_base_players(self.player1)
            opponent_score = evaluate_against_base_players(self.player1, [self.player2])
            self.add_scores(main_score, opponent_score)

            if not silent:
                if Printer.print_episode(episode*games_per_evaluation, self.games, datetime.now() - start_time):
                    self.plot_and_save(
                        "ReinforcementTraining vs %s LR: %s" % (self.player2.__class__.__name__, lr),
                        "Train ReinforcementPlayer vs %s with shared network\nLR: %s Games: %s \nFinal score: %s" % (self.opponent.__class__.__name__, lr, episode*games_per_evaluation, main_score))

        return self


if __name__ == '__main__':

    GAMES = 100000
    EVALUATIONS = 100
    LR = random()*1e-9 + 1e-3
    BATCH_SIZE = 32

    PLAYER = None  # Experiment.load_player("ReinforcePlayer using 3 layers pretrained on legal moves for 1000000 games.pth")
    OPPONENT = RandomPlayer

    print("Training ReinforcePlayer vs %s with lr: %s" % (OPPONENT, LR))
    experiment = TrainReinforcePlayer(games=GAMES, evaluations=EVALUATIONS, pretrained_player=PLAYER, opponent=OPPONENT)
    experiment.run(lr=LR, batch_size=BATCH_SIZE)

    print("Successfully trained on %s games, pretrained on %s" % (experiment.__plotter__.num_episodes, 10000000))

