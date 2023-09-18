import unittest
from unittest.mock import patch

from predict_message_mood import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    @patch('predict_message_mood.SomeModel', autospec=True)
    def test_normal_cond(self, mock_model):
        mock_model = mock_model.return_value
        mock_model.predict.side_effect = [0.2, 0.4, 0.9]

        bad_thresholds = 0.3
        good_thresholds = 0.8

        result1 = predict_message_mood(message='Чапаев и Пустота',
                                       model=mock_model,
                                       bad_thresholds=bad_thresholds,
                                       good_thresholds=good_thresholds)

        result2 = predict_message_mood(message='Generation П',
                                       model=mock_model,
                                       bad_thresholds=bad_thresholds,
                                       good_thresholds=good_thresholds)

        result3 = predict_message_mood(message='Голубое сало',
                                       model=mock_model,
                                       bad_thresholds=bad_thresholds,
                                       good_thresholds=good_thresholds)

        self.assertEqual(result1, 'неуд')
        self.assertEqual(result2, 'норм')
        self.assertEqual(result3, 'отл')

    def test_edge_cond(self):
        pass

    def test_thresholds_equals(self):
        pass

    def test_swap_thresholds(self):
        pass


if __name__ == "__main__":
    unittest.main()
