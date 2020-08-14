from room import Room
from player import Player
from world import World

from wander_aimlessly import find_unexplored_path, move_through_path, nearest_unexplored_room, find_path
from dft import Stack, Graph

import random
from ast import literal_eval

# Load world
world = World()

# map_file = "maps/test_line.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)

choice = input("1. Wander Aimlessly or DFT? (1/2)\n-> ").strip()
if choice == "1":

    seen = dict()
    visited = set()
    path_taken = list()

    traversal_path = find_path(player, seen, visited, path_taken, world)

elif choice == "2":

    traversal_path = []
    world_graph = Graph()
    world_graph.dft(traversal_path, player, room_graph)
else:
    print("Invalid Input\n")

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
