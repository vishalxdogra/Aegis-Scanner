from dataclasses import dataclass, field
from typing import Dict, Optional, Callable


@dataclass
class AuthProfile:
    """
    Describes an authentication flow.
    This is CONFIG, not logic.
    """

    login_url: str
    method: str = "POST"  # GET / POST
    fields: Dict[str, str] = field(default_factory=dict)

    # Optional CSRF handling
    csrf_url: Optional[str] = None
    csrf_field: Optional[str] = None
    csrf_regex: Optional[str] = None

    # Success validation
    success_check: Optional[Callable[[str], bool]] = None