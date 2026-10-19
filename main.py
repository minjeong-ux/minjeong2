"""나만의 프롬프트 관리 프로그램 (콘솔)"""

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

DEFAULT_PROMPTS = [
    {
        "title": "회의록 요약",
        "content": "다음 회의 내용을 핵심 결정사항, 담당자, 기한으로 나눠 5줄 이내로 요약해줘.",
        "category": "텍스트 생성",
        "favorite": True,
    },
    {
        "title": "미니멀 제품 사진",
        "content": "흰 배경 위의 무드등, 부드러운 그림자, 35mm 렌즈, 따뜻한 조명, 제품 사진 스타일",
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "시니어 코드 리뷰어",
        "content": "너는 10년차 시니어 개발자야. 코드의 버그와 가독성 문제를 짚고 개선안을 제시해줘.",
        "category": "페르소나",
        "favorite": False,
    },
]

MENU_ITEMS = [
    ("1", "프롬프트 추가"),
    ("2", "프롬프트 목록"),
    ("0", "종료"),
]


def input_non_empty(message):
    """빈 값이 아닐 때까지 반복해서 입력받는다."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


def input_number(message, min_value, max_value):
    """min_value~max_value 범위의 정수를 입력받는다. 잘못된 입력이면 None을 반환한다."""
    value = input(message).strip()
    try:
        number = int(value)
    except ValueError:
        print("숫자를 입력해주세요.")
        return None
    if number < min_value or number > max_value:
        print(f"{min_value}~{max_value} 사이의 번호를 입력해주세요.")
        return None
    return number


def choose_category():
    """미리 정의된 카테고리 중 하나를 고르거나 직접 입력받는다."""
    custom_number = len(CATEGORIES) + 1
    while True:
        print("카테고리 선택:")
        for number, category in enumerate(CATEGORIES, start=1):
            print(f"{number}) {category}")
        print(f"{custom_number}) 직접 입력")

        number = input_number("선택: ", 1, custom_number)
        if number is None:
            continue
        if number == custom_number:
            return input_non_empty("카테고리 이름: ")
        return CATEGORIES[number - 1]


def add_prompt(prompts):
    """새 프롬프트를 입력받아 목록에 추가한다."""
    print("\n=== 프롬프트 추가 ===")
    title = input_non_empty("제목: ")
    content = input_non_empty("내용: ")
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
    })
    print("프롬프트가 추가되었습니다!")


def print_prompt_line(number, prompt):
    """'번호. [카테고리] 제목 ⭐' 형식으로 한 줄 출력한다."""
    star = " ⭐" if prompt["favorite"] else ""
    print(f"{number}. [{prompt['category']}] {prompt['title']}{star}")


def show_list(prompts):
    """저장된 모든 프롬프트를 번호와 함께 출력한다."""
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다. 먼저 프롬프트를 추가해주세요.")
        return
    for number, prompt in enumerate(prompts, start=1):
        print_prompt_line(number, prompt)
    print(f"총 {len(prompts)}개의 프롬프트")


def show_menu():
    """메인 메뉴를 출력한다."""
    print("\n=== 나만의 프롬프트 관리 ===")
    for key, label in MENU_ITEMS:
        print(f"{key}. {label}")


def main():
    prompts = [dict(prompt) for prompt in DEFAULT_PROMPTS]

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            show_list(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 메뉴에 있는 번호를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
