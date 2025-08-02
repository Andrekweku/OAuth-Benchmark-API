from dataclasses import dataclass
import secrets


@dataclass
class OAuthSession:
    provider: str
    state: str
    start_time: float


sessions = {}


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def store_session(state: str, provider: str, start_time: float):
    sessions[state] = OAuthSession(
        provider=provider, state=state, start_time=start_time
    )


def get_session(state: str) -> OAuthSession:
    return sessions.get(state)


def clear_session(state: str):
    if state in sessions:
        del sessions[state]
