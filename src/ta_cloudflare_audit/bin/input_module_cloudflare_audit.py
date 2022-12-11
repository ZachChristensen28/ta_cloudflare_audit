
# encoding = utf-8

from cloudflare_helper import *


def validate_input(helper, definition):
    """Nothing to verify"""
    pass


def collect_events(helper, ew):
    log_level = helper.get_log_level()
    helper.set_log_level(log_level)

    cf_account = helper.get_arg('cloudflare_credentials')
    cf_token = cf_account['password']
    stanza = str(helper.get_input_stanza_names())

    proxy = helper.get_proxy()
    event_type = 'proxy_config'
    if proxy:
        if proxy["proxy_username"]:
            event_log = zts_logger(
                msg='Proxy is configured with authentication',
                action='success',
                event_type=event_type,
                stanza=stanza
            )
            helper.log_info(event_log)

        else:
            event_log = zts_logger(
                msg='Proxy is configured with no authentication',
                action='success',
                event_type=event_type,
                stanza=stanza
            )
            helper.log_info(event_log)

        proxy_config = True
    else:
        proxy_config = False

    def audit_logs():
        """Retrieve audit logs from Cloudflare"""
        event_type = 'input_get_audit_logs'
        event_log = zts_logger(
            msg='Starting event collection',
            action='started',
            event_type=event_type,
            stanza=stanza
        )
        helper.log_info(event_log)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(cf_token),
            "user-agent": 'Splunk-ta-cloudflare-audit'
        }

        last_time = checkpointer(helper, account_name=stanza)
        if last_time:
            params = {
                "since": last_time
            }
        else:
            params = None

        result, response_message = sendit(
            helper,
            CLOUDFLARE_AUDIT_URL,
            method='GET',
            verify=True,
            use_proxy=proxy_config,
            headers=headers,
            stanza=stanza,
            parameters=params
        )

        if result == 'success':
            checkpointer(helper, stanza, set_checkpoint=True)

            if not response_message['result']:
                event_log = zts_logger(
                        msg='No events found since last run ({})'.format(last_time),
                        action='aborted',
                        event_type=event_type,
                        stanza=stanza,
                        last_run_time=last_time
                )
                helper.log_info(event_log)
                return False

            event_log = zts_logger(
                msg='Collected audit events',
                action='success',
                event_type=event_type,
                stanza=stanza
            )
            helper.log_info(event_log)
        else:
            helper.log_error(response_message)
            return False

        event_count = 0
        for data in response_message['result']:
            event = helper.new_event(
                source=helper.get_input_type(),
                index=helper.get_output_index(),
                sourcetype=helper.get_sourcetype(),
                data=json.dumps(data)
            )
            ew.write_event(event)
            event_count += 1

        event_log = zts_logger(
            msg='Completed audit log collection',
            action='success',
            event_type=event_type,
            stanza=stanza,
            event_count=event_count
        )
        helper.log_info(event_log)

    # Get Audit Logs
    audit_logs()

