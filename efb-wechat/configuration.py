#!/usr/bin/env python3
from os import environ
from re import fullmatch
from ruamel.yaml import YAML


def get_file_path():
    if environ.get("ETM_CONFIG") is None:
        print("The environment variable ETM_CONFIG must be set!")
        exit(1)
    elif fullmatch("^\/(?:[^/]+\/)*[^/]+$", environ.get("ETM_CONFIG")) is None:
        print("The ETM config file path format isn't validated.")
        exit(1)
    else:
        print("The ETM config file path format is validated.")
        return environ.get("ETM_CONFIG")


def get_bot_config():
    if environ.get("BOT_TOKEN") is None:
        print("The environment variable BOT_TOKEN must be set!")
        exit(1)
    elif fullmatch("^[0-9]*:[a-zA-Z0-9_-]{35}$", environ.get("BOT_TOKEN")) is None:
        print("The bot token format isn't validated, please check it.")
        exit(1)
    elif environ.get("BOT_ADMIN") is None:
        print("The environment variable BOT_ADMIN must be set!")
        exit(1)
    elif fullmatch("^[0-9]*$", environ.get("BOT_ADMIN")) is None:
        print("The bot admin id format isn't validated, please check it.")
        exit(1)
    else:
        print("The bot token and bot admin id format is validated.")
        return {
            "bot_token": environ.get("BOT_TOKEN"),
            "bot_admin": int(environ.get("BOT_ADMIN")),
        }


def get_proxy_config():
    if environ.get("PROXY_URL") is None:
        print("You do not use network proxy.")
        return {}
    elif fullmatch("^(http|socks5):\/\/.*:\d{1,5}$", environ.get("PROXY_URL")) is None:
        print("Your proxy url format isn't validated, please check it.")
        exit(1)
    elif environ.get("PROXY_USER") is None or environ.get("PROXY_PASS") is None:
        print(
            "You will use "
            + environ.get("PROXY_URL")
            + " as your network proxy, and it don't require authentication."
        )
        return {"proxy_url": environ.get("PROXY_URL")}
    elif (
        fullmatch("^(http|socks5):\/\/.*:\d{1,5}$", environ.get("PROXY_URL")).group(1)
        == "http"
    ):
        print(
            "You will use "
            + environ.get("PROXY_URL")
            + " as your network proxy, and it require authentication."
        )
        return {
            "proxy_url": environ.get("PROXY_URL"),
            "proxy_user": environ.get("PROXY_USER"),
            "proxy_pass": environ.get("PROXY_PASS"),
        }
    elif (
        fullmatch("^(http|socks5):\/\/.*:\d{1,5}$", environ.get("PROXY_URL")).group(1)
        == "socks5"
    ):
        print(
            "You will use "
            + environ.get("PROXY_URL")
            + " as your network proxy, and it require authentication."
        )
        return {
            "proxy_url": environ.get("PROXY_URL"),
            "urllib3_proxy_kwargs": {
                "proxy_user": environ.get("PROXY_USER"),
                "proxy_pass": environ.get("PROXY_PASS"),
            },
        }
    else:
        print("Someting wrong!")


def get_mp_telegram_group_id():
    if environ.get("MP_GROUP_ID") is None:
        print("You do not use Telegram group to forward WeChat public account message.")
        return 0
    elif fullmatch("^\-[0-9]*$", environ.get("MP_GROUP_ID")) is None:
        print("Your Telegram group id didn't match the rule, please check it.")
        exit(1)
    else:
        print(
            "You will use a Telegram group that id is "
            + environ.get("MP_GROUP_ID")
            + " to forward WeChat public account message."
        )
        return int(environ.get("MP_GROUP_ID"))


def main():
    file_path = get_file_path()
    bot_config = get_bot_config()
    proxy_config = get_proxy_config()
    mp_telegram_group_id = get_mp_telegram_group_id()

    yaml = YAML()
    yaml.indent(mapping=2, sequence=2, offset=0)
    with open(file_path) as fo:
        config = yaml.load(fo)
    fo.close()

    config["token"] = bot_config["bot_token"]
    config["admins"][0] = bot_config["bot_admin"]
    config["request_kwargs"] = proxy_config

    if "tg_mp" in config and mp_telegram_group_id >= 0:
        del config["tg_mp"]
    else:
        config["tg_mp"] = mp_telegram_group_id

    with open(file_path, "w") as fw:
        yaml.dump(config, fw)
    fw.close()


if __name__ == "__main__":
    main()
