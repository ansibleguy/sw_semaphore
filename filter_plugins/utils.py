from re import match as regex_match
from re import compile as regex_compile


class FilterModule(object):

    def filters(self):
        return {
            "json_bool": self.json_bool,
            "valid_hostname": self.valid_hostname,
        }

    @staticmethod
    def _valid_domain(name: str) -> bool:
        # see: https://validators.readthedocs.io/en/latest/_modules/validators/domain.html
        domain = regex_compile(
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
        )
        return domain.match(name) is not None

    @classmethod
    def valid_hostname(cls, name: str) -> bool:
        # see: https://en.wikipedia.org/wiki/Hostname#Restrictions_on_valid_host_names
        expr_hostname = r'^[a-zA-Z0-9-\.]{1,253}$'
        valid_hostname = regex_match(expr_hostname, name) is not None
        return all([cls._valid_domain(name), valid_hostname])

    @staticmethod
    def json_bool(b: bool) -> str:
        return 'true' if b else 'false'
