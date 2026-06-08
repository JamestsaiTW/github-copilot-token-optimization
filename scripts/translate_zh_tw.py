from __future__ import annotations

import json
import os
import subprocess
import textwrap
import urllib.error
import urllib.request
from pathlib import Path


MODELS_ENDPOINT = "https://models.github.ai/inference/chat/completions"
ZERO_SHA = "0" * 40


def run_git(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def supported_source_files(repo_root: Path) -> list[Path]:
    files = [repo_root / "README.md"]
    docs_dir = repo_root / "docs"
    if docs_dir.exists():
        files.extend(
            path
            for path in sorted(docs_dir.rglob("*.md"))
            if not path.name.endswith(".zh-TW.md")
        )
    return [path for path in files if path.exists()]


def is_supported_source(rel_path: Path) -> bool:
    posix = rel_path.as_posix()
    if posix == "README.md":
        return True
    return posix.startswith("docs/") and posix.endswith(".md") and not posix.endswith(".zh-TW.md")


def target_for_source(rel_path: Path) -> Path:
    if rel_path.suffix != ".md" or rel_path.name.endswith(".zh-TW.md"):
        raise ValueError(f"Unsupported source path: {rel_path}")
    return rel_path.with_name(f"{rel_path.stem}.zh-TW.md")


def parse_changed_files(repo_root: Path, before_sha: str, after_sha: str) -> tuple[set[Path], set[Path]]:
    changed_sources: set[Path] = set()
    deleted_targets: set[Path] = set()

    if not before_sha or before_sha == ZERO_SHA:
        for file_path in supported_source_files(repo_root):
            changed_sources.add(file_path.relative_to(repo_root))
        return changed_sources, deleted_targets

    diff_output = run_git(
        "diff",
        "--name-status",
        "-M",
        "--find-renames",
        before_sha,
        after_sha,
        "--",
        "README.md",
        "docs",
        cwd=repo_root,
    )

    for line in diff_output.splitlines():
        if not line.strip():
            continue

        parts = line.split("\t")
        status = parts[0]

        if status.startswith("R") and len(parts) == 3:
            old_path = Path(parts[1])
            new_path = Path(parts[2])
            if is_supported_source(new_path):
                changed_sources.add(new_path)
            if is_supported_source(old_path):
                deleted_targets.add(target_for_source(old_path))
            continue

        if len(parts) < 2:
            continue

        rel_path = Path(parts[1])
        if not is_supported_source(rel_path):
            continue

        if status == "D":
            deleted_targets.add(target_for_source(rel_path))
        else:
            changed_sources.add(rel_path)

    return changed_sources, deleted_targets


def load_skill_context() -> str:
    skill_dir = Path(
        os.environ.get(
            "TRANSLATE_SKILL_DIR",
            Path.home() / ".copilot" / "skills" / "taiwanese-mandarin-translate",
        )
    )
    required_files = [
        skill_dir / "SKILL.md",
        skill_dir / "EXAMPLES.md",
        skill_dir / "references" / "vocabulary.md",
    ]
    missing = [str(path) for path in required_files if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing translation skill files: {', '.join(missing)}")

    parts: list[str] = []
    for path in required_files:
        header = path.relative_to(skill_dir).as_posix()
        parts.append(f"## {header}\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def build_system_prompt(skill_context: str) -> str:
    return textwrap.dedent(
        f"""
        You are a translation engine for repository documentation.

        Follow the translation skill below as the highest-priority style guide.
        Output only the final translated Markdown for the target file. Do not add explanations.
        Preserve headings, tables, links, code fences, inline code, placeholders, HTML, and file paths.
        Keep brands, APIs, commands, and technical identifiers in the source language unless translation is clearly required.
        Prefer Taiwanese Mandarin written in Traditional Chinese used in Taiwan.
        Reuse accurate wording from the existing zh-TW file where possible so unchanged sections stay stable.

        {skill_context}
        """
    ).strip()


def build_user_prompt(
    source_path: Path,
    source_markdown: str,
    existing_translation: str | None,
    source_diff: str | None,
) -> str:
    existing_block = existing_translation if existing_translation else "[No existing translation file]"
    diff_block = source_diff if source_diff else "[No prior diff available. Produce a full up-to-date translation.]"
    return textwrap.dedent(
        f"""
        Update the Traditional Chinese (Taiwan) translation for this repository file.

        Source file: {source_path.as_posix()}
        Target file: {target_for_source(source_path).as_posix()}

        English source diff against previous main:
        ```diff
        {diff_block}
        ```

        Current English source Markdown:
        ```markdown
        {source_markdown}
        ```

        Existing zh-TW Markdown:
        ```markdown
        {existing_block}
        ```

        Requirements:
        - Return the full final contents for the target file only.
        - Match the English source completely.
        - Preserve Markdown structure and link targets.
        - Keep terminology natural for Taiwan readers.
        - Keep unchanged sections stable when the existing translation is already correct.
        """
    ).strip()


def request_translation(model: str, system_prompt: str, user_prompt: str, github_token: str) -> str:
    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    request = urllib.request.Request(
        MODELS_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub Models request failed: HTTP {exc.code} {error_body}") from exc

    parsed = json.loads(body)
    choices = parsed.get("choices", [])
    if not choices:
        raise RuntimeError(f"GitHub Models returned no choices: {body}")

    content = choices[0].get("message", {}).get("content", "")
    if not content:
        raise RuntimeError(f"GitHub Models returned empty content: {body}")
    return content.rstrip() + "\n"


def source_diff(repo_root: Path, before_sha: str, after_sha: str, rel_path: Path) -> str | None:
    if not before_sha or before_sha == ZERO_SHA:
        return None

    try:
        diff_text = run_git(
            "diff",
            "--unified=3",
            before_sha,
            after_sha,
            "--",
            rel_path.as_posix(),
            cwd=repo_root,
        )
    except subprocess.CalledProcessError:
        return None

    return diff_text or None


def translate_files() -> None:
    repo_root = Path(os.environ.get("GITHUB_WORKSPACE", Path.cwd())).resolve()
    output_dir = Path(os.environ["TRANSLATION_OUTPUT_DIR"]).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    github_token = os.environ["GITHUB_TOKEN"]
    before_sha = os.environ.get("GITHUB_EVENT_BEFORE", "")
    after_sha = os.environ.get("GITHUB_SHA", "HEAD")
    translate_all = os.environ.get("TRANSLATE_ALL", "").lower() == "true"
    model = os.environ.get("TRANSLATE_MODEL", "openai/gpt-4.1-mini")

    if translate_all:
        changed_sources = {path.relative_to(repo_root) for path in supported_source_files(repo_root)}
        deleted_targets: set[Path] = set()
    else:
        changed_sources, deleted_targets = parse_changed_files(repo_root, before_sha, after_sha)

    skill_context = load_skill_context()
    system_prompt = build_system_prompt(skill_context)

    written_files: list[str] = []
    for rel_source in sorted(changed_sources):
        source_path = repo_root / rel_source
        target_rel = target_for_source(rel_source)
        existing_target = repo_root / target_rel

        source_markdown = source_path.read_text(encoding="utf-8")
        existing_translation = None
        if existing_target.exists():
            existing_translation = existing_target.read_text(encoding="utf-8")

        translation = request_translation(
            model=model,
            system_prompt=system_prompt,
            user_prompt=build_user_prompt(
                source_path=rel_source,
                source_markdown=source_markdown,
                existing_translation=existing_translation,
                source_diff=source_diff(repo_root, before_sha, after_sha, rel_source),
            ),
            github_token=github_token,
        )

        output_path = output_dir / target_rel
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(translation, encoding="utf-8")
        written_files.append(target_rel.as_posix())
        print(f"Translated {rel_source.as_posix()} -> {target_rel.as_posix()}")

    manifest = {
        "written": written_files,
        "deleted": sorted(path.as_posix() for path in deleted_targets),
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    translate_files()
