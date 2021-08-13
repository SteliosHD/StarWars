import argparse
from core.swapiDAO import SwapiDAO
from core.cache import PersistentCache
from time import sleep


def main_parser():
    """
        Main Parser
    """

    parser = argparse.ArgumentParser(prog="PROG")
    parser.add_argument("function", choices=["search", "cache", "history", "intro"])
    parser.add_argument("character", type=str, nargs="?")
    parser.add_argument("--world",  action="count", required=False, default=0)
    parser.add_argument("--clean", action="count", required=False, default=0)
    args = parser.parse_args()

    #  check function (search , cache, or intro )
    if args.function == 'search':
        # check if character was given
        if args.character:
            # check if world was given
            if args.world >= 1:
                search_call(args.character, show_world=True)
                # print(args.character,args.world)
            else:
                search_call(args.character)
    elif args.function == "cache":
        # if character with cache raise exception
        if args.character:
            raise Exception("error: unrecognized arguments: ", args.character)
        if args.clean >= 1:
            clean_cache()
        else:
            print("No command was given Commander!")
    elif args.function == "history":
        get_history()
    else:
        message = """In a galaxy far, far away from Canes Venatici I., on a planet called Earth,
        there exist a passionate programmer working with his computer and a semi-broken fan in
            order to land a job. There are signs that the force is strong within this young padawan.
                Prove his worth he must.\n"""
        for char in message:
            print(char, end='', flush=True)
            sleep(.075)

# Helper Functions
def search_call(search_query,  show_world=False):
    swapi_obj = SwapiDAO()
    swapi_obj.search_char(search_query, world_flag=show_world)
    return 1


def clean_cache():
    cache_obj = PersistentCache() # bound to the object but will delete the file anyways
    cache_obj.delete_cache()
    return 1


def get_history():
    cached_obj = PersistentCache() # bound to the object but will delete the file anyways
    cached_obj.get_history()
    return 1


if __name__ == "__main__":
    main_parser()
