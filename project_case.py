import math

class Item:
    def __init__(self, width, length, height, stackable=False):
        self.x = 0
        self.y = 0
        self.z = 0
        self.width = width
        self.length = length
        self.height = height
        self.stackable = stackable
        self.volume = self.width * self.height * self.length

    def get_points(self):
        return [
            (self.x, self.y, self.z),
            (self.x+self.width, self.y, self.z),
            (self.x, self.y+self.length, self.z),
            (self.x+self.width, self.y+self.length, self.z),
            (self.x, self.y, self.z+self.height),
            (self.x+self.width, self.y, self.z+self.height),
            (self.x, self.y+self.length, self.z+self.height),
            (self.x+self.width, self.y+self.length, self.z+self.height),
        ]

    def get_candidate_points(self):
        points = self.get_points()
        if not self.stackable:
            return points[:4]
        else:
            return points

    def get_position(self):
        return (self.x, self.y, self.z)

    def change_position(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def has_collision(self, item):
        x1, y1, z1, width1, length1, height1 = item.x, item.y, item.z, item.width, item.length, item.height
        x2, y2, z2, width2, length2, height2 = self.x, self.y, self.z, self.width, self.length, self.height

        if (x1 < x2 + width2 and x1 + width1 > x2 and
                y1 < y2 + length2 and y1 + length1 > y2 and
                z1 < z2 + height2 and z1 + height1 > z2):
            return True
        else:
            return False

    def has_on_top(self, item):
        is_on_top_points = [False, False, False, False]
        item_points = item.get_points()
        
        is_on_top_points[0] = self.x <= item_points[0][0] <= self.x+self.width and \
                        self.y <= item_points[0][1] <= self.y+self.length and \
                        item_points[0][2] == self.z+self.height

        is_on_top_points[1] = self.x <= item_points[1][0] <= self.x+self.width and \
                        self.y <= item_points[1][1] <= self.y+self.length and \
                        item_points[1][2] == self.z+self.height

        is_on_top_points[2] = self.x <= item_points[2][0] <= self.x+self.width and \
                        self.y <= item_points[2][1] <= self.y+self.length and \
                        item_points[2][2] == self.z+self.height

        is_on_top_points[3] = self.x <= item_points[3][0] <= self.x+self.width and \
                        self.y <= item_points[3][1] <= self.y+self.length and \
                        item_points[3][2] == self.z+self.height      

        return tuple(is_on_top_points)
 
    def __str__(self):
        return f"{self.x} {self.y} {self.z} {self.x+self.width} {self.y+self.length} {self.z+self.height}"

class Trailer:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height
        self.items = []

    def linear_feet(self):
        left_linear_feet = 0
        right_linear_feet = 0

        for item in self.items:
            if 0 <= item.x < int(self.width/2):
                left_linear_feet = max(left_linear_feet, item.y+item.length)
            if int(self.width/2) <= item.x <= self.width or int(self.width/2) <= item.x+item.width <= self.width:
                right_linear_feet = max(right_linear_feet, item.y+item.length)

        return math.ceil(((left_linear_feet/12)+(right_linear_feet/12))/2)

    def has_collision_with_walls(self, item):
        for point in item.get_points():
            if  point[0] > self.width or \
                point[1] > self.length or \
                point[2] > self.height:
                return True
        return False    

    def add_item(self, item):
        point_found = False
        has_on_top = (False, False, False, False)

        if len(self.items) == 0 and not self.has_collision_with_walls(item):
            item.change_position(0,0,0)
            point_found = True

        candidate_points = []
        for placed_item in self.items:
            candidate_points = candidate_points + placed_item.get_candidate_points()
        candidate_points = sorted(candidate_points, key=lambda x: (-x[2], x[1], x[0]))

        for point in candidate_points:
            has_collision = False
            has_on_top = (False, False, False, False)

            item.change_position(point[0], point[1], point[2])
            item_points = item.get_points()
            if item_points[0][2] == 0:
                has_on_top = (True, True, True, True)

            for placed_item in self.items:
                if placed_item.has_collision(item):
                    has_collision = True
                    break 
            if not has_collision:
                point_found = True
                for placed_item in self.items:
                    has_on_top = tuple(any(pair) for pair in zip(placed_item.has_on_top(item), has_on_top))
                if has_on_top[0] and has_on_top[1] and has_on_top[2] and has_on_top[3] \
                   and not self.has_collision_with_walls(item):
                    break  

        if item.z == 0:
            has_on_top = (True, True, True, True)
        if point_found and has_on_top[0] and has_on_top[1] and has_on_top[2] and has_on_top[3]:
            self.items += [item]

    def add_items(self, items):
        sorted_items = sorted(items, key=lambda x: (-x.volume, -x.width))
        for item in sorted_items:
            self.add_item(item)

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


def main():
    trailer = Trailer(96, float('inf'), 108)

    items = [
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),

        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),

        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),

        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(48,48,20, stackable=True),
        Item(20,20,20, stackable=True)      
    ]

    trailer.add_items(items)
    print(f"Linear feet: {trailer.linear_feet()}")

if __name__ == "__main__":
    main()
