import argparse

# Fun module
combine_parser = argparse.ArgumentParser(add_help=False)
combine_parser.add_argument(
    "--first", "-f", type=str, help="First Word", required=True, nargs="+"
)
combine_parser.add_argument(
    "--second", "-s", type=str, help="Second Word", required=True, nargs="+"
)

# Hentai module
rating_parser = argparse.ArgumentParser(add_help=False)
rating_parser.add_argument(
    "--rating",
    "-r",
    type=str,
    choices=["questionable", "explicit", "e", "q"],
    help="questionable | explicit | q | e",
    required=False,
    default=None,
)
hentai_api_parser = argparse.ArgumentParser(add_help=False)
hentai_api_parser.add_argument(
    "--rating",
    "-r",
    type=str,
    choices=["questionable", "explicit", "e", "q"],
    help="questionable | explicit | q | e",
    required=False,
    default=None,
)
hentai_api_parser.add_argument(
    "--tags", "-t", type=str, nargs="+", required=False, default=[], help="tags"
)
hentai_api_parser.add_argument(
    "--plus", "-p", action="store_true", help="Enable plus mode. Just type '-p'"
)

# inventory module
buycustom = argparse.ArgumentParser(add_help=False)
buycustom.add_argument(
    "--name",
    type=str,
    help="NAME",
    nargs="+",
    required=True,
)
buycustom.add_argument(
    "--link",
    type=str,
    help="LINK",
    required=True,
)

#manage module