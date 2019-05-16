# _*_coding:utf-8_*_
import re

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    # domain
    r")@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)"
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
    re.IGNORECASE)  # literal form, ipv4 address (SMTP 4.1.3)

mobile_re = re.compile(r"^0?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$")


def check_re(str, xx_re):
    if xx_re.match(str):
        return True
    return False


def check_email(email):
    return check_re(email, email_re)


def check_mobile(mobile):
    return check_re(mobile, mobile_re)
