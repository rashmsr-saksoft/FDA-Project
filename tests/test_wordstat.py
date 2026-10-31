import pytest

from wordstat.cli import count_words, main


def test_count_words():
    result = count_words("Python is easy. Python is useful.")

    assert result["python"] == 2
    assert result["is"] == 2
    assert result["easy"] == 1
    assert result["useful"] == 1


def test_count_words_ignores_case():
    result = count_words("Python PYTHON python")

    assert result["python"] == 3


def test_count_words_ignores_punctuation():
    result = count_words("Hello, world! Hello.")

    assert result["hello"] == 2
    assert result["world"] == 1


def test_empty_text():
    result = count_words("")

    assert result == {}


def test_unicode_words():
    result = count_words("café naïve")

    assert result["café"] == 1
    assert result["naïve"] == 1


def test_very_long_line():
    text = "python " * 10000
    result = count_words(text)

    assert result["python"] == 10000


def test_cli_displays_top_words(tmp_path, monkeypatch, capsys):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("apple banana apple orange", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["wordstat", str(sample_file), "-n", "2"],
    )
    main()
    output = capsys.readouterr()
    assert output.out == "apple: 2\nbanana: 1\n"


def test_cli_missing_file(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["wordstat", "missing.txt"],
    )

    with pytest.raises(SystemExit) as error:
        main()

    output = capsys.readouterr()

    assert error.value.code == 1
    assert "File not found" in output.err
