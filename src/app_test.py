import unittest
from unittest.mock import MagicMock, patch, call
from watchdog.events import FileCreatedEvent
from app import DirectoryCreationHandler


class TestDirectoryCreationHandler(unittest.TestCase):
    @patch("shutil.copytree")
    def test_on_created_directory_event(self, mock_copytree):
        # Arrange
        destination = "/mock_destination"
        handler = DirectoryCreationHandler(destination, debug=True)
        mock_event = MagicMock()
        mock_event.is_directory = True
        mock_event.src_path = "/mock_source/new_directory"

        # Act
        with patch("app.logger") as mock_logger:
            handler.on_created(mock_event)

        # Assert
        mock_copytree.assert_called_once_with(
            "/mock_source/new_directory", "/mock_destination/new_directory"
        )
        mock_logger.info.assert_has_calls(
            [
                call("New directory created: /mock_source/new_directory"),
                call("Copied /mock_source/new_directory to /mock_destination/new_directory"),
            ]
        )

    @patch("shutil.copytree")
    def test_on_created_directory_event_copy_failure(self, mock_copytree):
        # Arrange
        destination = "/mock_destination"
        handler = DirectoryCreationHandler(destination, debug=True)
        mock_event = MagicMock()
        mock_event.is_directory = True
        mock_event.src_path = "/mock_source/new_directory"
        mock_copytree.side_effect = Exception("Copy failed")

        # Act
        with patch("app.logger") as mock_logger:
            handler.on_created(mock_event)

        # Assert
        mock_copytree.assert_called_once_with(
            "/mock_source/new_directory", "/mock_destination/new_directory"
        )
        mock_logger.error.assert_called_once_with(
            "Failed to copy /mock_source/new_directory to /mock_destination/new_directory: Copy failed"
        )

    def test_on_created_non_directory_event(self):
        # Arrange
        destination = "/mock_destination"
        handler = DirectoryCreationHandler(destination, debug=True)
        mock_event = MagicMock()
        mock_event.is_directory = False
        mock_event.src_path = "/mock_source/new_file.txt"

        # Act
        with patch("app.logger") as mock_logger:
            handler.on_created(mock_event)

        # Assert
        mock_logger.info.assert_not_called()


if __name__ == "__main__":
    unittest.main()
