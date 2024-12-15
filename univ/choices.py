from django.db.models import TextChoices


class Region(TextChoices):
    # 첫번째가 실제 저장 값, 두번째가 label
    SEOUL = "SEOUL", "서울"
    GYEONGGI = "GYEONGGI", "경기"
    INCHEON = "INCHEON", "인천"
    GANGWON = "GANGWON", "강원"
    CHUNGCHEONG = "CHUNGCHEONG", "충청"
    JEOLLA = "JEOLLA", "전라"
    GYEONGSANG = "GYEONGSANG", "경상"
    JEJU = "JEJU", "제주"
