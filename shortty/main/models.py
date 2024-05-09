from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    username = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # 외래 키로 Category 모델을 참조하여 각 메시지가 카테고리에 속하게 함
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"{self.username}: {self.message[:20]}... ({self.timestamp})"
