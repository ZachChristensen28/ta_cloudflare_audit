
# encoding = utf-8

import datetime
import json
from requests.exceptions import HTTPError
from cloudflare_constants import *


def zts_logger(msg, action, event_type, stanza, **kwargs):
    """ To help with consistent logging format
    :param msg: message for log
    :param action: event outcome (started|success|failure|aborted)
    :param event_type: type of event
    :param stanza: stanza for event
    :param kwargs: any kv pair
    zts_logger(
            msg='message',
            action='success',
            event_type=event_type,
            stanza=stanza
        )
    """
    event_log = f'msg="{msg}", action="{action}", event_type="{event_type}", input_stanza="{stanza}"'
    for key, value in kwargs.items():
        event_log = event_log + f', {key}="{value}"'

    return event_log


def checkpointer(helper, account_name, set_checkpoint=False):
    """Checkpointer

    :param helper: Splunk add-on builder helper function
    :param account_name: account name from input stanza
    :param set_checkpoint: (Default False)
    """
    event_type = 'checkpointer'
    key = account_name

    if set_checkpoint:
        n = datetime.datetime.now(datetime.timezone.utc)
        helper.save_check_point(key, n.strftime(DEFAULT_TIME_FORMAT))
        event_log = zts_logger(
            msg='Updated checkpoint',
            action='success',
            event_type=event_type,
            stanza=account_name
        )
        helper.log_info(event_log)
        return True

    if helper.get_check_point(key):
        old_state = helper.get_check_point(key)
        event_log = zts_logger(
            msg='Checkpoint found',
            action='success',
            event_type=event_type,
            stanza=account_name
        )
        event_log_debug = zts_logger(
            msg='Checkpoint DEBUG',
            action='success',
            event_type=event_type,
            stanza=account_name,
            checkpoint_state=old_state
        )
        helper.log_info(event_log)
        helper.log_debug(event_log_debug)

        return old_state
    else:
        backfill = helper.get_arg('backfill')
        today = datetime.date.today()
        default_time = today - datetime.timedelta(days=int(backfill))
        last_time = default_time.strftime(DEFAULT_TIME_FORMAT)
        event_log = zts_logger(
            msg='Checkpoint not found, defaulting to {} days ago ({}).'.format(
                backfill, last_time),
            action='failure',
            event_type=event_type,
            stanza=account_name
        )
        helper.log_info(event_log)

        return last_time


def sendit(helper, url, method, verify, use_proxy, stanza, headers=None, payload=None, parameters=None,
           timeout=10):
    """ Sends HTTP request
    :param helper: Splunk add-on builder helper.
    :param url: URL to use in request.
    :param method: HTTP method to use in request.
    :param verify: True|False or a valid CA certificate.
    :param use_proxy: (bool) whether to use proxy settings.
    :param stanza: input stanza.
    :param headers: (optional) HTTP headers for request.
    :param payload: (optional) HTTP payload for request.
    :param parameters: (optional) HTTP parameters for request.
    :param timeout: (optional) connection timeout. Defaults to 10.
    """
    event_type = 'http_request'
    event_log = zts_logger(
        msg='Starting HTTP request',
        action='started',
        event_type=event_type,
        stanza=stanza,
        verify_certificate=verify
    )
    helper.log_info(event_log)

    try:
        r = helper.send_http_request(
            url=url,
            method=method,
            timeout=timeout,
            payload=payload,
            headers=headers,
            parameters=parameters,
            verify=verify,
            use_proxy=use_proxy
        )

        if r.status_code == 200:
            result = 'success'
            response = r.json()
            return result, response
        else:
            result = 'failure'
            message = zts_logger(
                msg='Request failed',
                action='failure',
                event_type=event_type,
                stanza=stanza,
                http_status=r.status_code,
                details=json.dumps(r.json())
            )
            return result, message

    except HTTPError as http_err:
        result = 'failure'
        message = zts_logger(
            msg='HTTP Error',
            action='failure',
            event_type=event_type,
            stanza=stanza,
            details=http_err
        )
        return result, message

    except Exception as e:
        result = 'failure'
        message = zts_logger(
            msg='Failed to make request',
            action='failure',
            event_type=event_type,
            stanza=stanza,
            http_status_code=r.status_code,
            details=e
        )
        return result, message
