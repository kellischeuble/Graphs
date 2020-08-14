class Stack():
    def __init__(self):
        self.stack = []

    def __str__(self):
        return str(self.stack)

    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:
    def __init__(self):
        self.visited = {}
        self.reversed_path_traveled = Stack()
        self.reverse_directions = {
            'n': 's',
            'w': 'e',
            'e': 'w',
            's': 'n'
        }

    def add_room_to_visited(self, room_id):
        self.visited[room_id] = {}

    def add_direction(self, room_id, direction, destination_room=None):
        """
        Adds Edge to the graph. If no desttination_room is passed in,
        default to "?"
        """
        if destination_room is None:
            destination_room = '?'
        self.visited[room_id][direction] =  destination_room

    def get_unvisited_exits(self, room_id):
        """
        Checks room for any exits that have not yet been visited
        Returns list of exits
        """
        unvisited = []
        exits = self.visited[room_id]

        for direction, exit in exits.items():
            if exit == '?':
                unvisited.append(direction)

        return unvisited


    def dft(self, path_traveled, player, room_graph, direction=None, previous_room=None):
        """
        Depth First Traversal. Keep track of reverse path
        By continiously adding on the last move (in reverse)
        To the stack
        """

        # check to see if base case has been met
        if len(self.visited) == len(room_graph):
            return

        # check to see if a direction was passed in 
        # if there was, then travel there and add to
        # the path_traveled as well as reversed_path_traveled
        if direction is not None:
            player.travel(direction)
            path_traveled.append(direction)

            self.reversed_path_traveled.push(self.reverse_directions[direction])


        current_room = player.current_room
        if current_room.id not in self.visited:
            self.add_room_to_visited(current_room.id)
            
            exits = current_room.get_exits()
            for exit in exits:
                self.add_direction(current_room.id, exit)

        # Checks to see if we are coming from a previous room. If we are,
        # those edges / connections in the graph can be made
        if previous_room is not None:
            self.add_direction(previous_room.id,
                               direction,
                               current_room.id)
            self.add_direction(current_room.id,
                               self.reverse_directions[direction],
                               previous_room.id)

        # looks at current room for any exits that we haven't been to yet
        unvisited_exits = self.get_unvisited_exits(current_room.id)

        # if we have any unvisited exits, then call a dft on them recursively
        if len(unvisited_exits) > 0:
            for exit in unvisited_exits:
                self.dft(path_traveled, player, room_graph, exit, current_room)

        # if we do not have any unvisited_exits, then we can just reverse
        # our steps
        reverse_step = self.reversed_path_traveled.pop()

        player.travel(reverse_step)
        path_traveled.append(reverse_step)