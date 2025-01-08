from django.db.models import TextChoices


class ProjectSaveForm(TextChoices):
    BASIC_FORM = 'BASIC_FORM', '기본 폼'
    README_FORM = 'README_FORM', '리드미 폼'


class ProjectMemberRole(TextChoices):
    # 첫번째가 실제 저장 값, 두번째가 label
    LEADER = "LEADER", "팀장"
    MEMBER = "MEMBER", "팀원"


class ProjectStatus(TextChoices):
    PLANNING = "PLANNING", "계획중"
    IN_PROGRESS = "IN_PROGRESS", "진행중"
    SUSPENDED = "SUSPENDED", "중단"
    COMPLETED = "COMPLETED", "완료"


class TechStackCategoryChoices(TextChoices):
    CLIENT = 'CLIENT', '클라이언트 사이드'
    SERVER = 'SERVER', '서버 사이드'
    INFRA = 'INFRA', '인프라/플랫폼'
    DATA = 'DATA', '데이터'
    AI_ML = 'AI_ML', 'AI/ML'
    SPECIAL = 'SPECIAL', '특수 분야'
    PRODUCT = 'PRODUCT', '제품/서비스'


class TechStackSubCategoryChoices(TextChoices):
    # 클라이언트 사이드
    WEB_FRONTEND = 'WEB_FRONTEND', '웹 프론트엔드'
    MOBILE_APP = 'MOBILE_APP', '모바일 앱'
    DESKTOP_APP = 'DESKTOP_APP', '데스크톱 앱'
    GAME_CLIENT = 'GAME_CLIENT', '게임 클라이언트'
    XR = 'XR', 'XR (AR/VR)'

    # 서버 사이드
    BACKEND = 'BACKEND', '백엔드'
    DATABASE = 'DATABASE', '데이터베이스'
    SERVERLESS = 'SERVERLESS', '서버리스'

    # 인프라/플랫폼
    DEVOPS = 'DEVOPS', 'DevOps'
    CLOUD = 'CLOUD', '클라우드'
    MONITORING = 'MONITORING', '모니터링/관측성'
    SECURITY = 'SECURITY', '보안'

    # 데이터
    DATA_ENG = 'DATA_ENG', '데이터 엔지니어링'
    DATA_SCIENCE = 'DATA_SCIENCE', '데이터 사이언스'
    BI_VISUALIZATION = 'BI_VISUALIZATION', 'BI/시각화'

    # AI/ML
    MACHINE_LEARNING = 'MACHINE_LEARNING', '머신러닝'
    DEEP_LEARNING = 'DEEP_LEARNING', '딥러닝'
    NLP = 'NLP', 'NLP'
    COMPUTER_VISION = 'COMPUTER_VISION', '컴퓨터 비전'

    # 특수 분야
    EMBEDDED_IOT = 'EMBEDDED_IOT', '임베디드/IoT'
    BLOCKCHAIN = 'BLOCKCHAIN', '블록체인/Web3'
    ROBOTICS = 'ROBOTICS', '로보틱스'

    # 제품/서비스
    PRODUCT_MANAGEMENT = 'PRODUCT_MANAGEMENT', '제품 관리'
    UX_UI = 'UX_UI', 'UX/UI 디자인'
    QA = 'QA', '품질 보증(QA)'
    TECHNICAL_DOC = 'TECHNICAL_DOC', '기술 문서'