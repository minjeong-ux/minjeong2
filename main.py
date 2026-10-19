"""나만의 프롬프트 관리 프로그램 (콘솔)"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "prompts.json")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

DEFAULT_PROMPTS = [
    {
        "title": "회의록 요약",
        "content": "다음 회의 내용을 핵심 결정사항, 담당자, 기한으로 나눠 5줄 이내로 요약해줘.",
        "category": "텍스트 생성",
        "favorite": True,
        "views": 0,
    },
    {
        "title": "미니멀 제품 사진",
        "content": "흰 배경 위의 무드등, 부드러운 그림자, 35mm 렌즈, 따뜻한 조명, 제품 사진 스타일",
        "category": "이미지 생성",
        "favorite": False,
        "views": 0,
    },
    {
        "title": "시니어 코드 리뷰어",
        "content": "너는 10년차 시니어 개발자야. 코드의 버그와 가독성 문제를 짚고 개선안을 제시해줘.",
        "category": "페르소나",
        "favorite": False,
        "views": 0,
    },
]

MENU_ITEMS = [
    ("1", "프롬프트 추가"),
    ("2", "프롬프트 목록"),
    ("3", "카테고리별 조회"),
    ("4", "프롬프트 검색"),
    ("5", "프롬프트 상세 보기"),
    ("6", "즐겨찾기 관리"),
    ("7", "즐겨찾기 목록"),
    ("8", "프롬프트 수정"),
    ("9", "프롬프트 삭제"),
    ("10", "많이 본 프롬프트 Top"),
    ("11", "JSON 파일로 저장"),
    ("12", "JSON 파일에서 불러오기"),
    ("13", "카테고리별 Markdown 내보내기"),
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


def has_duplicate(prompts, title, category, ignore=None):
    """같은 카테고리에 같은 제목(공백/대소문자 무시)이 이미 있는지 확인한다.

    ignore: 검사에서 제외할 프롬프트 (수정 중인 자기 자신).
    """
    key = title.strip().lower()
    return any(
        prompt is not ignore
        and prompt["category"] == category
        and prompt["title"].strip().lower() == key
        for prompt in prompts
    )


def add_prompt(prompts):
    """새 프롬프트를 입력받아 목록에 추가한다."""
    print("\n=== 프롬프트 추가 ===")
    title = input_non_empty("제목: ")
    content = input_non_empty("내용: ")
    category = choose_category()

    if has_duplicate(prompts, title, category):
        print(f"[{category}] 카테고리에 같은 제목의 프롬프트가 이미 있습니다. 추가하지 않았습니다.")
        return

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
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


def find_prompts(prompts, condition):
    """condition(prompt)가 참인 프롬프트를 (전체 목록 기준 번호, 프롬프트) 목록으로 반환한다.

    전체 목록 기준 번호를 유지해서, 결과에 보이는 번호를 그대로 다른 기능에 입력할 수 있다.
    """
    return [
        (number, prompt)
        for number, prompt in enumerate(prompts, start=1)
        if condition(prompt)
    ]


def print_matches(matches):
    """find_prompts()의 결과를 출력한다."""
    for number, prompt in matches:
        print_prompt_line(number, prompt)


def get_all_categories(prompts):
    """기본 카테고리에 사용자가 직접 입력한 카테고리를 더한 목록을 반환한다."""
    categories = list(CATEGORIES)
    for prompt in prompts:
        if prompt["category"] not in categories:
            categories.append(prompt["category"])
    return categories


def show_by_category(prompts):
    """선택한 카테고리의 프롬프트만 출력한다."""
    print("\n=== 카테고리별 조회 ===")
    categories = get_all_categories(prompts)
    for number, category in enumerate(categories, start=1):
        print(f"{number}) {category}")

    number = input_number("선택: ", 1, len(categories))
    if number is None:
        return
    category = categories[number - 1]

    matches = find_prompts(prompts, lambda prompt: prompt["category"] == category)
    print(f"\n[{category}] 카테고리 프롬프트:")
    if not matches:
        print("이 카테고리에 등록된 프롬프트가 없습니다.")
        return
    print_matches(matches)
    print(f"총 {len(matches)}개의 프롬프트")


def search_prompt(prompts):
    """키워드가 제목 또는 내용에 포함된 프롬프트를 찾는다 (대소문자 무시)."""
    print("\n=== 프롬프트 검색 ===")
    keyword = input_non_empty("검색어: ").lower()

    matches = find_prompts(
        prompts,
        lambda prompt: keyword in prompt["title"].lower()
        or keyword in prompt["content"].lower(),
    )
    print("\n검색 결과:")
    if not matches:
        print("검색 결과가 없습니다.")
        return
    print_matches(matches)
    print(f"{len(matches)}개의 프롬프트를 찾았습니다.")


def select_prompt(prompts):
    """번호를 입력받아 해당 프롬프트를 반환한다. 잘못된 번호면 None."""
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None
    number = input_number(f"번호 입력 (1~{len(prompts)}): ", 1, len(prompts))
    if number is None:
        return None
    return prompts[number - 1]


def show_detail(prompts):
    """선택한 프롬프트의 전체 내용을 출력한다."""
    print("\n=== 프롬프트 상세 보기 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    prompt["views"] += 1

    line = "─" * 40
    print(line)
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"조회수: {prompt['views']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '-'}")
    print(line)
    print("내용:")
    print(prompt["content"])
    print(line)


def toggle_favorite(prompts):
    """선택한 프롬프트의 즐겨찾기 상태를 추가/해제한다."""
    print("\n=== 즐겨찾기 관리 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다! ⭐")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다.")


def show_favorites(prompts):
    """즐겨찾기된 프롬프트만 모아서 출력한다."""
    print("\n=== 즐겨찾기 목록 ===")
    matches = find_prompts(prompts, lambda prompt: prompt["favorite"])
    if not matches:
        print("즐겨찾기한 프롬프트가 없습니다. (메뉴 6번에서 추가할 수 있습니다)")
        return
    print_matches(matches)
    print(f"총 {len(matches)}개의 즐겨찾기")


def edit_prompt(prompts):
    """선택한 프롬프트의 제목/내용/카테고리를 수정한다. 빈 값은 기존 값을 유지한다."""
    print("\n=== 프롬프트 수정 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    print("(빈 값으로 Enter 하면 기존 값을 유지합니다)")
    title = input(f"제목 [{prompt['title']}]: ").strip() or prompt["title"]
    content = input("내용 (비우면 유지): ").strip() or prompt["content"]
    print(f"현재 카테고리: {prompt['category']}")
    category = prompt["category"]
    if input("카테고리를 변경할까요? (y/N): ").strip().lower() == "y":
        category = choose_category()

    if has_duplicate(prompts, title, category, ignore=prompt):
        print(f"[{category}] 카테고리에 같은 제목의 프롬프트가 이미 있습니다. 수정하지 않았습니다.")
        return

    prompt["title"] = title
    prompt["content"] = content
    prompt["category"] = category
    print("프롬프트가 수정되었습니다!")


def delete_prompt(prompts):
    """선택한 프롬프트를 확인 후 삭제한다."""
    print("\n=== 프롬프트 삭제 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    answer = input(f"'{prompt['title']}' 프롬프트를 삭제할까요? (y/N): ").strip().lower()
    if answer != "y":
        print("삭제를 취소했습니다.")
        return
    prompts.remove(prompt)
    print("프롬프트가 삭제되었습니다.")


def show_top(prompts, limit=5):
    """조회수가 높은 순으로 상위 limit개를 출력한다 (조회수 0은 제외)."""
    print("\n=== 많이 본 프롬프트 Top ===")
    viewed = find_prompts(prompts, lambda prompt: prompt["views"] > 0)
    if not viewed:
        print("아직 조회 기록이 없습니다. (메뉴 5번 상세 보기로 조회수가 쌓입니다)")
        return

    # sorted()는 안정 정렬이라 조회수가 같으면 등록 순서가 유지된다.
    ranked = sorted(viewed, key=lambda item: item[1]["views"], reverse=True)[:limit]
    for rank, (number, prompt) in enumerate(ranked, start=1):
        print(f"{rank}위. (번호 {number}) [{prompt['category']}] {prompt['title']} - 조회 {prompt['views']}회")


def normalize_prompt(raw):
    """파일에서 읽은 항목을 프롬프트 딕셔너리로 정리한다. 형식이 잘못되면 None."""
    if not isinstance(raw, dict):
        return None
    title = str(raw.get("title", "")).strip()
    content = str(raw.get("content", "")).strip()
    category = str(raw.get("category", "")).strip()
    if not (title and content and category):
        return None
    views = raw.get("views", 0)
    return {
        "title": title,
        "content": content,
        "category": category,
        "favorite": bool(raw.get("favorite", False)),
        "views": views if isinstance(views, int) and views >= 0 else 0,
    }


def save_prompts(prompts, path=DATA_FILE):
    """프롬프트 목록을 JSON 파일로 저장한다. 성공하면 True."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(prompts, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"저장에 실패했습니다: {error}")
        return False
    return True


