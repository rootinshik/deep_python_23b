from model import SomeModel


class ThresholdsError(Exception):
    def __init__(self,
                 bad_thresholds: float,
                 good_thresholds: float,
                 message: str = "Bad threshold greater then good thresholds"
                 ):
        self.bad_thresholds = bad_thresholds
        self.good_thresholds = good_thresholds
        self.message = message
        super().__init__(self.message + f': {self.bad_thresholds=}, {self.good_thresholds=}')


def predict_message_mood(
        message: str,
        model: SomeModel,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    if bad_thresholds > good_thresholds:
        raise ThresholdsError(bad_thresholds, good_thresholds)

    model_prediction = model.predict(message)

    if model_prediction < bad_thresholds:
        return "неуд"
    elif model_prediction < good_thresholds:
        return "норм"
    else:
        return "отл"
