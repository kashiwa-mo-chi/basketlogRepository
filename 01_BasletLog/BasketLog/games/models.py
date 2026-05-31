from django.db import models
from django.conf import settings

class Diary(models.Model):
    ARENA_CHOICES = [
        (1,'北海きたえーる'),
        (2,'ゼビオアリーナ仙台'),
        (3,'CNAアリーナ★あきた'),
        (4,'アダストリアみとアリーナ'),
        (5,'ブレックスアリーナ宇都宮'),
        (6,'OPEN HOUSE ARENA OTA'),
        (7,'越谷市立総合体育館'),
        (8,'LaLa arena TOKYO-BAY'),
        (9,'千葉ポートアリーナ'),
        (10,'TOYOTA ARENA TOKYO'),
        (11,'青山学院記念館'),
        (12,'東急ドレッセとどろきアリーナ'),
        (13,'横浜国際プール'),
        (14,'富山市総合体育館'),
        (15,'豊橋市総合体育館'),
        (16,'ウィングアリーナ刈谷'),
        (17,'名古屋市枇杷島スポーツセンター'),
        (18,'IGアリーナ'),
        (19,'滋賀ダイハツアリーナ'),
        (20,'にっしんでんきアリーナ京都'),
        (21,'おおきにアリーナ舞洲'),
        (22,'松江市総合体育館'),
        (23,'広島サンプラザホール'),
        (24,'SAGAアリーナ'),
        (25,'HAPPINESS ARENA'),
        (26,'沖縄サントリーアリーナ'),        
    ]

    TEAM_CHOICES = [
        (1,'レバンガ北海道'),
        (2,'仙台８９ERS'),
        (3,'秋田ノーザンハピネッツ'),
        (4,'茨城ロボッツ'),
        (5,'宇都宮ブレックス'),
        (6,'群馬クレインサンダーズ'),
        (7,'越谷アルファーズ'),
        (8,'アルティーリ千葉'),
        (9,'千葉ジェッツ'),
        (10,'アルバルク東京'),
        (11,'サンロッカーズ渋谷'),
        (12,'川崎ブレイブサンダース'),
        (13,'横浜ビー・コルセアーズ'),
        (14,'富山グラウジーズ'),
        (15,'三遠ネオフェニックス'),
        (16,'シーホース三河'),
        (17,'ファイティングイーグルス名古屋'),
        (18,'名古屋ダイヤモンドドルフィンズ'),
        (19,'滋賀レイクス'),
        (20,'京都ハンナリーズ'),
        (21,'大阪エヴェッサ'),
        (22,'島根スサノオマジック'),
        (23,'広島ドラゴンフライズ'),
        (24,'佐賀バルーナーズ'),
        (25,'長崎ヴェルカ'),
        (26,'琉球ゴールデンキングス'),
    ]

    VISIBILITY_CHOICES = [
        (1,'公開'),
        (2,'非公開'),
    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="投稿者",
    )
    arena_name = models.IntegerField(
        choices=ARENA_CHOICES,
        default=1,
        verbose_name="会場",
    )
    home_team_name = models.IntegerField(
        choices=TEAM_CHOICES,
        default=1,
        verbose_name="ホームチーム名",
    )
    away_team_name = models.IntegerField(
        choices=TEAM_CHOICES,
        default=2,
        verbose_name="アウェイチーム名",
    )
    status = models.IntegerField(
        choices=VISIBILITY_CHOICES,
        default=1,
        verbose_name="公開範囲",
    )        

    watch_date = models.DateField(verbose_name="観戦日")
    home_team_score = models.IntegerField(verbose_name="ホームチーム得点")
    away_team_score = models.IntegerField(verbose_name="アウェイチーム得点")
    memory = models.TextField(verbose_name="感想")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    def __str__(self):
        return f"{self.watch_date} : {self.arena_name}"
    
class DiaryPicture(models.Model):
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        related_name='pictures',
        verbose_name='観戦記録'
    )
    picture_url = models.ImageField(
        upload_to='diary_photos/',
        verbose_name='写真'
    )
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return f"{self.diary.watch_date}の写真"
    