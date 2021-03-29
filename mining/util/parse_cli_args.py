import re
from typing import Optional, Tuple


def parse_time_unit(string: str) -> Optional[Tuple[int, str]]:
  matches = re.findall(r"(\d+)(s|m|h|d)", string)
  if len(matches):
    return (int(matches[0][0]), matches[0][1])
