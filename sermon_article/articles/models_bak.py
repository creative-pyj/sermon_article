from django.db import models

def generate_random_id():
    import secrets
    return secrets.token_hex(8)

class members(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.TextField(blank=True, max_length=20, verbose_name='姓名')
    kana = models.TextField(blank=True, max_length=20, verbose_name='姓名（カナ）')
    gender = models.TextField(blank=True, verbose_name='性别（male,female）')
    image = models.TextField(blank=True, verbose_name='头像图片')
    birth_date = models.TextField(blank=True, verbose_name='出生年月日')
    role = models.TextField(blank=True, verbose_name='担当职务')
    join_date = models.TextField(blank=True, verbose_name='加入日期')
    baptism_date = models.TextField(blank=True, verbose_name='洗礼日期')
    phone = models.TextField(blank=True, verbose_name='电话号码')
    email = models.TextField(blank=True, verbose_name='电子邮件')
    address = models.TextField(blank=True, verbose_name='住所')
    notes = models.TextField(blank=True, verbose_name='備考 ')

    class Meta:
        verbose_name = '成员'
        verbose_name_plural = '成员'
        managed = False
        db_table = 'members'

    def __str__(self):
        return self.name

class sermon_article(models.Model):
    id = models.CharField(primary_key=True, max_length=16, default=generate_random_id, editable=False)
    language = models.CharField(max_length=10, default='zh', verbose_name='语言')
    content_title = models.CharField(max_length=200, verbose_name='说教标题')
    content_summary = models.TextField(blank=True, verbose_name='内容摘要')
    content_scripture = models.TextField(blank=True, verbose_name='经文引用')
    content_sermon_original = models.TextField(blank=True, verbose_name='说教原文')
    content_sermon_translate = models.TextField(blank=True, verbose_name='说教译文')
    content_tips = models.TextField(blank=True, verbose_name='补充说明')
    sermon_at = models.DateTimeField(verbose_name='说教日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '说教文章'
        verbose_name_plural = '说教文章'
        managed = False
        db_table = 'sermon_article'

    def __str__(self):
        return self.content_title