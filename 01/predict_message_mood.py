from model import SomeModel


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:

    model_prediction = model.predict(message)

    if model_prediction < bad_thresholds:
        return "неуд"
    elif model_prediction < good_thresholds:
        return "норм"
    else:
        return "отл"

