# apps/ads/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ad(models.Model):
    """
    Объявление о товаре для обмена.
    """
    class Condition(models.TextChoices):
        NEW = "new", "Новый"
        USED = "used", "Б/у"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="Автор",
    )
    title = models.CharField("Заголовок", max_length=120)
    description = models.TextField("Описание")
    image_url = models.URLField("URL изображения", blank=True)
    category = models.CharField("Категория", max_length=60)
    condition = models.CharField(
        "Состояние",
        max_length=4,
        choices=Condition.choices,
    )
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "объявление"
        verbose_name_plural = "объявления"

    def __str__(self) -> str:
        return self.title


class ExchangeProposal(models.Model):
    """
    Предложение обмена одного объявления на другое.
    """
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        ACCEPTED = "accepted", "Принята"
        DECLINED = "declined", "Отклонена"

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="sent_proposals",
        verbose_name="Отправитель (объявление)",
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="received_proposals",
        verbose_name="Получатель (объявление)",
    )
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField(
        "Статус",
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField("Дата предложения", auto_now_add=True)

    class Meta:
        verbose_name = "предложение обмена"
        verbose_name_plural = "предложения обмена"
        constraints = [
            # Нельзя предложить обмен самому себе
            models.CheckConstraint(
                check=~models.Q(ad_sender=models.F("ad_receiver")),
                name="no_self_exchange",
            ),
            # Единственное активное (pending) предложение между парой объявлений
            models.UniqueConstraint(
                fields=["ad_sender", "ad_receiver"],
                condition=models.Q(status="pending"),
                name="unique_pending_pair",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.ad_sender} ↔ {self.ad_receiver} ({self.get_status_display()})"