# efb-wechat-docker-itchat-uos

将微信中的聊天消息转发到telegram :drooling_face:

好处:
- 可以完全关闭手机上的微信应用（禁用android上微信的自启权限，禁止微信后台运行）。android国产rom上如何开启telegram通知[参考1](https://www.v2ex.com/t/831069) [参考 2](https://github.com/kooritea/fcmfix)

**注意:**
  - **使用该项目，微信有被封禁风险，请自行判断是否使用** [参考1](https://github.com/why2lyj/ItChat-UOS#%E6%9B%B4%E6%96%B0---20230210) [参考2](https://github.com/HoganGolden/efb-wechat-slave-itchat-uos#%E4%BD%BF%E7%94%A8%E5%89%8D%E9%A1%BB%E7%9F%A5)
  - 如何减少封禁：项目尽量部署在你的本地(本市范围)，如家里的树莓派等。并为该本地的网络环境配置可以访问telegram的代理。代理配置[参考FQA](#FQA)

# docker image
点击下面图标，跳转到docker hub 

[![docker: image size](https://img.shields.io/docker/image-size/hogangolden/efb-wechat)](https://hub.docker.com/r/hogangolden/efb-wechat)

## 鸣谢
* [efb-wechat-docker](https://github.com/haukeng/efb-wechat-docker)
* [ehForwarderBot](https://github.com/ehForwarderBot)
* [ItChat-UOS](https://github.com/why2lyj/ItChat-UOS)

EFB Docker image with:
* [efb-telegram-master](https://github.com/ehForwarderBot/efb-telegram-master)
* [efb-wechat-slave-itchat-uos](https://github.com/HoganGolden/efb-wechat-slave-itchat-uos)
* [efb-patch-middleware-itchat-uos](https://github.com/HoganGolden/efb-patch-middleware-itchat-uos)
* [efb-search_msg-middleware](https://github.com/ehForwarderBot/efb-search_msg-middleware)

## Features

- Container run by non-root user.
- Support add environment variables `PROXY_URL`, `PROXY_USER`, and `PROXY_PASS` to use proxy for ETM.
- Integrate [efb-patch-middleware-itchat-uos](https://github.com/HoganGolden/efb-wechat-slave-itchat-uos) and [efb-search_msg-middleware](https://github.com/ehForwarderBot/efb-search_msg-middleware) by default.

## Build

### Use GitHub Action pre-build image

```shell
docker pull hogangolden/efb-wechat
```

### Build image manually

```shell
git clone https://github.com/HoganGolden/efb-wechat-docker-itchat-uos.git
cd efb-wechat-docker-itchat-uos && docker build -t hogangolden/efb-wechat efb-wechat
```

## Usage

### Step 0

Create a Telegram Bot by talking to [@BotFather](https://t.me/botfather) and it will give you the Bot Token

Get your Telegram ID (**Not username**) from [@getidsbot](https://t.me/getidsbot)

### Step 1

**If you prefer to use docker.**

```shell
# Create volumes
docker volume create efb-wechat-data

# Run 
docker run -d -t \
--name "efb-wechat" \
-e BOT_TOKEN=xxxx \
-e BOT_ADMIN=xxxx \
-v efb-wechat-data:/home/efb/efb_config/profiles/default \
hogangolden/efb-wechat
```

(**Required**) Use your Telegram Bot Token as `BOT_TOKEN` and your Telegram ID as `BOT_ADMIN`

**If you prefer to use docker-compose.**

```shell
mkdir efb-wechat && cd efb-wechat
wget https://raw.githubusercontent.com/HoganGolden/efb-wechat-docker-itchat-uos/main/docker-compose.yml -O docker-compose.yml
```

(**Required**) Modify the environment variables by editing docker-compose.yml, and then:

```shell
docker-compose up -d
```
raspberry pi os
```shell
docker compose up -d
```

### Step 2

```shell
docker logs --tail=200 -f efb-wechat 
# Ctrl + C to quit after your log in
```

Scan the QR code to log in

## Configuration Options

`BOT_TOKEN`

> (**Required**) Your Telegram bot token.

`BOT_ADMIN`

> (**Required**) Your Telegram account id.

`PROXY_URL`

> (Optional) Proxy url use to connect Telegram by network proxy.
>
> Supported both `http` and `socks5` proxy.
>
> For example: `http://172.17.0.1:1080`

`PROXY_USER`

> (Optional) Use for proxy authentication

`PROXY_PASS`

> (Optional) Use for roxy authentication

`SEND_IMAGE_AS_FILE`

> (Optional) Set the value to `0` to **disable** send all image messages as files (preventing Telegram’s image compression).
>
> _Enabled by default._

`ANIMATED_STICKERS`

> (Optional) Set the value to `0` to **disable** support to animated stickers.
>
> _Enabled by default._

`MESSAGE_MUTED_ON_SLAVE`

> (Optional) Behavior when a message received is muted on slave channel platform. Availiable value: `normal`, `silent` and `mute`. Go to [ehForwarderBot/efb-telegram-master](https://github.com/ehForwarderBot/efb-telegram-master#experimental-flags) to get more information.
>
> _`normal` is the default value_

`YOUR_MESSAGE_ON_SLAVE`

> (Optional) Behavior when a message received is from you on slave channel platform. Availiable value: `normal`, `silent` and `mute`. Go to [ehForwarderBot/efb-telegram-master](https://github.com/ehForwarderBot/efb-telegram-master#experimental-flags) to get more information.
>
> _`silent` is the default value_

`MP_GROUP_ID`

> (Optional) Telegram group id for forwarding every public account message to it. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.

`AUTO_MARK_AS_READ`

> (Optional) Set the value to `0` to **disable** auto mark as read in wechat phone client. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.
>
> _Enabled by default._

`REMOVE_EMOJI_IN_TITLE`

> (Optional) Set the value to `0` to **disable**  remove emoji in telegram group title. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.
>
> _Enabled by default._

`STRIKETHROUGH_RECALL_MSG`

> (Optional) Set the value to `0` to **disable** strikethrough instead of replying to a recall message. Go to [efb-patch-middleware](https://github.com/ehForwarderBot/efb-patch-middleware#usage) to get more information.
>
> _Enabled by default._

## FQA

### How to use host machine proxy?

Try to set `PROXY_URL` as `http://172.17.0.1:YOUR_PORT` (Socks5 works as well)

* 本人使用[xray](https://github.com/XTLS/Xray-core)客户端做代理，需要配置为：大陆ip和域名直连，外网地址通过代理访问。客户端routing部分的配置参考如下：
```json
{
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      {
        "type": "field",
        "outboundTag": "direct",
        "domain": [
          "geosite:cn",
          "geosite:private"
        ]
      },
      {
        "type": "field",
        "outboundTag": "direct",
        "ip": [
          "geoip:private",
          "geoip:cn"
        ]
      }
    ]
  }
}
```

## [EFB 框架及各组件常见问题](https://github.com/ehForwarderBot/efb-wechat-slave/wiki/EFB%E2%80%86%E6%A1%86%E6%9E%B6%E5%8F%8A%E5%90%84%E7%BB%84%E4%BB%B6%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)

## [efb-telegram-master usage](https://github.com/ehforwarderbot/efb-telegram-master/#usage)
ETM offers the following commands, you can also send it
to BotFather for a command list::

    help - Show commands list.
    link - Link a remote chat to a group.
    unlink_all - Unlink all remote chats from a group.
    info - Display information of the current Telegram chat.
    chat - Generate a chat head.
    extra - Access additional features from Slave Channels.
    update_info - Update info of linked Telegram group.
    react - Send a reaction to a message, or show a list of reactors.
    rm - Remove a message from its remote chat.

## LICENSE
MIT
