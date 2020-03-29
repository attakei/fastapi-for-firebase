"""Cache management on Firebase Hosting.

Cloud Run response caching on Firebase Hosting.
https://firebase.google.com/docs/hosting/manage-cache
"""
from dataclasses import dataclass


@dataclass
class CacheControl:
    """Cache-Control header object.
    """

    max_age: int = 0
    s_maxage: int = 0

    @property
    def header_name(self) -> str:
        return "Cache-Control"

    @property
    def header_value(self) -> str:
        """Header value from object attribute.

        If you use this class, on default value set "public".
        """
        val = "public"
        if self.max_age and self.max_age > 0:
            val += f", max-age={self.max_age}"
        if self.s_maxage and self.s_maxage > 0:
            val += f", s-maxage={self.s_maxage}"
        return val
