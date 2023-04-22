# -*- coding: utf-8 -*-

from pathlib import Path

dir_project_root = Path(__file__).absolute().parent.parent
dir_cache = dir_project_root.joinpath(".cache")

path_ts_data = Path(dir_project_root, f"cdkts-data.json")
path_ts_setting = Path(dir_project_root, f"cdkts-setting.json")

path_python_data = Path(dir_project_root, f"cdkpython-data.json")
path_python_setting = Path(dir_project_root, f"cdkpython-setting.json")
