import unittest
from unittest import mock

from predict_message_mood import predict_message_mood, ThresholdsError
from model import SomeModel


class TestPredictMessageMood(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SomeModel()

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_normal_cond(self, mock_predict):
        mock_predict.side_effect = [0.2, 0.4, 0.9]

        bad_thresholds = 0.3
        good_thresholds = 0.8

        result1 = predict_message_mood(
            message="Чапаев и Пустота",
            model=self.model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result2 = predict_message_mood(
            message="Generation П",
            model=self.model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result3 = predict_message_mood(
            message="Голубое сало",
            model=self.model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        self.assertEqual(result1, "неуд")
        self.assertEqual(result2, "норм")
        self.assertEqual(result3, "отл")

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_count_predict_calls(self, mock_predict):
        mock_predict.return_value = 0.3

        message = "Понедельник начинается в субботу"
        predict_message_mood(message=message, model=self.model)

        mock_predict.assert_called_once_with(message)

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_edge_cond(self, mock_predict):
        mock_predict.side_effect = [0, 0.3, 0.8]

        bad_thresholds = 0.3
        good_thresholds = 0.8

        result1 = predict_message_mood(
            message="Надзирать и наказывать",
            model=self.model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result2 = predict_message_mood(
            message="Над пропастью во ржи",
            model=self.model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result3 = predict_message_mood(
            message="Тихий Дон",
            model=self.model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        self.assertEqual(result1, "неуд")
        self.assertEqual(result2, "норм")
        self.assertEqual(result3, "норм")

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_thresholds_equals(self, mock_predict):
        mock_predict.return_value = 0.3

        bad_thresholds = 0.3
        good_thresholds = 0.3

        result = predict_message_mood(
            message="Пикник на обочине",
            model=self.model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        self.assertEqual(result, "норм")

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_swap_thresholds(self, mock_predict):
        mock_predict.return_value = 0.3

        bad_thresholds = 0.8
        good_thresholds = 0.3

        with self.assertRaises(ThresholdsError):
            predict_message_mood(
                message="Пикник на обочине",
                model=self.model,
                bad_thresholds=bad_thresholds,
                good_thresholds=good_thresholds,
            )

    def test_model_not_some_model(self):
        bad_thresholds = 0.3
        good_thresholds = 0.8

        with self.assertRaises(TypeError):
            predict_message_mood(
                message="Вишневый сад",
                model=42,
                bad_thresholds=bad_thresholds,
                good_thresholds=good_thresholds,
            )

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_message_not_str(self, mock_predict):
        mock_predict.return_value = 0.3

        bad_thresholds = 0.8
        good_thresholds = 0.3

        with self.assertRaises(TypeError):
            predict_message_mood(
                message=42,
                model=self.model,
                bad_thresholds=bad_thresholds,
                good_thresholds=good_thresholds,
            )

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_bad_thresholds_not_int(self, mock_predict):
        mock_predict.return_value = 0.3

        bad_thresholds = "Хорошо, что сундуки остались наверху"
        good_thresholds = 0.8

        with self.assertRaises(TypeError):
            predict_message_mood(
                message="Палата №6",
                model=self.model,
                bad_thresholds=bad_thresholds,
                good_thresholds=good_thresholds,
            )

    @mock.patch("predict_message_mood.SomeModel.predict")
    def test_good_thresholds_not_int(self, mock_predict):
        mock_predict.return_value = 0.3

        bad_thresholds = 0.3
        good_thresholds = "Ой мама пришла"

        with self.assertRaises(TypeError):
            predict_message_mood(
                message="Чайка",
                model=self.model,
                bad_thresholds=bad_thresholds,
                good_thresholds=good_thresholds,
            )


if __name__ == "__main__":
    unittest.main()
