import pytest
import requests
from unittest.mock import patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import buscar_cotacao


def test_buscar_cotacao_valida():
    # Usando patch para simular a resposta da API
    mock_response = {"USDBRL": {"bid": "5.29"}}

    with patch("requests.get") as mock_get:
        # Simulando a resposta da API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Executando a função e verificando o valor retornado
        cotacao = buscar_cotacao()

        # Verificando se a cotação foi retornada corretamente
        assert cotacao == 5.29, f"Esperado 5.29, mas obteve {cotacao}"


def test_buscar_cotacao_erro_requisicao():
    # Simulando um erro de requisição (por exemplo, API fora do ar)
    with patch("requests.get") as mock_get:
        # Simulando um erro de rede (requisição falhou)
        mock_get.side_effect = requests.exceptions.RequestException("Erro de rede")

        # Executando a função e verificando se retorna None
        cotacao = buscar_cotacao()

        # Verificando que a cotação é None, pois houve erro
        assert cotacao is None, "Esperado None devido a erro de requisição"


def test_buscar_cotacao_erro_json():
    # Simulando uma resposta que não contém a chave esperada
    mock_response = {"USDBRL": {"bid": "invalid_value"}}

    with patch("requests.get") as mock_get:
        # Simulando a resposta da API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Executando a função e verificando se trata corretamente o valor inválido
        cotacao = buscar_cotacao()

        # Verificando que a cotação será None porque a conversão para float falhou
        assert cotacao is None, "Esperado None devido a erro de conversão de valor"


if __name__ == "__main__":
    pytest.main()
