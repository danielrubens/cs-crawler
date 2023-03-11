from .aggregator import get_many_products_from_many_sites


def main():
    search_term = input("Digite o termo de busca: ")
    quantity = int(input("Digite quantos itens você quer buscar: "))
    products = get_many_products_from_many_sites(search_term, quantity)

    if not products:
        print("Nenhum produto encontrado")
        return

    for product in sorted(products, key=lambda prod: prod.price):
        print(f"{product.name = }\n{product.price = }\n{product.url = }\n")


main()
