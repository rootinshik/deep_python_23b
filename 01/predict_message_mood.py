from model import SomeModel


class ThresholdsError(Exception):
    def __init__(
        self,
        bad_thresholds: float,
        good_thresholds: float,
        message: str = "Bad threshold greater then good threshold",
    ):
        super().__init__(message + f": {bad_thresholds=}, {good_thresholds=}")


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
    if model_prediction > good_thresholds:
        return "отл"
    return "норм"
