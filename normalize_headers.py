from pathlib import Path
import re


TEMPLATES_DIR = Path("templates")


def build_replacement(indent: str, back_expr: str | None, aria_label: str | None) -> str:
    lines: list[str] = []

    if not back_expr:
        lines.append(f"{indent}{{% include 'includes/global_header.html' %}}")
        return "\n".join(lines)

    url_name_match = re.fullmatch(r"\{% url '([^']+)' %\}", back_expr)
    if url_name_match:
        lines.append(f"{indent}{{% with header_back_url='{url_name_match.group(1)}' %}}")
        if aria_label and aria_label != "Назад":
            lines.append(f'{indent}{{% with header_back_aria_label="{aria_label}" %}}')
            lines.append(f"{indent}{{% include 'includes/global_header.html' %}}")
            lines.append(f"{indent}{{% endwith %}}")
        else:
            lines.append(f"{indent}{{% include 'includes/global_header.html' %}}")
        lines.append(f"{indent}{{% endwith %}}")
        return "\n".join(lines)

    dyn_match = re.fullmatch(r"\{% url '([^']+)' (.+) %\}", back_expr)
    if dyn_match:
        url_name, url_args = dyn_match.groups()
        lines.append(f"{indent}{{% url '{url_name}' {url_args} as header_back_href %}}")
        if aria_label and aria_label != "Назад":
            lines.append(f'{indent}{{% with header_back_aria_label="{aria_label}" %}}')
            lines.append(f"{indent}{{% include 'includes/global_header.html' %}}")
            lines.append(f"{indent}{{% endwith %}}")
        else:
            lines.append(f"{indent}{{% include 'includes/global_header.html' %}}")
        return "\n".join(lines)

    lines.append(f"{indent}{{% include 'includes/global_header.html' %}}")
    return "\n".join(lines)


def replace_header_blocks() -> None:
    for path in sorted(TEMPLATES_DIR.glob("*.html")):
        if path.name == "home.html":
            continue

        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?ms)^([ \t]*)<header class=\"header\">.*?</header>", text)
        if not match:
            continue

        header_block = match.group(0)
        indent = match.group(1)

        back_match = re.search(r"href=\"(\{% url [^\"]+%\})\" class=\"back-btn\"", header_block)
        aria_match = re.search(r'class=\"back-btn\" aria-label=\"([^\"]+)\"', header_block)

        back_expr = back_match.group(1) if back_match else None
        aria_label = aria_match.group(1) if aria_match else None
        replacement = build_replacement(indent, back_expr, aria_label)
        text = text[:match.start()] + replacement + text[match.end():]
        path.write_text(text, encoding="utf-8")


def normalize_existing_include_blocks() -> None:
    simple_pattern = re.compile(
        r"(?m)^([ \t]*)\{% with header_back_href=\{% url '([^']+)' %\} %\}\n"
        r"\1\{% include 'includes/global_header\.html' %\}\n"
        r"\1\{% endwith %\}"
    )
    dynamic_pattern = re.compile(
        r"(?m)^([ \t]*)\{% with header_back_href=\{% url '([^']+)' (.+?) %\} %\}\n"
        r"\1\{% include 'includes/global_header\.html' %\}\n"
        r"\1\{% endwith %\}"
    )
    dynamic_with_aria_pattern = re.compile(
        r"(?m)^([ \t]*)\{% with header_back_href=\{% url '([^']+)' (.+?) %\} %\}\n"
        r"\1\{% with header_back_aria_label=\"([^\"]+)\" %\}\n"
        r"\1\{% include 'includes/global_header\.html' %\}\n"
        r"\1\{% endwith %\}\n"
        r"\1\{% endwith %\}"
    )

    for path in sorted(TEMPLATES_DIR.glob("*.html")):
        text = path.read_text(encoding="utf-8")

        text = dynamic_with_aria_pattern.sub(
            lambda m: (
                f"{m.group(1)}{{% url '{m.group(2)}' {m.group(3)} as header_back_href %}}\n"
                f'{m.group(1)}{{% with header_back_aria_label="{m.group(4)}" %}}\n'
                f"{m.group(1)}{{% include 'includes/global_header.html' %}}\n"
                f"{m.group(1)}{{% endwith %}}"
            ),
            text,
        )

        text = dynamic_pattern.sub(
            lambda m: (
                f"{m.group(1)}{{% url '{m.group(2)}' {m.group(3)} as header_back_href %}}\n"
                f"{m.group(1)}{{% include 'includes/global_header.html' %}}"
            ),
            text,
        )

        text = simple_pattern.sub(
            lambda m: (
                f"{m.group(1)}{{% with header_back_url='{m.group(2)}' %}}\n"
                f"{m.group(1)}{{% include 'includes/global_header.html' %}}\n"
                f"{m.group(1)}{{% endwith %}}"
            ),
            text,
        )

        path.write_text(text, encoding="utf-8")


def tweak_theme_toggle() -> None:
    path = TEMPLATES_DIR / "theme_head.html"
    text = path.read_text(encoding="utf-8")

    text = text.replace(
        """    .header-top .theme-toggle {
        margin-left: 10px;
        transform: translateY(0);
    }""",
        """    .header-top .theme-toggle {
        margin-left: 14px;
        transform: translateY(2px);
    }""",
    )

    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    replace_header_blocks()
    normalize_existing_include_blocks()
    tweak_theme_toggle()
