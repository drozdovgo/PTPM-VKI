import unittest
import os
from unittest.mock import patch, Mock
from src.parser import ProductParser
from src.database import DatabaseRepository

class TestProductParser(unittest.TestCase):
    def setUp(self):
        self.parser = ProductParser()
        self.repo = DatabaseRepository(':memory:')
        self.fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'opt_products.html')
        with open(self.fixture_path, 'r', encoding='utf-8') as f:
            self.sample_html = f.read()

    def tearDown(self):
        self.repo.close()

    def test_parse_html_extracts_products_correctly(self):
        data = self.parser.parse_html(self.sample_html)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['name'], 'ANTILOPA')
        self.assertIn('AL16091 роз. Ботинки деми дев', data[0]['message'])
        self.assertIn('1 695 руб.', data[0]['message'])
        self.assertEqual(data[2]['name'], 'Неизвестный бренд')
        self.assertIn('Сумка женская', data[2]['message'])

    @patch('src.parser.requests.get')
    def test_parse_page_network_mock(self, mock_get):
        mock_response = Mock()
        mock_response.text = self.sample_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        data = self.parser.parse_page("https://opt-opt-opt.ru/catalog/")

        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args.kwargs
        self.assertIn('User-Agent', call_kwargs['headers'])
        self.assertEqual(len(data), 3)
        self.assertEqual(data[1]['name'], 'KUMFO')

    def test_save_to_db_integration(self):
        data = self.parser.parse_html(self.sample_html)
        self.parser.save_to_db(data, self.repo)
        db_record = self.repo.get_by_id(1)
        self.assertIsNotNone(db_record)
        self.assertEqual(db_record['name'], 'ANTILOPA')
        self.assertIn('1 695 руб.', db_record['message'])


if __name__ == '__main__':
    unittest.main()