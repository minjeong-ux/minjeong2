# 나만의 프롬프트 관리 프로그램

자주 쓰는 AI 프롬프트를 **분류·검색·즐겨찾기**로 관리하는 Python 콘솔 프로그램입니다.
외부 라이브러리 없이 표준 라이브러리(`json`, `os`, `re`)만 사용합니다.

- 기본 기능: 추가 / 목록 / 카테고리별 조회 / 키워드 검색 / 상세 보기 / 즐겨찾기
- 보너스 1: JSON 저장·불러오기, 카테고리별 Markdown 내보내기
- 보너스 2: 수정·삭제, 상세 보기 조회수 기록, 조회수 Top 목록

## 실행 방법

Python 3.10 이상, Git이 필요합니다.

```bash
git clone https://github.com/minjeong-ux/minjeong2.git
cd minjeong2
python3 --version          # 3.10 이상인지 확인 (Windows: python --version)
python3 main.py            # Windows: python main.py
```

처음 실행하면 샘플 프롬프트 3개로 시작하고, 종료(0번)할 때 `prompts.json`에 자동 저장되어
다음 실행 때 이어서 사용합니다.

```
=== 나만의 프롬프트 관리 ===
1. 프롬프트 추가            8. 프롬프트 수정
2. 프롬프트 목록            9. 프롬프트 삭제
3. 카테고리별 조회          10. 많이 본 프롬프트 Top
4. 프롬프트 검색            11. JSON 파일로 저장
5. 프롬프트 상세 보기       12. JSON 파일에서 불러오기
6. 즐겨찾기 관리            13. 카테고리별 Markdown 내보내기
7. 즐겨찾기 목록            0. 종료
```

(실제 출력은 번호 순서대로 한 줄씩 나옵니다. 전체 실행 로그: [docs/run_log.txt](docs/run_log.txt))

## 기능 설명

| 번호 | 기능 | 설명 |
|---|---|---|
| 1 | 추가 | 제목·내용·카테고리 입력. 빈 값은 다시 입력. 같은 카테고리에 같은 제목(대소문자·공백 무시)은 거부 |
| 2 | 목록 | `번호. [카테고리] 제목 ⭐` 형식 |
| 3 | 카테고리별 조회 | 선택한 카테고리의 프롬프트만 출력 (직접 입력한 카테고리도 포함) |
| 4 | 검색 | 제목 **또는** 내용에 키워드가 포함된 항목 (대소문자 무시) |
| 5 | 상세 보기 | 전체 내용 출력, **조회수 +1** |
| 6 | 즐겨찾기 관리 | 번호 입력으로 추가/해제 토글 |
| 7 | 즐겨찾기 목록 | ⭐ 항목만 출력 |
| 8 | 수정 | 제목/내용/카테고리 수정 (빈 값 = 기존 값 유지) |
| 9 | 삭제 | y/N 확인 후 삭제 |
| 10 | Top | 조회수 내림차순 상위 5개 (조회수 0 제외, 동률은 등록 순) |
| 11/12 | JSON 저장/불러오기 | `prompts.json` 읽기·쓰기. 깨진 파일/잘못된 항목은 안내 후 무시 |
| 13 | Markdown 내보내기 | `exports/<카테고리>.md` 를 카테고리마다 생성 |
| 0 | 종료 | 자동 저장 후 종료 |

잘못된 메뉴 번호, 숫자가 아닌 입력, 범위를 벗어난 번호에는 안내 메시지를 출력합니다.
조회·검색 결과의 번호는 **전체 목록 기준 번호**라 상세 보기·즐겨찾기·수정·삭제에 그대로 쓸 수 있습니다.

## 코드 구조

모든 코드는 `main.py` 한 파일, 기능마다 함수 하나입니다.

| 구분 | 함수 |
|---|---|
| 입력 검증 | `input_non_empty()` (빈 값 재입력), `input_number()` (정수·범위), `choose_category()`, `select_prompt()` |
| 기본 기능 | `add_prompt()`, `show_list()`, `show_by_category()`, `search_prompt()`, `show_detail()`, `toggle_favorite()`, `show_favorites()` |
| 보너스 2 | `edit_prompt()`, `delete_prompt()`, `show_top()`, `has_duplicate()` |
| 보너스 1 | `save_prompts()`, `load_prompts()`, `normalize_prompt()`, `export_markdown()`, `safe_filename()` |
| 공통 도우미 | `find_prompts(prompts, condition)` (조건에 맞는 (번호, 프롬프트) 반환), `print_matches()`, `get_all_categories()` |
| 진입 | `show_menu()`, `main()` (while 메뉴 루프) |

데이터는 딕셔너리의 리스트입니다.

```python
prompts = [
    {"title": "회의록 요약", "content": "...", "category": "텍스트 생성",
     "favorite": True, "views": 0},
]
```

## Git 작업 방식

기능 단위 브랜치에서 작업하고 `main`에 `--no-ff` 병합했습니다. (`git log --oneline --graph`)

`feature/add-list` → `feature/category-search` → `feature/favorites` →
`feature/crud-views` (보너스 2) → `feature/persistence-export` (보너스 1) → `docs/readme-evaluation`

## 문서

- [docs/env_check.txt](docs/env_check.txt): Python/Git 버전, user.name/email
- [docs/clone_log.txt](docs/clone_log.txt): 샘플 저장소 clone 기록
- [docs/run_log.txt](docs/run_log.txt): 프로그램 실행 로그
- [EVALUATION.md](EVALUATION.md): 평가표 항목별 자체 점검과 인터뷰 답변
