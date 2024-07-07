#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Everytime.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django를 가져올 수 없습니다. Django가 설치되어 있는지 확인하거나, "
            "가상 환경을 활성화했는지 확인하세요."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()