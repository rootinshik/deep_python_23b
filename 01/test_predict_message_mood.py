import unittest
from unittest import mock

from predict_message_mood import predict_message_mood, ThresholdsError


class TestPredictMessageMood(unittest.TestCase):
    @mock.patch("predict_message_mood.SomeModel", autospec=True)
    def test_normal_cond(self, mock_model):
        mock_model = mock_model.return_value
        mock_model.predict.side_effect = [0.2, 0.4, 0.9]

        bad_thresholds = 0.3
        good_thresholds = 0.8

        result1 = predict_message_mood(
            message="Чапаев и Пустота",
            model=mock_model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result2 = predict_message_mood(
            message="Generation П",
            model=mock_model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result3 = predict_message_mood(
            message="Голубое сало",
            model=mock_model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        self.assertEqual(result1, "неуд")
        self.assertEqual(result2, "норм")
        self.assertEqual(result3, "отл")

    @mock.patch("predict_message_mood.SomeModel", autospec=True)
    def test_count_predict_calls(self, mock_model):
        mock_model = mock_model.return_value
        mock_model.predict.return_value = 0.3

        message = "Понедельник начинается в субботу"
        predict_message_mood(message=message, model=mock_model)

        expected_calls = [mock.call.predict(message)]
        self.assertEqual(mock_model.mock_calls, expected_calls)

    @mock.patch("predict_message_mood.SomeModel", autospec=True)
    def test_edge_cond(self, mock_model):
        mock_model = mock_model.return_value
        mock_model.predict.side_effect = [0, 0.3, 0.8]

        bad_thresholds = 0.3
        good_thresholds = 0.8

        result1 = predict_message_mood(
            message="Надзирать и наказывать",
            model=mock_model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result2 = predict_message_mood(
            message="Над пропастью во ржи",
            model=mock_model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        result3 = predict_message_mood(
            message="Тихий Дон",
            model=mock_model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )

        self.assertEqual(result1, "неуд")
        self.assertEqual(result2, "норм")
        self.assertEqual(result3, "норм")

    @mock.patch("predict_message_mood.SomeModel", autospec=True)
    def test_thresholds_equals(self, mock_model):
        mock_model = mock_model.return_value
        mock_model.predict.return_value = 0.3

        bad_thresholds = 0.3
        good_thresholds = 0.3

        result = predict_message_mood(
                    message="Пикник на обочине",
                    model=mock_model,
                    bad_thresholds=bad_thresholds,
                    good_thresholds=good_thresholds,
            )

        self.assertEqual(result, "норм")

    @mock.patch("predict_message_mood.SomeModel", autospec=True)
    def test_swap_thresholds(self, mock_model):
        mock_model = mock_model.return_value
        mock_model.predict.return_value = 0.3

        bad_thresholds = 0.8
        good_thresholds = 0.3

        with self.assertRaises(ThresholdsError):
            predict_message_mood(
                message="Пикник на обочине",
                model=mock_model,
                bad_thresholds=bad_thresholds,
                good_thresholds=good_thresholds,
            )


if __name__ == "__main__":
    unittest.main()