def load_prompts(path=DATA_FILE):
    """JSON 파일에서 프롬프트 목록을 읽는다. 파일이 없거나 깨졌으면 None."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError) as error:
        print(f"불러오기에 실패했습니다: {error}")
        return None
    if not isinstance(data, list):
        print("불러오기에 실패했습니다: 파일 형식이 올바르지 않습니다.")
        return None

    prompts = [item for item in map(normalize_prompt, data) if item is not None]
    skipped = len(data) - len(prompts)
    if skipped:
        print(f"형식이 잘못된 항목 {skipped}개는 건너뛰었습니다.")
    return prompts


def save_to_json(prompts):
    """메뉴: 현재 목록을 JSON 파일로 저장한다."""
    print("\n=== JSON 저장 ===")
    if save_prompts(prompts):
        print(f"{len(prompts)}개의 프롬프트를 저장했습니다: {DATA_FILE}")


def load_from_json(prompts):
    """메뉴: JSON 파일의 내용으로 현재 목록을 교체한다."""
    print("\n=== JSON 불러오기 ===")
    loaded = load_prompts()
    if loaded is None:
        print("불러올 수 있는 저장 파일이 없습니다. 현재 목록을 유지합니다.")
        return
    prompts[:] = loaded  # 같은 리스트 객체를 유지한 채 내용만 교체
    print(f"{len(prompts)}개의 프롬프트를 불러왔습니다.")


def safe_filename(name):
    """카테고리 이름을 파일 이름으로 쓸 수 있게 바꾼다."""
    return re.sub(r'[\\/:*?"<>|\s]+', "_", name).strip("_") or "category"


def export_markdown(prompts):
    """카테고리마다 Markdown 파일 하나씩 exports/ 폴더에 내보낸다."""
    print("\n=== Markdown 내보내기 ===")
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return

    try:
        os.makedirs(EXPORT_DIR, exist_ok=True)
        for category in get_all_categories(prompts):
            items = [prompt for prompt in prompts if prompt["category"] == category]
            if not items:
                continue
            lines = [f"# {category}", ""]
            for prompt in items:
                star = " ⭐" if prompt["favorite"] else ""
                lines += [
                    f"## {prompt['title']}{star}",
                    "",
                    f"- 조회수: {prompt['views']}",
                    "",
                    prompt["content"],
                    "",
                ]
            path = os.path.join(EXPORT_DIR, safe_filename(category) + ".md")
            with open(path, "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
            print(f"{category}: {len(items)}개 -> {path}")
    except OSError as error:
        print(f"내보내기에 실패했습니다: {error}")


def show_menu():
    """메인 메뉴를 출력한다."""
    print("\n=== 나만의 프롬프트 관리 ===")
    for key, label in MENU_ITEMS:
        print(f"{key}. {label}")


def main():
    prompts = load_prompts()
    if prompts is None:
        prompts = [dict(prompt) for prompt in DEFAULT_PROMPTS]

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            show_by_category(prompts)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            show_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "8":
            edit_prompt(prompts)
        elif choice == "9":
            delete_prompt(prompts)
        elif choice == "10":
            show_top(prompts)
        elif choice == "11":
            save_to_json(prompts)
        elif choice == "12":
            load_from_json(prompts)
        elif choice == "13":
            export_markdown(prompts)
        elif choice == "0":
            save_prompts(prompts)  # 종료할 때 자동 저장
            print("프로그램을 종료합니다. (데이터가 prompts.json에 저장되었습니다)")
            break
        else:
            print("잘못된 입력입니다. 메뉴에 있는 번호를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
