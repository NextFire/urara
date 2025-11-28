import os

from urara.client import client


def main():
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    assert TOKEN
    client.run(TOKEN, root_logger=True)


if __name__ == "__main__":
    main()
