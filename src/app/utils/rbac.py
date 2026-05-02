def split_scope(scope: str) -> tuple[str, str]:
    subject, action = scope.split(":", maxsplit=1)
    return subject, action
