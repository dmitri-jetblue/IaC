from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, NewType

import yaml
from jinja2 import Environment, StrictUndefined, Template

DeviceData = NewType("DeviceData", dict[str, Any])


class JinjaTemplateRenderer:
    @classmethod
    def _set_template(cls, template: str) -> Template:
        env = Environment(
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        return env.from_string(template)

    @classmethod
    def render(cls, template: str, data: DeviceData) -> str:
        return cls._set_template(template).render(device=data)


def get_template(template_path: Path) -> str:
    return template_path.read_text(encoding="utf-8")


def get_device_data(data_path: Path) -> DeviceData:
    raw_data = data_path.read_text(encoding="utf-8")
    return DeviceData(yaml.safe_load(raw_data))


def main() -> None:
    template = get_template(template_path=Path(sys.argv[1]))
    data = get_device_data(data_path=Path(sys.argv[2]))
    print(JinjaTemplateRenderer.render(template, data))


if __name__ == "__main__":
    main()
