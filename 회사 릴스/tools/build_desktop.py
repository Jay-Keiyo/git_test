"""바탕화면 「흙수저 김토토」 폴더의 구성표(desktop_manifest.json)를 만든다.

바탕화면 폴더의 server.py 는 켜질 때 이 구성표를 GitHub에서 받아,
해시가 다른 파일만 새로 내려받는다. 파일을 고친 뒤에는 이 스크립트를 다시 돌리고 커밋·푸시한다.

사용: python3 tools/build_desktop.py [zip 출력 경로]
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent      # 회사 릴스
REPO = BASE.parent                                  # 저장소 루트


def files():
    """(바탕화면 폴더 안 경로, 저장소 안 파일) 목록."""
    studio = BASE / "studio"
    out = [("시작.html", studio / "index.html"), ("server.py", studio / "server.py"),
           ("시작.bat", studio / "시작.bat"), ("시작.command", studio / "시작.command"),
           ("읽어주세요.txt", studio / "읽어주세요.txt"), ("자료/ep1.js", studio / "ep1.js"),
           ("자료/AGENTS.md", BASE / "AGENTS.md")]
    out += [(f"자료/{p.name}", p) for p in sorted(BASE.glob("0*.md"))]
    for folder in ("assets", "episodes", "preview"):
        out += [(f"자료/{p.relative_to(BASE).as_posix()}", p) for p in sorted((BASE / folder).rglob("*")) if p.is_file()]
    return out


def main():
    manifest = {"files": {}}
    for local, src in files():
        manifest["files"][local] = {"src": src.relative_to(REPO).as_posix(),
                                    "sha256": hashlib.sha256(src.read_bytes()).hexdigest()}
    (BASE / "desktop_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"구성표: 파일 {len(manifest['files'])}개")
    if len(sys.argv) > 1:  # 처음 한 번 받을 압축 파일
        with zipfile.ZipFile(sys.argv[1], "w", zipfile.ZIP_DEFLATED) as z:
            for local, src in files() + [("codex_설정.json", BASE / "studio" / "codex_설정.json")]:
                info = zipfile.ZipInfo.from_file(src, "흙수저 김토토/" + local)
                if local.endswith(".command"):
                    info.external_attr = 0o755 << 16
                z.writestr(info, src.read_bytes(), zipfile.ZIP_DEFLATED)
            url = "[InternetShortcut]\r\nURL=https://claude.ai/artifact/PZmQcEkrhZ2KDb5iUnPF74\r\n"
            z.writestr("흙수저 김토토/Claude 제작실 (온라인).url", url)
        print(f"압축 파일: {sys.argv[1]}")


if __name__ == "__main__":
    main()
