#!/usr/bin/env python
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quizapp.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Set default port to 8080 for runserver command
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        # Check if port is already specified (either as "port" or "ip:port")
        port_specified = False
        if len(sys.argv) > 2:
            # Check if second argument is a port number or contains ":"
            second_arg = sys.argv[2]
            if ":" in second_arg or second_arg.isdigit():
                port_specified = True
        
        if not port_specified:
            sys.argv.append("8080")
    
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()


