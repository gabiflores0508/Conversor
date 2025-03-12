import pytest
from fucntion.cotacao import buscar_cotacao, converter_valor


@pytest.fixture
def mock_cotacao():
    return 5.0  # Simula uma cotação do dólar


def test_buscar_cotacao(monkeypatch):
    """Testa se a função buscar_cotacao retorna um valor válido"""

    class MockResponse:
        @staticmethod
        def json():
            return {"USDBRL": {"bid": "5.25"}}

        def raise_for_status(self):
            pass

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    cotacao = buscar_cotacao()
    assert cotacao == 5.25


def test_converter_valor(mock_cotacao):
    """Testa conversões corretas"""
    assert converter_valor(10, mock_cotacao) == 2.0
    assert converter_valor(50, mock_cotacao) == 10.0
    assert converter_valor(0, mock_cotacao) is None  # Testa valor zero
    assert converter_valor(-5, mock_cotacao) is None  # Testa valor negativo
    assert converter_valor(10, None) is None  # Testa cotação inválida
