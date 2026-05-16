import time
from timestitch import TimeStitch


def test_stamp_prepends_header():
    ts = TimeStitch(timezone="UTC")
    result = ts.stamp("hello")
    assert result.startswith("[TimeStitch |")
    assert "hello" in result


def test_stamp_tracks_delta():
    ts = TimeStitch(timezone="UTC")
    ts.stamp("first")
    time.sleep(1)
    result = ts.stamp("second")
    assert "Since last:" in result


def test_system_context():
    ts = TimeStitch(timezone="UTC")
    ctx = ts.system_context()
    assert "Current time:" in ctx
    assert "UTC" in ctx


def test_reset_session():
    ts = TimeStitch(timezone="UTC")
    ts.stamp("something")
    ts.reset_session()
    assert ts.last_message is None


def test_explicit_timezone():
    ts = TimeStitch(timezone="Europe/Berlin")
    result = ts.stamp("test")
    assert "Europe/Berlin" in result
