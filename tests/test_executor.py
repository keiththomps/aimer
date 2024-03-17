import os
from io import StringIO
from tempfile import NamedTemporaryFile

import pytest

from aimer.executor import DeleteFile, UpdateFile, Inquire, Executor


def test_delete_file():
    with NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name

    func_call = DeleteFile(file_path)
    func_call()
    assert not os.path.exists(file_path)


def test_update_file():
    with NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name

    contents = "Hello, World!"
    func_call = UpdateFile(file_path, contents)
    func_call()

    with open(file_path, "r") as file:
        assert file.read() == contents

    os.remove(file_path)


def test_inquire():
    with NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.write(b"Hello, World!")
        temp_file.close()

    func_call = Inquire(file_path)
    result = func_call()
    assert result == {"file_path": file_path, "contents": "Hello, World!"}

    os.remove(file_path)


def test_inquire_non_existent_file():
    file_path = "non_existent_file.txt"
    func_call = Inquire(file_path)
    result = func_call()
    assert result == {"file_path": file_path, "contents": ""}


def test_executor():
    with NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.write(b"Initial contents")
        temp_file.close()

    function_calls = [
        {"name": "inquire", "kwargs": {"file_path": file_path}},
        {
            "name": "updateFile",
            "kwargs": {"file_path": file_path, "contents": "New contents"},
        },
        {"name": "inquire", "kwargs": {"file_path": file_path}},
        {"name": "deleteFile", "kwargs": {"file_path": file_path}},
    ]

    executor = Executor(function_calls)
    results = executor.execute(confirm=False)

    assert results[0] == {"file_path": file_path, "contents": "Initial contents"}
    assert results[1] is None
    assert results[2] == {"file_path": file_path, "contents": "New contents"}
    assert results[3] is None
    assert not os.path.exists(file_path)


@pytest.fixture
def mock_stdin(monkeypatch):
    stdin_mock = StringIO()
    monkeypatch.setattr("sys.stdin", stdin_mock)
    return stdin_mock


def test_execute_without_confirm(mock_stdin, capsys):
    function_calls = [
        {"name": "deleteFile", "kwargs": {"file_path": "/path/to/file.txt"}}
    ]
    executor = Executor(function_calls)

    executor.execute(confirm=False)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_execute_with_confirm(mock_stdin, capsys):
    function_calls = [
        {"name": "deleteFile", "kwargs": {"file_path": "/path/to/file.txt"}},
        {
            "name": "updateFile",
            "kwargs": {"file_path": "/path/to/file.txt", "contents": "Hello, World!"},
        },
        {"name": "inquire", "kwargs": {"file_path": "/path/to/file.txt"}},
    ]
    executor = Executor(function_calls)

    mock_stdin.write("y\ny\nn\n")
    mock_stdin.seek(0)
    executor.execute(confirm=True)
    captured = capsys.readouterr()
    assert "Delete file: /path/to/file.txt" in captured.out
    assert "Do you want to continue? (y/n) " in captured.out
    assert (
        "Update file '/path/to/file.txt' with contents: Hello, World!" in captured.out
    )
    assert "Do you want to continue? (y/n) " in captured.out
    assert "Inquire contents of file: /path/to/file.txt" in captured.out
    assert "Do you want to continue? (y/n) " in captured.out
    assert "Skipping this function call." in captured.out
