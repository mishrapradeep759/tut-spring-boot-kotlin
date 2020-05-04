

uuid_regex = (
    "(%(hex)s{8}-%(hex)s{4}-%(hex)s{4}-%(hex)s{4}-%(hex)s{12})|(%(hex)s{32})"
    % {"hex": "[a-f0-9]"}
)