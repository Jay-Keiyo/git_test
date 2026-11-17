"""흙수저 김토토 제작실 - PC용 로컬 서버.

시작.html 을 http://127.0.0.1:8765 로 열어 주고, 페이지의 버튼이 누르면
이 PC에 설치된 Codex(codex exec)를 실행해 대본을 쓰거나 그림을 만들게 한다.
그림은 자료/만든그림/<화>/<그림 번호>.png 로 저장된다.

Codex를 부르는 명령은 codex_설정.json 에서 바꿀 수 있다.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "자료"
OUT = DATA / "만든그림"
CONFIG = ROOT / "codex_설정.json"
PORT = 8765
DEFAULT = {
    "command": ["codex", "exec", "--skip-git-repo-check", "--sandbox", "workspace-write"],
    "prompt_via": "stdin",
    "timeout_seconds": 900,
}
LOCK = threading.Lock()
REPO_RAW = os.environ.get("TOTO_REPO_RAW", "https://raw.githubusercontent.com/Jay-Keiyo/git_test/claude/office-drama-reels-88za6o/")
MANIFEST = "회사 릴스/desktop_manifest.json"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(repo_path, timeout=20):
    with urlopen(REPO_RAW + quote(repo_path), timeout=timeout) as r:
        return r.read()


def self_update():
    """GitHub에 올라간 최신 파일과 비교해 바뀐 것만 받아 온다. 바뀐 파일 목록을 돌려준다.
    자료/만든그림 과 codex_설정.json 처럼 이 PC에서 만든 것은 건드리지 않는다."""
    try:
        manifest = json.loads(fetch(MANIFEST).decode("utf-8"))
    except Exception as e:  # 인터넷이 없거나 GitHub에 못 가면 그냥 지금 파일로 켠다
        print(f"업데이트를 확인하지 못했습니다 ({e.__class__.__name__}). 지금 파일로 켭니다.")
        return []
    changed = []
    for local, info in manifest.get("files", {}).items():
        target = (ROOT / local).resolve()
        if ROOT.resolve() not in target.parents or "만든그림" in target.parts:
            continue
        if target.exists() and sha256(target) == info["sha256"]:
            continue
        try:
            data = fetch(info["src"], timeout=60)
        except Exception as e:
            print(f"  {local} 을(를) 받지 못했습니다 ({e.__class__.__name__}).")
            continue
        if hashlib.sha256(data).hexdigest() != info["sha256"]:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".new")
        tmp.write_bytes(data)
        os.replace(tmp, target)
        changed.append(local)
    if changed:
        print(f"최신 파일 {len(changed)}개를 받았습니다: " + ", ".join(changed[:8]) + (" …" if len(changed) > 8 else ""))
    else:
        print("이미 최신입니다.")
    return changed


def config():
    try:
        cfg = {**DEFAULT, **json.loads(CONFIG.read_text(encoding="utf-8"))}
    except (OSError, ValueError):
        cfg = dict(DEFAULT)
    # 예전 설정의 --full-auto 는 새 Codex에서 없어진 옵션이라 바꿔 준다
    cmd = []
    for a in cfg["command"]:
        cmd += ["--sandbox", "workspace-write"] if a == "--full-auto" else [a]
    cfg["command"] = cmd
    return cfg


def codex_home():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def newest_generated(since):
    """Codex 그림 도구가 저장한 그림 중 since 이후에 생긴 가장 최근 파일."""
    folder = codex_home() / "generated_images"
    if not folder.is_dir():
        return None
    files = [f for f in folder.rglob("*") if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp") and f.stat().st_mtime >= since]
    return max(files, key=lambda f: f.stat().st_mtime) if files else None


def run_codex(prompt, images=()):
    """Codex에 prompt를 보내고 (성공 여부, 출력)을 돌려준다. 한 번에 하나씩만 실행한다."""
    cfg = config()
    cmd = list(cfg["command"])
    exe = shutil.which(cmd[0])
    if not exe:
        return False, f"'{cmd[0]}' 명령을 찾지 못했습니다. Codex가 설치되어 있고 터미널에서 '{cmd[0]}'이 실행되는지 확인해 주세요."
    cmd[0] = exe
    for im in images:
        cmd += ["-i", im]
    last = Path(tempfile.gettempdir()) / f"toto_codex_{os.getpid()}_{threading.get_ident()}.txt"
    cmd += ["-o", str(last)]
    stdin = prompt if cfg.get("prompt_via") == "stdin" else None
    if stdin is None:
        cmd.append(prompt)
    with LOCK:
        try:
            last.unlink(missing_ok=True)
            p = subprocess.run(cmd, input=stdin, cwd=DATA, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=cfg["timeout_seconds"])
        except subprocess.TimeoutExpired:
            return False, "Codex가 제한 시간 안에 끝내지 못했습니다."
        except OSError as e:
            return False, f"Codex를 실행하지 못했습니다: {e}"
    try:
        out = last.read_text(encoding="utf-8").strip()
        last.unlink(missing_ok=True)
    except OSError:
        out = (p.stdout or "").strip()
    if p.returncode != 0:
        tail = ((p.stderr or "") + "\n" + out).strip()[-1500:]
        return False, f"Codex가 오류로 끝났습니다 (코드 {p.returncode}).\n{tail}"
    return True, out


def safe_rel(rel):
    """자료 폴더 안의 경로만 허용한다."""
    path = (DATA / rel).resolve()
    if DATA.resolve() not in path.parents and path != DATA.resolve():
        raise ValueError(rel)
    return path


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                      ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                      ".md": "text/plain; charset=utf-8", ".json": "application/json; charset=utf-8",
                      ".webp": "image/webp"}

    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def log_message(self, fmt, *args):
        sys.stderr.write("  " + (fmt % args) + "\n")

    def send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/ping":
            exe = shutil.which(config()["command"][0])
            return self.send_json(200, {"ok": True, "codex": bool(exe)})
        if u.path == "/api/images":
            ep = parse_qs(u.query).get("ep", [""])[0]
            folder = OUT / ep
            files = sorted(f.stem for f in folder.glob("*.png")) if ep and folder.is_dir() else []
            return self.send_json(200, {"images": files})
        return super().do_GET()

    def do_POST(self):
        u = urlparse(self.path)
        try:
            n = int(self.headers.get("Content-Length", "0"))
            req = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except ValueError:
            return self.send_json(400, {"error": "요청을 읽지 못했습니다."})
        if self.client_address[0] not in ("127.0.0.1", "::1"):
            return self.send_json(403, {"error": "이 PC에서만 쓸 수 있습니다."})

        if u.path == "/api/text":
            ok, out = run_codex(str(req.get("prompt", "")))
            return self.send_json(200 if ok else 500, {"text": out} if ok else {"error": out})

        if u.path == "/api/image":
            ep, img = str(req.get("ep", "")), str(req.get("img", ""))
            if not (ep.replace("-", "").isalnum() and img.replace("-", "").isalnum()) or "." in ep + img:
                return self.send_json(400, {"error": "그림 이름이 올바르지 않습니다."})
            target = OUT / ep / f"{img}.png"
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                old = target.with_name(f"{img}_old_{time.strftime('%m%d%H%M%S')}.png")
                target.rename(old)
            refs = []
            for r in req.get("refs", []):
                try:
                    path = safe_rel(r)
                except ValueError:
                    continue
                if path.exists():
                    refs.append(path.relative_to(DATA).as_posix())
            rel_target = target.relative_to(DATA).as_posix()
            prompt = "\n".join([
                "$imagegen 으로 그림 한 장을 만들어 줘. 내장 image_gen 도구를 쓰고, API 키가 필요한 CLI 방식은 쓰지 마.",
                "다른 파일은 만들거나 고치지 마.",
                "",
                "[저장할 곳]",
                f"{rel_target}",
                "그림 도구는 결과를 $CODEX_HOME/generated_images/ 아래에 저장한다. 만든 뒤 그 파일을 위 경로로 복사해 줘.",
                "",
                "[참조 그림] 함께 첨부한 그림이다. 인물의 얼굴, 피부색, 머리, 머리 위 식물, 옷, 그림체를 똑같이 맞춰.",
                *([f"- {r}" for r in refs] or ["- 없음"]),
                "",
                "[그림 내용]",
                str(req.get("prompt", "")),
                "",
                "세로 9:16 (안 되면 가장 가까운 세로 비율). AGENTS.md 의 그림 규칙을 지켜. 저장이 끝나면 '완료' 한 단어만 답해.",
            ])
            started = time.time() - 1
            ok, out = run_codex(prompt, refs)
            if not target.exists():
                found = newest_generated(started)
                if found:
                    shutil.copyfile(found, target)
            if target.exists():
                return self.send_json(200, {"url": f"/자료/{rel_target}?t={int(time.time())}"})
            msg = out if not ok else "Codex가 끝났지만 그림 파일이 저장되지 않았습니다. Codex가 이 환경에서 그림을 만들 수 있는지 확인해 주세요.\n" + out[-800:]
            return self.send_json(500, {"error": msg})

        return self.send_json(404, {"error": "없는 주소입니다."})


def main():
    os.chdir(ROOT)
    if "--no-update" not in sys.argv:
        print("업데이트 확인 중…")
        changed = self_update()
        if "server.py" in changed:  # 서버 자신이 바뀌었으면 새 서버로 다시 켠다
            print("제작실 서버가 새 버전으로 바뀌어 다시 켭니다.")
            os.execv(sys.executable, [sys.executable, str(ROOT / "server.py"), "--no-update"])
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print(f"이미 제작실이 켜져 있는 것 같습니다. 브라우저에서 http://127.0.0.1:{PORT}/시작.html 을 여세요.")
        webbrowser.open(f"http://127.0.0.1:{PORT}/%EC%8B%9C%EC%9E%91.html")
        return
    url = f"http://127.0.0.1:{PORT}/%EC%8B%9C%EC%9E%91.html"
    print("흙수저 김토토 제작실이 켜졌습니다.")
    print(f"브라우저가 안 열리면 주소창에 붙여 넣으세요: http://127.0.0.1:{PORT}/시작.html")
    print("이 창을 닫으면 제작실이 꺼집니다.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
