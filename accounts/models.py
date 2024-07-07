from django.db import models


class Account(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} : {self.email}'

    class Meta:
        db_table = 'accounts_accounts'  # 여기서 테이블 이름을 변경
