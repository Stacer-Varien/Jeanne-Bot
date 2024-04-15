import argparse
import random

parser=argparse.ArgumentParser(add_help=False)

# fun
parser.add_argument(
"--first",
"-f",
type=str,
help="First Word",
required=False,
nargs="+",
default=None,
)
parser.add_argument(
"--second",
"-s",
type=str,
help="Second Word",
required=False,
nargs="+",
default=None,
)

# Hentai module
parser.add_argument(
"--rating",
"-r",
type=str,
choices=["questionable", "explicit", "e", "q"],
help="questionable | explicit | q | e",
required=False,
default=random.choice(["questionable", "explicit"]),
)
parser.add_argument(
"--tags", "-t", type=str, nargs="+", required=False, default=[], help="tags"
)
parser.add_argument(
"--plus", "-p", action="store_true", help="Enable plus mode. Just type '-p'"
)

# inventory
parser.add_argument(
"--name",
type=str,
help="NAME",
nargs="+",
required=False,
default=None
)
parser.add_argument("--link", type=str, help="LINK", required=False, default=None)

# manage module
parser.add_argument(
"-t",
"--topic",
type=str,
help="topic",
nargs="+",
required=False,
default=None,
)
parser.add_argument(
"-cat",
"--category",
type=str,
help="category",
nargs="+",
required=False,
default=None,
)
parser.add_argument(
"-slow",
"--slowmode",
type=str,
help="slowmode",
nargs="+",
required=False,
default=None,
)
parser.add_argument(
"-nsfw", action="store_true", help="Enable NSFW. Just type '-nsfw"
)

parser.add_argument(
"-u",
"--users",
type=int,
help="USERS",
required=False,
default=None,
)


parser.add_argument(
"-u",
"--users",
type=int,
help="users",
required=False,
default=None,
)
parser.add_argument(
"-c",
"--color",
type=str,
help="color",
nargs="+",
required=False,
default=None,
)
parser.add_argument(
"-h",
"--hoisted",
help="Make it hoisted. Just type -h",
action="store_true",
required=False,
)

parser.add_argument(
"-m",
"--mentioned",
help="Make it mentionable. Just type -m",
action="store_true",
required=False,
)

parser.add_argument(
"-ch",
"--channel",
type=str,
help="CHANNEL",
nargs="+",
required=False,
)
parser.add_argument(
"-msg",
"--message",
type=int,
help="MESSAGE ID",
required=False,
)
parser.add_argument(
"-s",
"--slowmode",
type=str,
help="SLOWMODE",
nargs="+",
required=False,
default=None,
)
parser.add_argument(
"-d",
"-desc",
"--description",
type=str,
help="DESCRIPTION",
nargs="+",
required=False,
default=None,
)
parser.add_argument(
"-v",
"--verification",
type=str,
help="VERIFICATION LEVEL",
choices=["none", "low", "medium", "high", "highest"],
required=False,
default=None,
)

parser.add_argument(
"-w",
"--welcomer",
type=str,
help="WELCOMER",
nargs="+",
required=False,
default=None,
)

parser.add_argument(
"-l",
"--leaving",
type=str,
help="LEAVING",
nargs="+",
required=False,
default=None,
)

#moderation
parser.add_argument(
    "-u",
    "--user",
    "-m",
    "--member",
    type=str,
    help="USER ID | MEMBER NAME | MEMBER GLOBAL NAME",
    nargs="+",
    required=False,
    default=None,
)
parser.add_argument(
    "-r",
    "--reason",
    type=str,
    help="REASON",
    nargs="+",
    required=False,
    default="Unspecified",
)


parser.add_argument(
    "-t",
    "--time",
    type=str,
    help="TIME",
    nargs="+",
    required=False,
    default=None,
)

parser.add_argument(
    "-uids",
    "--users",
    "-ids",
    type=str,
    help="USER IDS",
    nargs="+",
    required=False,
    default=None,
)
