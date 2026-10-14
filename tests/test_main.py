import logging
import unittest
from unittest.mock import MagicMock, patch

import main
from src.database import Database
from src.notifier import EmailSender
from src.triangle import Triangle
from src.user_interface import ConsoleUserInterface


def setUpModule():
    logging.disable(logging.CRITICAL)


def tearDownModule():
    logging.disable(logging.NOTSET)


class TestMain(unittest.TestCase):

    def test_build_controller_connects_all_real_classes(self):
        controller = main.build_controller(":memory:")

        self.assertIsInstance(controller.user_interface, ConsoleUserInterface)
        self.assertIsInstance(controller.database, Database)
        self.assertIsInstance(controller.calculator, Triangle)
        self.assertIsInstance(controller.sender, EmailSender)
        controller.database.close()

    @patch("main.logging.FileHandler")
    @patch("main.logging.basicConfig")
    @patch("main.os.makedirs")
    def test_logger_writes_to_console_and_file(self, fake_makedirs, fake_config, fake_file):
        main.configure_logging()

        fake_makedirs.assert_called_once_with("logs", exist_ok=True)
        self.assertEqual(len(fake_config.call_args.kwargs["handlers"]), 2)

    @patch("builtins.print")
    @patch("main.configure_logging")
    @patch("main.build_controller")
    def test_main_prints_result_of_scenario(self, fake_build, fake_logging, fake_print):
        fake_build.return_value = MagicMock(**{"run.return_value": "итог"})

        main.Main()

        fake_print.assert_called_once_with("итог")

    @patch("main.configure_logging")
    @patch("main.build_controller", side_effect=RuntimeError("БД недоступна"))
    def test_main_does_not_crash_on_error(self, fake_build, fake_logging):
        main.Main()

        fake_build.assert_called_once()


if __name__ == "__main__":
    unittest.main()
