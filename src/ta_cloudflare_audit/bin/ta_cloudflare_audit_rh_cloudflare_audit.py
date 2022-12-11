
import ta_cloudflare_audit_declare

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    DataInputModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()


fields = [
    field.RestField(
        'interval',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.Pattern(
            regex=r"""(?:(?:^[3-9][0-9][0-9]$|^[1-9][0-9][0-9][0-9]\d*$)|(?:^\S+(?: \S+){4}))""",
        )
    ),
    field.RestField(
        'index',
        required=True,
        encrypted=False,
        default='default',
        validator=validator.String(
            min_len=1,
            max_len=80,
        )
    ),
    field.RestField(
        'cloudflare_credentials',
        required=True,
        encrypted=False,
        default=None,
        validator=None
    ),
    field.RestField(
        'backfill',
        required=False,
        encrypted=False,
        default='7',
        validator=None
    ),

    field.RestField(
        'disabled',
        required=False,
        validator=None
    )

]
model = RestModel(fields, name=None)


endpoint = DataInputModel(
    'cloudflare_audit',
    model,
)


if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
