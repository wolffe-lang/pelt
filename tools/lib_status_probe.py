"""Test-only counter overlay, provenance validation and independent diagnostics."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

SINK_ENABLED = False
TOTAL = "    if sh.count_routes {\n        sh.route_total += 1\n    }"
STATUS = "            if sh.count_routes && r.status_route {\n                sh.route_status += 1\n            }"
WRITER = r'''
fn corpus_counter_config() -> (bool, str, str) {
    let a = env_args()
    if a.len >= 5 && a[0] == "--status-corpus" && a[1] == "--counter-sink" {
        return (true, a[2], a[3])
    }
    (false, "", "")
}

fn corpus_counter_append(path: str, value: str) -> bool {
    let fd = fs_open_perm(path, 2, 0o600) else |_| { return false }
    var out = buf()
    put(mut out, value)
    fs_write_chunk(fd, out.b) else |_| {
        fs_close(fd) else |_| {}
        return false
    }
    fs_close(fd) else |_| { return false }
    true
}

fn corpus_counter_fault(path: str) {
    let prior = fs_stat(path + ".failed") else |_| List[int]()
    if prior.len > 0 { return }
    fs_rename(path, path + ".failed") else |_| {}
}

fn corpus_counter_emit(done: int, total: int) {
    copy region corpus_prefix {
        let (on, path, nonce) = corpus_counter_config()
        if !on { return }
        let prior = fs_stat(path + ".failed") else |_| List[int]()
        if prior.len > 0 { return }
        let owner_bytes = fs_read_bytes(path + ".owner") else |_| { corpus_counter_fault(path); return }
        let owner = str_from_utf8(owner_bytes) else |_| { corpus_counter_fault(path); return }
        let pid = os_pid()
        if owner != "{nonce} {pid}\n" { return }
        let writes = 1 + total + done
        if !corpus_counter_append(
            path, "PREFIX 1 {nonce} {pid} {total} {done} {writes}\n",
        ) { corpus_counter_fault(path) }
    }
}

fn corpus_counter_init() {
    copy region corpus_init {
        let (on, path, nonce) = corpus_counter_config()
        if !on { return }
        let pid = os_pid()
        if !corpus_counter_append(path + ".owner", "{nonce} {pid}\n") { corpus_counter_fault(path); return }
        corpus_counter_emit(0, 0)
    }
}
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files(root):
    root = Path(root)
    result = {}
    for path in sorted((root / "src").rglob("*")):
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError("source-symlink:" + str(relative))
        if path.is_file():
            result[str(relative)] = path.read_bytes()
    return result


def replace_once(text, old, new, label):
    if text.count(old) != 1:
        raise ValueError("anchor-drift:" + label)
    return text.replace(old, new)


def overlay(original, enabled):
    updated = dict(original)
    name = "src/sh/exec.lu"
    text = original[name].decode()
    text = replace_once(text, TOTAL, TOTAL.replace("sh.route_total += 1", "sh.route_total += 1\n        corpus_counter_emit(sh.route_status, sh.route_total)"), "counter-total")
    text = replace_once(text, STATUS, STATUS.replace("sh.route_status += 1", "sh.route_status += 1\n                corpus_counter_emit(sh.route_status, sh.route_total)"), "counter-status")
    updated[name] = text.encode()
    name = "src/sh/main.lu"
    text = original[name].decode()
    text = replace_once(text, "pub fn status_probe(args: List[str]) -> int {", '''pub fn status_probe(input: List[str]) -> int {
    let has_sink = input.len >= 4 && input[0] == "--counter-sink"
    let args = if has_sink then input[3..input.len] else input''', "probe-config")
    if enabled:
        text = replace_once(text, "    sh.count_routes = true\n    let st = run_source_state(", "    sh.count_routes = true\n    corpus_counter_init()\n    let st = run_source_state(", "probe-init")
    else:
        if text.count("    sh.count_routes = true\n    let st = run_source_state(") != 1:
            raise ValueError("anchor-drift:probe-init")
    text = replace_once(text, "\nfn run_source_state(", WRITER + "\nfn run_source_state(", "probe-writer")
    updated[name] = text.encode()
    return updated


def differences(original, updated):
    changed, hunks, parts = [], {}, []
    for name in sorted(original):
        if original[name] == updated[name]:
            continue
        changed.append(name)
        part = "".join(difflib.unified_diff(original[name].decode().splitlines(True), updated[name].decode().splitlines(True), fromfile="a/" + name, tofile="b/" + name))
        hunks[name] = sum(line.startswith("@@ ") for line in part.splitlines())
        parts.append(part)
    return changed, hunks, "".join(parts)


def revision(root, suffix=""):
    result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD" + suffix], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def committed_source(root, original, commit, tree):
    if commit is None:  # isolated source fixtures; the executable builder rejects these
        return
    if revision(root) != commit or revision(root, ":src") != tree:
        raise ValueError("probe-source-commit-drift")
    result = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "-z", commit, "--", "src"], check=True, capture_output=True)
    blobs = {}
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError("probe-source-not-regular")
        blobs[name.decode()] = oid
    actual = {name: hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
              for name, data in original.items()}
    if actual != blobs:
        raise ValueError("probe-source-not-committed")


def generate(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output == source or source in output.parents:
        raise ValueError("generated-output-inside-source")
    if output.exists():
        raise ValueError("generated-output-exists")
    original = files(source)
    commit, tree = revision(source), revision(source, ":src")
    committed_source(source, original, commit, tree)
    updated = overlay(original, SINK_ENABLED)  # validate every anchor before creating output
    changed, hunks, diff = differences(original, updated)
    if changed != ["src/sh/exec.lu", "src/sh/main.lu"] or hunks["src/sh/exec.lu"] != 2:
        raise ValueError("undeclared-overlay")
    output.mkdir(parents=True)
    for name, data in updated.items():
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (output / "generated.diff").write_text(diff)
    manifest = {"schema": 1, "source_root": str(source), "source_commit": revision(source),
                "source_src_tree": revision(source, ":src"), "sink_enabled": SINK_ENABLED,
                "source_files": {n: digest(b) for n, b in original.items()},
                "generated_files": {n: digest(b) for n, b in updated.items()},
                "diff_files": changed, "hunks": hunks, "diff_sha256": digest(diff.encode()),
                "producer_sha256": digest(Path(__file__).read_bytes())}
    (output / "probe.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def verify(manifest_path):
    path = Path(manifest_path).resolve()
    manifest = json.loads(path.read_text())
    if manifest.get("schema") != 1 or type(manifest.get("sink_enabled")) is not bool:
        raise ValueError("invalid-probe-manifest")
    original = files(manifest["source_root"])
    committed_source(manifest["source_root"], original, manifest["source_commit"], manifest["source_src_tree"])
    if {n: digest(b) for n, b in original.items()} != manifest["source_files"]:
        raise ValueError("probe-original-source-drift")
    expected = overlay(original, manifest["sink_enabled"])
    actual = files(path.parent)
    if actual != expected or {n: digest(b) for n, b in actual.items()} != manifest["generated_files"]:
        raise ValueError("probe-source-drift")
    changed, hunks, diff = differences(original, expected)
    if manifest["diff_files"] != changed or manifest["hunks"] != hunks or changed != ["src/sh/exec.lu", "src/sh/main.lu"] or hunks["src/sh/exec.lu"] != 2:
        raise ValueError("undeclared-probe-diff")
    if (path.parent / "generated.diff").read_text() != diff or manifest["diff_sha256"] != digest(diff.encode()):
        raise ValueError("probe-diff-drift")
    if "probe_sha256" in manifest:
        if digest((path.parent / "probe").read_bytes()) != manifest["probe_sha256"]:
            raise ValueError("probe-binary-drift")
    return manifest


def read_counter(path, nonce, pid):
    path = Path(path)
    failed = Path(str(path) + ".failed")
    if failed.exists():
        return {"state": "invalid", "reason": "counter-write-failed", "done": None, "total": None,
                "preserved_prefix": str(failed), "sha256": digest(failed.read_bytes())}
    if not path.exists() or not path.stat().st_size:
        return {"state": "missing", "reason": "counter-missing", "done": None, "total": None}
    data = path.read_bytes()
    invalid = {"state": "invalid", "reason": "counter-invalid", "done": None, "total": None}
    if not data.endswith(b"\n"):
        return dict(invalid, detail="truncated")
    previous = None
    frames = data.splitlines()
    for index, line in enumerate(frames):
        match = re.fullmatch(rb"PREFIX 1 ([0-9a-z]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)", line)
        if not match:
            return dict(invalid, detail="frame")
        token, owner, total, done, writes = match.groups()
        owner, total, done, writes = map(int, (owner, total, done, writes))
        if token.decode() != nonce or owner != pid or not 0 <= done <= total or writes != index + 1 or writes != 1 + total + done:
            return dict(invalid, detail="identity-counts-or-sequence")
        if previous is None:
            if (total, done) != (0, 0):
                return dict(invalid, detail="initial-frame")
        elif (total - previous[0], done - previous[1]) not in ((1, 0), (0, 1)):
            return dict(invalid, detail="counter-step")
        previous = total, done
    return {"state": "valid", "done": done, "total": total, "owner_pid": owner,
            "data_write_calls": len(frames), "control_write_calls": 1,
            "write_calls": len(frames) + 1, "bytes": len(data), "sha256": digest(data)}


def compare(normal, probe, counter):
    failures = []
    for label, outcome in (("normal", normal), ("probe", probe)):
        if outcome is None:
            failures.append(label + "-timeout")
    behavior = {"match": None, "different_fields": []}
    if normal is not None and probe is not None:
        stripped = re.sub(rb"^ROUTE corpus done=\d+ total=\d+\n", b"", probe["err"], flags=re.M)
        for name, a, b in (("exit", normal["exit"], probe["exit"]), ("stdout", normal["stdout"], probe["stdout"]), ("stderr-presence", bool(normal["err"]), bool(stripped))):
            if a != b:
                behavior["different_fields"].append(name)
        behavior["match"] = not behavior["different_fields"]
        if not behavior["match"]:
            failures.append("behavior-mismatch")
        if (normal["raw_returncode"] < 0) != (probe["raw_returncode"] < 0):
            failures.append("termination-mismatch")
        markers = re.findall(rb"^ROUTE corpus done=(\d+) total=(\d+)\n", probe["err"], flags=re.M)
        if len(markers) > 1:
            failures.append("duplicate-final-counter")
        if markers and counter["state"] == "valid" and tuple(map(int, markers[0])) != (counter["done"], counter["total"]):
            failures.append("final-counter-disagreement")
    if counter["state"] != "valid":
        failures.append(counter.get("reason", "counter-invalid"))
    return {"behavior": behavior, "counter": counter, "failures": failures, "observed": not failures}
