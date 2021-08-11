import argparse
from core.search import Search


def main_parser():
    """
        Main Parser
    """

    parser = argparse.ArgumentParser(prog="PROG")
    parser.add_argument("function", choices=["search", "cache", "intro"])
    parser.add_argument("character", type=str, nargs="?")
    parser.add_argument("--world",  action="count", required=False, default=0)
    parser.add_argument("--clean", action="count", required=False, default=0)
    args = parser.parse_args()

    #  check function (search , cache, or intro )
    if args.function == 'search':
        print("im in search")
        # check if character was given
        if args.character:
            # check if world was given
            if args.world >= 1:
                print(args.character,args.world)
            else:
                print(args.character)
    elif args.function == "cache":
        print("im in cache")
        # if character with cache raise exception
        if args.character:
            raise Exception("error: unrecognized arguments: ", args.character)
        if args.clean >= 1:
            print(args.function, args.clean)
        else:
            print(args.function)
    else:
        print("intro")


def search_call(search_query,  show_world=False):
    pass


def clean_cache(object_name):
    pass




if __name__ == "__main__":
    main_parser()
