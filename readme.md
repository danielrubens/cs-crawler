# Dia prático de crawlers

Este exercício consiste no desenvolvimento de um crawler, que acessa websites de e-commerce em busca de um conjunto de produtos e ordena os resultados obtidos pelo menor preço.

Esse repositório possui testes automatizados, mas não tem finalidade avaliativa como o avaliador de projetos da Trybe. Aproveite esse momento para aprender e se divertir!

## Antes de começar

O crawler foi construído, testado e _mockado_ com base nos sites [Magalu](https://www.magazineluiza.com.br) e [Pichau](https://www.pichau.com.br) em meados de dezembro de 2022.

> ⚠️ Os sites podem mudar sua estrutura de tags e classes, nesse caso, o presente código deixará de funcionar na prática, passando a funcionar somente nos testes. Nesse caso, informe o time de currículo para que os devidos ajustes sejam feitos. ⚠️
>
> ⚠️ Executar o crawler muitas vezes pode gerar um bloqueio temporário do seu IP em um ou mais sites, fazendo com que as buscas deixem de funcionar corretamente, portanto execute somente quando preciso. ⚠️

Os testes realizam um mock da requisição, portanto ao utilizar o método `requests.get`, uma chamada a um arquivo local será feita.

Com isso, o `pytest` poderá ser chamado quantas vezes forem necessárias, uma vez que as requisições não serão feitas ao site real, mas sim ao arquivo de mock correspondente.

## Ferramentas para o desenvolvimento

A biblioteca utilizada e recomendada para o desenvolvimento deste exercício é a `BeautifulSoup4`. Não existindo um gabarito que faça uso de outras bibliotecas como `Parsel`, `Scrapy` ou similar.

Além disso, como o mock das requisições é feito diretamente no método `get` da biblioteca `requests`, utilizar uma biblioteca diferente para as requisições HTTP exigirão alterações nos arquivos de teste.

### Arquitetura

O presente crawler é disposto na seguinte arquitetura:

- Uma classe de dados que representa um produto (em [`product.py`](src/product.py))
- Uma classe abstrata que representa um website (em [`website.py`](src/websites/website.py))
- Outras classes concretas de websites, na concepção dos sites Pichau e Magalu (em [`websites`](src/websites/))
- Funções auxiliares para realizar as consultas, por meio de multithreading (em [`aggregator.py`](src/aggregator.py))
- Uma pequena [CLI](https://pt.wikipedia.org/wiki/Interface_de_linha_de_comandos) para interagir com o sistema (em [`__main__.py`](src/__main__.py))
- Diversos testes, em especial para as classes concretas
- Alguns outros arquivos utilitários e complementares

### Executando

1. Crie o ambiente virtual para o projeto

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

2. Instale as dependências

   ```bash
   python3 -m pip install -r dev-requirements.`txt`
   ```

3. Execute os testes:

   ```bash
   python3 -m pytest
   ```

4. Execute a interface com linha comando (presente no arquivo `src/__main__.py`):

   ```bash
   python3 -m src
   ```

## Sobre a atividade prática

A atividade prática possui 2 objetivos:``

   1. melhorar a compreensão do uso prático da Orientação a Objetos em um projeto aplicado;
   2. aplicar os conhecimentos de web scrapping em um projeto simples, apenas para fins de exercício.

### 1 - Compreenda a arquitetura de classes do projeto

- Leia atentamente a definição dos atributos e métodos das classes [`Product`](src/product.py) e [`Website`](src/websites/website.py). Além disso, explore os métodos abstratos presentes na classe `Website`.

- Leia os comentários do arquivo de testes [`test_get_product_price.py`](tests/websites/test_get_product_price.py). Os comentários explicam a dinâmica do `pytest`, foque no que diz respeito ao uso da classe `Website` e das classes concretas `Magalu` e `Pichau`.

### 2 - Implemente a raspagem dos sites Magalu e Pichau

- Implemente as classes concretas `Magalu` e/ou `Pichau`, de forma a conseguir os dados dos sites. Você precisará herdar de `Website` e implementar os métodos abstratos definidos. Para isso, se oriente através das **_DocStrings_** (documentação como comentários nos métodos) e das **_Type Hints_** (indicativos de tipagem de parâmetros e retornos dos métodos).

> ⚠️ **Atenção**: O site real pode estar diferente dos mocks. É recomendável tomar como base os HTMLs presentes na [pasta de mocks dos testes](tests/websites/mocks/).
>
> Lá, os arquivos terminados em "full.html" são as páginas de busca completas, enquanto que os outros são o HTML de itens em específico.

### Dicas

Caso esteja difícil realizar os desafios, confira aqui algumas dicas que podem te ajudar no processo.

<details>
   <summary>headers</summary>

   Lembre-se de mandar um header de `user-agent` customizado na sua requisição, caso contrário, você pode ter o acesso ao site recusado.
   Faça uma requisição normal pelo seu navegador de internet, copie o header de `user-agent` nas ferramentas de desenvolvedor do navegador e cole nos headers da requisição.
</details>

<details>
   <summary><code>_get_product_price</code> dica genérica 1</summary>

   Use o regex `PRICE_REGEX`, em [utils](src/utils.py), especificamente seu método `PRICE_REGEX.search(string_onde_será_pesquisado_o_preço).group(0)` para pesquisar se uma string dá match com um preço. Você pode ter que verificar se o retorno é diferente de `None` antes de usar `.group(0)`.
</details>

<details>
   <summary><code>_get_product_price</code> dica genérica 2</summary>

   Após o uso da regex, verifique a presença de pontos e vírgulas nas strings de preço, substituindo os incorretos pelo padrão americano (pontos para separar centavos) para só então passar para a função `float(string_numérica)`.
</details>

<details>
   <summary><code>_get_product_url</code></summary>

   As urls estão dentro do atributo `href` da primeira tag `a`. Você pode ter que verificar se o atributo retorna uma string ou uma lista de strings para satisfazer o verificador de tipagem.
</details>

#### Magalu

<details>
   <summary><code>_get_search_page_with_search_results</code></summary>

   A página de buscas funciona passando o _termo de busca_ em `/busca/termo+de+busca`, transformando espaços em sinais de mais.
</details>

<details>
   <summary><code>_get_products_html</code></summary>

   Os produtos estão dentro de uma tag `li` que possuem as classes `sc-fCBrnK hYPKVt`.
</details>

<details>
   <summary><code>_get_product_price</code></summary>

   Os preços estão dentro de uma tag `p`, com o atributo `data-testid` com o valor `price-value`.
</details>

<details>
   <summary><code>_get_product_name</code></summary>

   Os nomes estão dentro de uma tag `h2`, com o atributo `data-testid` com o valor `product-title`.
</details>

#### Pichau

<details>
   <summary><code>_get_search_page_with_search_results</code></summary>

   A página de buscas funciona passando o termo de busca como valor do parâmetro `q` da requisição.
</details>

<details>
   <summary><code>_get_products_html</code></summary>

   Os produtos estão dentro de uma tag `a`, com o atributo `data-cy` com o valor `list-product`.
</details>

<details>
   <summary><code>_get_product_price</code></summary>

   Os preços estão dentro de uma tag `div`, com o atributo `class` com o valor `jss83`.
</details>

<details>
   <summary><code>_get_product_name</code></summary>

   Os nomes estão dentro de uma tag `h2`.
</details>

## Depois de tentar

Caso queira ir além, após o momento prático você pode tentar adicionar um novo website ao projeto: basta criar uma classe que herde de `Website` e respeite sua interface. Adicione essa classe na lista de classes utilizadas em [`src/websites/__init__.py`](src/websites/__init__.py) para que ela funcione em sua CLI, e verá o poder da Orientação a Objetos.
Os testes, caso queira criar, também são simples: basta adicionar novos valores para as parametrizações existentes nas funções já criadas.
