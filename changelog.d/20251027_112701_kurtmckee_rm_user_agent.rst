Breaking changes
----------------

*   feedparser no longer sends a default User-Agent header.
    In addition, the module-level ``feedparser.USER_AGENT`` variable
    has been removed and is no longer respected if set.

    feedparser can be used in violation of sites' Terms of Service,
    and the default User-Agent header incorrectly associated those violations
    with the project itself.

    It is not tenable to continue receiving notifications from large companies
    regarding usage violations that has nothing to do with this project
    and cannot be resolved by project maintainers,
    so there will no longer be a default User-Agent header
    that points at the project.

    As has been documented in this project for nearly 20 years,
    **developers are still encouraged to set an appropriate User-Agent**
    when making HTTP requests.
