#!/usr/bin/env python3
from os import getenv
from os import path
from re import fullmatch
from ruamel.yaml import YAML


class bcolors:
    OK = "\033[36m"
    WARN = "\33[33m"
    FAIL = "\033[33m"
    ENDC = "\033[0m"


def config_validator(value: str, _type="OTHER") -> bool:
    if _type == "BOT_TOKEN":
        if fullmatch("^[0-9]*:[a-zA-Z0-9_-]{35}$", value) is None:
            return False
        return True
    elif _type == "BOT_ADMIN":
        admins_list = value.split("#")
        if len(admins_list[0]) == 0:
            return False
        else:
            for id in admins_list:
                if fullmatch("^[0-9]*$", id) is None:
                    return False
            return True
    elif _type == "PROXY_URL":
        if fullmatch("^(http|socks5):\/\/.*:\d{1,5}$", value) is None:
            return False
        return True
    elif _type == "MP_GROUP_ID":
        if fullmatch("^\-[0-9]*$", value) is None:
            return False
        return True
    elif _type == "BOOL_NUM":
        if fullmatch("^(0|1)$", value) is None:
            return False
        return True
    elif _type == "MESSAGE_NOTICE":
        if fullmatch("^(normal|silent|mute)$", value.lower()) is None:
            return False
        return True
    elif _type == "OTHER":
        if len(value) == 0:
            return False
        return True
    else:
        return False


def get_etm_config():
    etm_config = {}
    etm_config_flags = {
        "send_image_as_file": True,
        "animated_stickers": True,
        "message_muted_on_slave": "normal",
        "your_message_on_slave": "silent",
    }

    bot_token = getenv("BOT_TOKEN", "")
    bot_admin = getenv("BOT_ADMIN", "")
    proxy_url = getenv("PROXY_URL", "")
    proxy_user = getenv("PROXY_USER", "")
    proxy_pass = getenv("PROXY_PASS", "")
    mp_group_id = getenv("MP_GROUP_ID", "")
    send_image_as_file = getenv("SEND_IMAGE_AS_FILE", "")
    animated_stickers = getenv("ANIMATED_STICKERS", "")
    message_muted_on_slave = getenv("MESSAGE_MUTED_ON_SLAVE", "")
    your_message_on_slave = getenv("YOUR_MESSAGE_ON_SLAVE", "")

    if config_validator(bot_token, "BOT_TOKEN"):
        etm_config["token"] = bot_token
        print(bcolors.OK + "The bot token check passed." + bcolors.ENDC)
    else:
        print(
            bcolors.FAIL
            + "The bot token isn't validated, please check it."
            + bcolors.ENDC
        )
        exit(1)

    if config_validator(bot_admin, "BOT_ADMIN"):
        etm_config["admins"] = [int(x) for x in bot_admin.split("#")]
        print(bcolors.OK + "The bot admin list check passed." + bcolors.ENDC)
    else:
        print(
            bcolors.FAIL
            + "The bot admin list isn't validated, please check it."
            + bcolors.ENDC
        )
        exit(1)

    if (
        config_validator(proxy_url, "PROXY_URL")
        and config_validator(proxy_user)
        and config_validator(proxy_pass)
    ):
        proxy_method = fullmatch("^(http|socks5):\/\/.*:\d{1,5}$", proxy_url).group(1)
        if proxy_method == "http":
            etm_config["request_kwargs"] = {
                "proxy_url": proxy_url,
                "proxy_user": proxy_user,
                "proxy_pass": proxy_pass,
            }
            print(
                bcolors.OK
                + "You are using http proxy with authentication."
                + bcolors.ENDC
            )
        elif proxy_method == "socks5":
            etm_config["request_kwargs"] = {
                "proxy_url": proxy_url,
                "urllib3_proxy_kwargs": {
                    "proxy_user": proxy_user,
                    "proxy_pass": proxy_pass,
                },
            }
            print(
                bcolors.OK
                + "You are using socks5 proxy with authentication."
                + bcolors.ENDC
            )
        else:
            print(
                bcolors.FAIL
                + "The proxy method is "
                + proxy_method
                + " and it was unsupported."
                + bcolors.ENDC
            )
            exit(1)
    elif config_validator(proxy_url, "PROXY_URL"):
        etm_config["request_kwargs"] = {"proxy_url": proxy_url}
        print(bcolors.OK + "You are using proxy without authentication." + bcolors.ENDC)
    else:
        print(
            bcolors.WARN
            + "You don't use any proxy at all, make sure you can access telegram by direct!"
            + bcolors.ENDC
        )

    if config_validator(mp_group_id, "MP_GROUP_ID"):
        print(
            bcolors.WARN
            + "All messages from WeChat Official Account will be forward to the Group "
            + mp_group_id
            + bcolors.ENDC
        )
        etm_config["tg_mp"] = int(mp_group_id)
    else:
        print(
            bcolors.OK
            + "You message from WeChat Official Account will not be forward to the Group."
            + bcolors.ENDC
        )

    if config_validator(send_image_as_file, "BOOL_NUM"):
        etm_config_flags["send_image_as_file"] = bool(int(send_image_as_file))

    if config_validator(animated_stickers, "BOOL_NUM"):
        etm_config_flags["animated_stickers"] = bool(int(animated_stickers))

    if config_validator(message_muted_on_slave, "MESSAGE_NOTICE"):
        etm_config_flags["message_muted_on_slave"] = message_muted_on_slave.lower()

    if config_validator(your_message_on_slave, "MESSAGE_NOTICE"):
        etm_config_flags["your_message_on_slave"] = your_message_on_slave.lower()

    etm_config["flags"] = etm_config_flags
    return etm_config


def get_efb_patch_config():
    efb_patch_config = {
        "auto_mark_as_read": True,
        "remove_emoji_in_title": True,
        "strikethrough_recall_msg": True,
    }

    auto_mark_as_read = getenv("AUTO_MARK_AS_READ", "")
    remove_emoji_in_title = getenv("REMOVE_EMOJI_IN_TITLE", "")
    strikethrough_recall_msg = getenv("STRIKETHROUGH_RECALL_MSG", "")

    if config_validator(auto_mark_as_read, "BOOL_NUM"):
        efb_patch_config["auto_mark_as_read"] = bool(int(auto_mark_as_read))

    if config_validator(remove_emoji_in_title, "BOOL_NUM"):
        efb_patch_config["remove_emoji_in_title"] = bool(int(remove_emoji_in_title))

    if config_validator(strikethrough_recall_msg, "BOOL_NUM"):
        efb_patch_config["strikethrough_recall_msg"] = bool(
            int(strikethrough_recall_msg)
        )

    return efb_patch_config


def main():
    etm_config = get_etm_config()
    efb_patch_config = get_efb_patch_config()

    etm_config_path = "efb_config/profiles/default/blueset.telegram/config.yaml"
    efb_patch_config_path = (
        "efb_config/profiles/default/patch.PatchMiddleware/config.yaml"
    )

    yaml = YAML()
    yaml.indent(mapping=2, sequence=2, offset=0)
    with open(path.join(path.dirname(__file__), etm_config_path), "w") as fw_etm_config:
        yaml.dump(etm_config, fw_etm_config)

    with open(
        path.join(path.dirname(__file__), efb_patch_config_path), "w"
    ) as fw_efb_patch_config:
        yaml.dump(efb_patch_config, fw_efb_patch_config)


if __name__ == "__main__":
    main()
