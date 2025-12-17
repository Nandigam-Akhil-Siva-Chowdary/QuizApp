from django.utils import timezone
from datetime import timedelta


def seconds_between(start, end):
    """
    Return seconds between two datetimes.
    """
    if not start or not end:
        return 0
    delta = end - start
    return int(delta.total_seconds())


def add_minutes(dt, minutes):
    """
    Add minutes to a datetime safely.
    """
    if not dt:
        return None
    return dt + timedelta(minutes=minutes)


def now():
    """
    Wrapper for timezone.now()
    """
    return timezone.now()


def is_expired(start_time, duration_minutes):
    """
    Check if a duration (in minutes) has expired from start_time.
    """
    if not start_time:
        return True

    end_time = start_time + timedelta(minutes=duration_minutes)
    return timezone.now() >= end_time


def remaining_seconds(start_time, duration_minutes):
    """
    Return remaining seconds before expiry.
    """
    if not start_time:
        return 0

    end_time = start_time + timedelta(minutes=duration_minutes)
    remaining = (end_time - timezone.now()).total_seconds()
    return max(0, int(remaining))
