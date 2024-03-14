import pytest
import os

from tempfile import TemporaryDirectory
from click.testing import CliRunner

from ghost_writer.cli import cli


def test_config_command(monkeypatch):
    runner = CliRunner()

    # Mock user input
    monkeypatch.setattr("click.prompt", lambda *args, **kwargs: "Python, JavaScript")
    monkeypatch.setattr("click.confirm", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "click.edit",
        lambda *args, **kwargs: '# Example test case for the sum function\ndef test_sum():\n    assert sum([1, 2, 3]) == 6, "Should be 6"',
    )

    with TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = runner.invoke(cli, ["--config"])
        assert result.exit_code == 0

        # Check if the prompt file was created
        prompt_file = os.path.join(temp_dir, ".ghost", "default_prompt.txt")
        assert os.path.isfile(prompt_file)
