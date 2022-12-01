from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto, Categoria, Opcoes, Adicional

def home(request):

    # Verifica se o essa variável carrinho existe, se não existir, ele entra no if e cria.
    if not request.session.get('carrinho'):
        request.session['carrinho'] = []
        request.session.save()

    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    
    return render(request, 'produto/home.html', {'produtos': produtos, 'carrinho': len(request.session['carrinho']), 'categorias': categorias})


def categoria(request, id):

    # Verifica se o essa variável carrinho existe, se não existir, ele entra no if e cria.
    if not request.session.get('carrinho'):
        request.session['carrinho'] = []
        request.session.save()

    produtos = Produto.objects.filter(categoria_id = id)
    categorias = Categoria.objects.all()

    return render(request, 'produto/home.html', {'produtos': produtos,
                                        'carrinho': len(request.session['carrinho']),
                                        'categorias': categorias,})


def produto(request, id):
    
    # Verifica se o essa variável carrinho existe, se não existir, ele entra no if e cria.
    if not request.session.get('carrinho'):
        request.session['carrinho'] = []
        request.session.save()

    erro = request.GET.get('erro')

    produto = Produto.objects.filter(id=id)[0]
    categorias = Categoria.objects.all()
    return render(request, 'produto/produto.html', {'produto': produto, 
                                            'carrinho': len(request.session['carrinho']),
                                            'categorias': categorias,
                                            'erro': erro})


def add_carrinho(request):

    if not request.session.get('carrinho'):
        request.session['carrinho'] = []
        request.session.save()

    requisicao = dict(request.POST)
    

    def remove_lixo(adicional):

        """Para remover as chaves que tem um padrão, e transformar em lista o que está dinâmico"""

        adicional = requisicao.copy()
        adicional.pop('csrfmiddlewaretoken')
        adicional.pop('id')
        adicional.pop('observacoes')
        adicional.pop('quantidade')
        adicional = list(adicional.items())
        return adicional

    adicionais = remove_lixo(requisicao)

    # Pega o id do produro #
    id = int(requisicao['id'][0])
    
    # Verifica quais são os adicionais que aquele determinado produto possui #
    adicionais_verifica = Adicional.objects.filter(produto=id)

    for chave in adicionais_verifica:
        minimo = chave.minimo
        maximo = chave.maximo

        for chave1 in adicionais:

            if chave1[1] == chave.nome:
                if len(chave1[1]) < minimo or len(1) > maximo:
                    return HttpResponse('valor errado de adicionais')


    # Para calcular o valor do acrecimo e da quantidade #

    preco_total = Produto.objects.filter(id=id)[0].preco

    for chave, valor in adicionais:
        for v in valor:
            opcoes = Opcoes.objects.filter(id=v)[0].acrecimo
            preco_total += opcoes

    quantidade = int(requisicao['quantidade'][0])
    preco_total *= quantidade

    # Trocar o id do valor do adicional para o nome #

    def troca_id_por_nome(adicional):

        nomes_adicionais = []

        for chave_valor in adicionais:
            opcoes = []
            for valor in chave_valor[1]:
                op = Opcoes.objects.filter(id=valor)[0].nome
                opcoes.append(op)
            nomes_adicionais.append((chave_valor[0], opcoes))

        return nomes_adicionais

    adicionais = troca_id_por_nome(adicionais)


    data = {'id_produto': int(requisicao['id'][0]),
            'observacoes': requisicao['observacoes'][0],
            'preco': preco_total,
            'adicionais': adicionais,
            'quantidade': requisicao['quantidade'][0]}

    request.session['carrinho'].append(data)
    request.session.save()
    # return HttpResponse(request.session['carrinho'])
    return redirect(f'/ver_carrinho')
    

def ver_carrinho(request):

    categorias = Categoria.objects.all()

    dados_mostrar = []

    for item in request.session['carrinho']:
        produto = Produto.objects.filter(id=item['id_produto'])
    
        dados_mostrar.append(
            {'imagem': produto[0].img.url,
            'nome': produto[0].nome_produto,
            'quantidade': item['quantidade'],
            'preco': f"R$ {item['preco']:.2f}",
            'id': item['id_produto'],}
            )

    # Primeira forma de fazer #
    # lista = []
    # for cada_preco in request.session['carrinho']:
        
    #     lista.append(float(cada_preco['preco']))

    # total_da_compra = sum(lista)
    

    # Segunda forma de fazer #
    total = sum([float(i['preco']) for i in request.session['carrinho']])
        


    return render(request, 'produto/ver_carrinho.html', {'dados': dados_mostrar,
                                             'total': f'{total:.2f}',
                                             'carrinho': len(request.session['carrinho']),
                                             'categorias': categorias,
                                             })


def remover_carrinho(request, id):

    request.session['carrinho'].pop(id)
    request.session.save()
    return redirect('/ver_carrinho')

