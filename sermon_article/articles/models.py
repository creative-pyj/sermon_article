from django.db import models
import secrets

# 16桁のランダムなIDを生成する関数 (SQLの hex(randomblob(8)) 相当)
def generate_id():
    return secrets.token_hex(8)

class Member(models.Model):
    """
    教会員・スタッフ管理テーブル
    """
    GENDER_CHOICES = [
        ('male', '男性'),
        ('female', '女性'),
        ('other', 'その他'),
    ]

    ROLE_CHOICES = [
        ('pastor', '牧師'),
        ('evangelist', '伝道師'),
        ('elder', '長老'),
        ('deacon', '執事'),
        ('staff', 'スタッフ'),
        ('volunteer', 'ボランティア'),
    ]

    # idはDjangoが自動でAutoFieldを作成するため省略可能ですが、
    # SQL定義に合わせて明示する場合は以下のように書きます。
    # id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100, verbose_name="氏名")
    kana = models.CharField(max_length=100, blank=True, null=True, verbose_name="カナ")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="性別")
    
    # 画像はImageField推奨（Pillowライブラリが必要）。
    # 文字列(パス)だけでよいなら CharField(max_length=255) に変更してください。
    image = models.ImageField(upload_to='members/', blank=True, null=True, verbose_name="写真")
    
    birth_date = models.DateField(blank=True, null=True, verbose_name="生年月日")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="役割")
    join_date = models.DateField(blank=True, null=True, verbose_name="入会日")
    baptism_date = models.DateField(blank=True, null=True, verbose_name="洗礼日")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号")
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    address = models.TextField(blank=True, null=True, verbose_name="住所")
    notes = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'members' # テーブル名を指定
        verbose_name = 'メンバー'
        verbose_name_plural = 'メンバー'

    def __str__(self):
        return self.name


class SermonArticle(models.Model):
    """
    説教・記事管理テーブル
    """
    # 16文字のランダムID
    id = models.CharField(
        primary_key=True,
        max_length=16,
        default=generate_id,
        editable=False
    )
    
    # Memberへの外部キー (db_column='member_id'とすることでDB上はmember_idカラムになります)
    # on_delete=models.SET_NULL: メンバーが削除されても記事は残る（著者が空になる）設定
    member = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='member_id',
        verbose_name="説教者/著者"
    )

    content_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="タイトル")
    content_summary = models.TextField(blank=True, null=True, verbose_name="要約")
    content_scripture = models.TextField(blank=True, null=True, verbose_name="聖書箇所")
    content_sermon_original = models.TextField(blank=True, null=True, verbose_name="原文")
    content_sermon_translate = models.TextField(blank=True, null=True, verbose_name="翻訳")
    content_tips = models.TextField(blank=True, null=True, verbose_name="Tips")
    language = models.CharField(max_length=2, blank=True, null=True, verbose_name="言語")
    
    sermon_at = models.DateTimeField(verbose_name="説教日時")
    
    # auto_now: 更新のたびに日時更新 / auto_now_add: 作成時のみ日時設定
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    class Meta:
        db_table = 'sermon_article'
        verbose_name = '説教記事'
        verbose_name_plural = '説教記事'

    def __str__(self):
        return self.content_title or self.id