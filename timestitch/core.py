from datetime import datetime, timezone
import zoneinfo
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimeStamp:
    utc: datetime
    local: datetime
    tz_abbrev: str
    tz_iana: str
    session_start: datetime
    last_message: Optional[datetime]

    @property
    def session_duration(self) -> str:
        delta = self.utc - self.session_start
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

    @property
    def since_last(self) -> Optional[str]:
        if not self.last_message:
            return None
        delta = self.utc - self.last_message
        total_seconds = int(delta.total_seconds())
        if total_seconds < 1:
            return None
        minutes, seconds = divmod(total_seconds, 60)
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

    def format(self) -> str:
        utc_str = self.utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        local_str = self.local.strftime("%H:%M")
        base = (
            f"[TimeStitch | {utc_str} UTC | "
            f"{local_str} {self.tz_abbrev} ({self.tz_iana}) | "
            f"Session: {self.session_duration}"
        )
        if self.since_last:
            base += f" | Since last: {self.since_last}"
        return base + "]"


class TimeStitch:
    def __init__(self, timezone: str = None):
        """
        Initialize TimeStitch middleware.

        Args:
            timezone: IANA timezone string (e.g., 'Europe/Berlin').
                      Auto-detects from system if not provided.
        """
        self.session_start = datetime.now(tz=_utc())
        self.last_message = None

        if timezone:
            self.tz = zoneinfo.ZoneInfo(timezone)
            self.tz_iana = timezone
        else:
            self.tz, self.tz_iana = self._detect_timezone()

    def _detect_timezone(self):
        try:
            import tzlocal
            tz = tzlocal.get_localzone()
            return tz, str(tz)
        except ImportError:
            return zoneinfo.ZoneInfo("UTC"), "UTC"
        except Exception:
            return zoneinfo.ZoneInfo("UTC"), "UTC"

    def _get_timestamp(self) -> TimeStamp:
        now_utc = datetime.now(tz=_utc())
        now_local = now_utc.astimezone(self.tz)
        tz_abbrev = now_local.strftime("%Z")
        ts = TimeStamp(
            utc=now_utc,
            local=now_local,
            tz_abbrev=tz_abbrev,
            tz_iana=self.tz_iana,
            session_start=self.session_start,
            last_message=self.last_message,
        )
        self.last_message = now_utc
        return ts

    def stamp(self, message: str) -> str:
        """
        Attach a temporal sticky note to a message.

        Args:
            message: The original message text.

        Returns:
            Message with TimeStitch header prepended.
        """
        ts = self._get_timestamp()
        return f"{ts.format()}\n{message}"

    def system_context(self) -> str:
        """
        Generate a one-line time context string for system prompts.
        Use once at session initialization to avoid breaking prefix caching.

        Returns:
            Formatted time context string.
        """
        now_utc = datetime.now(tz=_utc())
        now_local = now_utc.astimezone(self.tz)
        tz_abbrev = now_local.strftime("%Z")
        utc_str = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        local_str = now_local.strftime("%H:%M")
        return (
            f"Current time: {local_str} {tz_abbrev} "
            f"({self.tz_iana}) | UTC: {utc_str}"
        )

    def reset_session(self):
        """Reset session timer. Call when starting a new conversation."""
        self.session_start = datetime.now(tz=_utc())
        self.last_message = None


def _utc():
    return timezone.utc
