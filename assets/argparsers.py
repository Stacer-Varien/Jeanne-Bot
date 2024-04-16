import argparse
import random

from discord import Role

combined_parser=argparse.ArgumentParser(add_help=False)
hentai_parser = argparse.ArgumentParser(add_help=False)
inv_parser = argparse.ArgumentParser(add_help=False)
manage_parser = argparse.ArgumentParser(add_help=False)
mod_parser = argparse.ArgumentParser(add_help=False)

# fun
combined_parser.add_argument(
"--first",
"-f",
type=str,
help="FIRST WORD",
required=False,
nargs="+",
default=None,
)
combined_parser.add_argument(
"--second",
"-s",
type=str,
help="SECOND WORD",
required=False,
nargs="+",
default=None,
)

# Hentai module
hentai_parser.add_argument(
"--rating",
"-r",
type=str,
choices=["questionable", "explicit", "e", "q"],
help="questionable | explicit | q | e",
required=False,
default=random.choice(["questionable", "explicit"]),
)
hentai_parser.add_argument(
"--tags", "-t", type=str, nargs="+", required=False, default=[], help="tags"
)
hentai_parser.add_argument(
"--plus", "-p", action="store_true", help="Enable plus mode. Just type '-p'"
)

# inventory
inv_parser.add_argument(
"--name",
type=str,
help="NAME",
nargs="+",
required=False,
default=None
)
inv_parser.add_argument("--link", type=str, help="LINK", required=False, default=None)

# manage module
manage_parser.add_argument(
"-t",
"--topic",
type=str,
help="topic",
nargs="+",
required=False,
default=None,
)
manage_parser.add_argument(
"-cat",
"--category",
type=str,
help="category",
nargs="+",
required=False,
default=None,
)

manage_parser.add_argument(
"-nsfw", action="store_true", help="Enable NSFW. Just type '-nsfw"
)


manage_parser.add_argument(
"-c",
"--color",
type=str,
help="color",
nargs="+",
required=False,
default=None,
)
manage_parser.add_argument(
"-h",
"--hoisted",
help="Make it hoisted. Just type -h",
action="store_true",
required=False,
)

manage_parser.add_argument(
"--mentioned",
help="Make it mentionable. Just type --mentioned",
action="store_true",
required=False,
)

manage_parser.add_argument(
"-ch",
"--channel",
type=str,
help="CHANNEL",
nargs="+",
required=False,
)
manage_parser.add_argument(
"-msg",
"--message",
type=int,
help="MESSAGE ID",
required=False,
)
manage_parser.add_argument(
"-s",
"-slow",
"--slowmode",
type=str,
help="SLOWMODE",
nargs="+",
required=False,
default=None,
)
manage_parser.add_argument(
"-d",
"-desc",
"--description",
type=str,
help="DESCRIPTION",
nargs="+",
required=False,
default=None,
)
manage_parser.add_argument(
"-v",
"--verification",
type=str,
help="VERIFICATION LEVEL",
choices=["none", "low", "medium", "high", "highest"],
required=False,
default=None,
)

manage_parser.add_argument(
"-w",
"--welcomer",
type=str,
help="WELCOMER",
nargs="+",
required=False,
default=None,
)

manage_parser.add_argument(
"-l",
"--leaving",
type=str,
help="LEAVING",
nargs="+",
required=False,
default=None,
)
manage_parser.add_argument(
    "-r",
    "--role",
    help="ROLE",
    nargs="+",
    required=False,
    default=None,
)

# moderation
mod_parser.add_argument(
    "-uid",
    "--userid",
    "-m",
    "--member",
    type=str,
    help="USER ID | MEMBER NAME | MEMBER GLOBAL NAME",
    nargs="+",
    required=False,
    default=None,
)
mod_parser.add_argument(
    "-r",
    "--reason",
    type=str,
    help="REASON",
    nargs="+",
    required=False,
    default="Unspecified",
)


mod_parser.add_argument(
    "--time",
    type=str,
    help="TIME",
    nargs="+",
    required=False,
    default=None,
)

mod_parser.add_argument(
    "-uids",
    "--users",
    "-ids",
    type=str,
    help="USER IDS",
    nargs="+",
    required=False,
    default=None,
)
