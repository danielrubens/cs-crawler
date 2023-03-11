from typing import Dict, NamedTuple, Type

import pytest

from src.websites import Magalu, Pichau, Website

# * A única função de testes do arquivo é a `test_get_product_price_okay`
# * É uma função de teste parametrizada, ou seja, a mesma função roda mais de
# * uma vez para cada parâmetro, contando como se fosse um teste a cada vez
# * que roda. Neste exemplo, ela roda 4 testes, pois são 4 parâmetros.


# ? Classe auxiliar para guardar as informações que um teste precisa para rodar
class ProductInfo(NamedTuple):
    # ? Classe do website a ser testado. Observe que a tipagem diz que
    # ? esperamos uma classe, e não uma instância. Observe também que esperamos
    # ? uma classe de Website, que pode ser Pichau ou Magalu ou qualquer outra
    # ? classe que herde de Website ou que seja sua descendente.
    website_class: Type[Website]

    # ? Termo de busca a ser pesquisado
    search_term: str

    # ? Preço esperado como retorno da busca
    expected_product_price: float

    # ? Função utilitária no formato de atributo para retornar o nome da classe
    # ? Vai ser utilizada para identificar o teste, visto que ele é
    # ? parametrizado
    @property
    def company_name(self):
        return self.website_class.__name__.lower()


# ? Lista de parâmetros de parametrização. O teste vai rodar uma vez para cada
# ? um destes parâmetros
PARAMS = [
    ProductInfo(Magalu, "i5 11400f", 1_235.28),
    ProductInfo(Magalu, "rtx 3080", 5_499.00),
    ProductInfo(Pichau, "i9 12900ks", 4_449.98),
    ProductInfo(Pichau, "rtx 3080", 6_699.99),
]


# ? Função auxiliar que cria o identificador das execuções parametrizadas
# ? Assim as funções vão aparecer nos resultados dos testes assim:
# test_get_product_price_okay[magalu - i5 11400f]
# test_get_product_price_okay[magalu - rtx 3080]
# test_get_product_price_okay[pichau - i9 12900ks]
# test_get_product_price_okay[pichau - rtx 3080]
def id_function(value: ProductInfo):
    return f"{value.company_name} - {value.search_term}"


# * Função de teste
# ? O parametrize cria vários testes, um para cada elemento da lista PARAMS,
# ? passando esse elemento para o parâmetro `product` da função de teste.
# ? `content` é uma fixture definida em conftest.py, que basicamente coloca os
# ? conteúdos dos arquivos de mock do diretório de mocks dentro de um
# ? dicionário, para acesso conveniente pelas funções de teste
@pytest.mark.parametrize("product", PARAMS, ids=id_function)
def test_get_product_price_okay(content: Dict[str, str], product: ProductInfo):
    # Cria uma instância da classe concreta, seja ela Magalu ou Pichau
    website = product.website_class()

    # Pega o html do mock no dicionário content
    # Se não encontrar nada no dicionário, retorna uma string vazia, o que
    # deve fazer o teste quebrar
    file_name = f"{product.company_name} - {product.search_term}.html"
    html = content.get(file_name, "")

    # Passa o HTML do mock para o método que está sendo testado
    result = website._get_product_price(html)

    # Verifica se o resultado é o esperado
    assert result == product.expected_product_price
