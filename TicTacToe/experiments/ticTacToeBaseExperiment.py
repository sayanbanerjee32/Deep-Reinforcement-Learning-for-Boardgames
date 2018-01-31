from datetime import datetime

import TicTacToe.config as config
from TicTacToe.environment.board import TicTacToeBoard
from TicTacToe.players.base_players import ExperiencedPlayer, RandomPlayer
from experiment import Experiment


class TicTacToeBaseExperiment(Experiment):

    def __init__(self, experiment_path):
        super(TicTacToeBaseExperiment, self).__init__(experiment_path)

    def generate_supervised_training_data(self, games, labeling_strategy):
        """
        Generates training data by applying random moves to a board and labeling each sample with the move that :param labeling_strategy would have taken given the board.

        :param games: The number of games to be simulated
        :param labeling_strategy: The strategy used to label each sample. The label equals labeling_strategy.get_move(board)
        :return: a list of tuples(board_sample, move_label)
        """

        labeling_strategy.color = config.BLACK

        generator = RandomPlayer()
        color_iterator = self.AlternatingColorIterator()

        start = datetime.now()
        training_set = []
        for game in range(games):
            board = TicTacToeBoard()
            for i in range(9):
                # generate training pair
                expert_move = labeling_strategy.get_move(board)
                training_set.append((board.board.copy(), expert_move))

                # prepare for next sample
                move = generator.get_move(board)
                board.apply_move(move, color_iterator.__next__())

        print("Generated %s training pairs form %s games in %s" % (len(training_set), games, datetime.now() - start))
        return training_set
