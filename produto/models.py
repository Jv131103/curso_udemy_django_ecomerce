import os

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image

# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to="produto_imagens/%Y/%m/", blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(default=0, verbose_name="preco")
    preco_marketing_promocional = models.FloatField(
        default=0, verbose_name="preco_promocao"
    )
    tipo = models.CharField(
        default="V",
        max_length=1,
        choices=(
            ("V", "Variável"),
            ("S", "Simples"),
        )
    )

    def __str__(self) -> str:
        return self.nome

    def get_preco_formatado(self):
        return f"R$ {self.preco_marketing:.2f}".replace(".", ",")
    get_preco_formatado.short_description = "PREÇO"

    def get_preco_promo_formatado(self):
        return f"R$ {self.preco_marketing_promocional:.2f}".replace(".", ",")
    get_preco_promo_formatado.short_description = "PREÇO PROMOSSIONAL"

    @staticmethod
    def resize_image(original_img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, original_img.name)
        img_pil = Image.open(img_full_path)

        original_width, original_height = img_pil.size
        new_height = round((new_width * original_height) / original_width)

        if new_width >= original_width:
            img_pil.close()
            return

        nova_imagem = img_pil.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )
        nova_imagem.save(img_full_path, optimize=True, quality=60)
        img_pil.close()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f"{slugify(self.nome)}"
            self.slug = slug

        super().save(*args, **kwargs)

        img_max_width = 800

        if self.imagem:
            self.resize_image(self.imagem, img_max_width)


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField(default=0)
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name or self.produto.nome

    class Meta:
        verbose_name = "Variação"
        verbose_name_plural = "Variações"
