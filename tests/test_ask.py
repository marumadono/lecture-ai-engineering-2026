"""対話スクリプトのテスト（LLMもAPIキーも使わない）。"""

import sys

import app.ask as ask_module


def test_main_sends_conversation_history(monkeypatch, capsys):
    inputs = iter(["次の質問", "  QuIt  "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(sys, "argv", ["app.ask", "最初の質問"])
    requests = []

    def fake_ask(history):
        requests.append([(message.role, message.parts[0].text) for message in history])
        return f"回答: {history[-1].parts[0].text}"

    monkeypatch.setattr(ask_module, "ask", fake_ask)

    ask_module.main()

    assert requests == [
        [("user", "最初の質問")],
        [("user", "最初の質問"), ("model", "回答: 最初の質問"), ("user", "次の質問")],
    ]
    assert "回答: 次の質問" in capsys.readouterr().out


def test_main_skips_empty_input(monkeypatch, capsys):
    inputs = iter(["   ", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(sys, "argv", ["app.ask", "初回質問"])
    calls = []
    monkeypatch.setattr(ask_module, "ask", lambda history: calls.append(history) or "回答")

    ask_module.main()

    assert len(calls) == 1
    assert "質問を入力してください。" in capsys.readouterr().out


def test_main_continues_after_api_error(monkeypatch, capsys):
    class FakeAPIError(Exception):
        code = 503
        message = "busy"

    inputs = iter(["次の質問", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(sys, "argv", ["app.ask", "失敗する質問"])
    monkeypatch.setattr(ask_module.errors, "APIError", FakeAPIError)
    requests = []

    def fake_ask(history):
        requests.append([(message.role, message.parts[0].text) for message in history])
        if len(requests) == 1:
            raise FakeAPIError()
        return "回答"

    monkeypatch.setattr(ask_module, "ask", fake_ask)

    ask_module.main()

    assert requests == [[("user", "失敗する質問")], [("user", "次の質問")]]
    assert "モデルが混み合っています" in capsys.readouterr().out