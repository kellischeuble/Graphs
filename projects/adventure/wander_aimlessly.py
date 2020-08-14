import random

def find_unexplored_path(cur_room, seen, visited):
    """
    Looks around in current room for
    an unexplored path. 
    
    Returns direction of unexplored path and the room
    above it if there is one, otherwise returns -1
    """

    add_to_seen(cur_room, seen)
    if cur_room not in visited:
        visited.add(cur_room)

    keys = list(seen[cur_room].keys())
    random.shuffle(keys)
    shuffled = [(key, seen[cur_room][key]) for key in keys]    
    for exit, known in shuffled:
        if known == "?":
            room_in_direction = cur_room.get_room_in_direction(exit)
            seen[cur_room][exit] = room_in_direction

            add_to_seen(room_in_direction, seen, cur_room, exit, get_opposite_direction(exit))
            return exit

    return False
    

def move_through_path(cur_room, path, visited, player, path_taken):
    """
    Given a path as a list ex:
    ['n'] or ['n', 's', 'e'], move through
    that path
    """
    add_to_visited(cur_room, visited)

    for direction in path:
        path_taken.append(direction)
        player.travel(direction)
        cur_room = player.current_room
        add_to_visited(cur_room, visited)

    return cur_room

def nearest_unexplored_room(cur_room, seen, visited):
    """
    Uses breadth first search to find the closest
    room with an unexplored path. 

    Returns path
    """

    queue = list()

    for exit in cur_room.get_exits():
        queue.append([exit, cur_room])

    while len(queue) > 0:
        path = queue.pop(0)
        room = path[-1]
        direction = path[-2]
        
        direction_from = get_opposite_direction(direction)
        new_room = room.get_room_in_direction(direction)

        if new_room:
            if new_room not in seen:
                add_to_seen(new_room, seen, room, direction, direction_from)
                
            if new_room not in visited:
                return path[:-1]
            
            for exit in new_room.get_exits():
                new_path = path[:-1].copy()
                new_path.append(direction)
                new_path.append(new_room)
                queue.append(new_path)

            paths = cur_room.get_exits()
            for path in paths:
                seen[cur_room][path] = "?"

    return False


def add_to_seen(room_to, seen, room_from=None, direction_to=None, direction_from=None):
    """
    Adds room to seen dictionary
    """
    if room_to in seen:
        return False
    if room_to not in seen:
        seen[room_to] = dict()
        paths = room_to.get_exits()

        for path in paths:
            seen[room_to][path] = "?"

        if room_from:
            seen[room_from][direction_to] = room_to
            seen[room_to][direction_from] = room_from
        return True

def add_to_visited(room, visited):
    if room not in visited:
        visited.add(room)
        return True
    return False


def get_opposite_direction(direction):
    dir = {"n":"s", "s":"n", "e":"w", "w":"e"}
    return dir[direction]

def find_path(player, seen, visited, path_taken, world):
    player.current_room = world.starting_room

    while len(visited) < len(world.rooms):
        can_move = True

        while can_move:
            path = find_unexplored_path(player.current_room, seen, visited)
            if path:
                move_through_path(player.current_room, [path], visited, player, path_taken)
            else:
                can_move = False

        next_path = nearest_unexplored_room(player.current_room, seen, visited)
        if next_path:
            move_through_path(player.current_room, next_path, visited, player, path_taken)

    return path_taken
    

