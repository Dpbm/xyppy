
import argparse

from xyppy import run_game

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-slow-scroll', action='store_true', help='remove the artificial scrolling delay')
    parser.add_argument('STORY_FILE_OR_URL')
    args = parser.parse_args()
    run_game(args)
