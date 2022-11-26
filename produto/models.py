from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe


class Categoria(models.Model):

    categoria = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self) -> str:
        return self.categoria


class Opcoes(models.Model):

    nome = models.CharField(max_length=100)
    acrecimo = models.FloatField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Opções'

    def __str__(self) -> str:
        return self.nome


class Adicional(models.Model):

    nome = models.CharField(max_length=100, unique=True)
    maximo = models.IntegerField()
    minimo = models.IntegerField()
    opcoes = models.ManyToManyField(Opcoes)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Adicionais'

    def __str__(self) -> str:
        return self.nome


class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    img = models.ImageField(upload_to='post_img')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    preco = models.FloatField()
    descricao = models.TextField()
    ingredientes = models.CharField(max_length=2000)
    adicionais = models.ManyToManyField(Adicional, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Produtos'


    @mark_safe
    def icone(self):
        return f'<img src="/media/{self.img}" width="30px">'


    def __str__(self) -> str:
        return self.nome_produto

















