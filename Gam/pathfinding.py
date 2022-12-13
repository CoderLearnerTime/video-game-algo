import math
import pygame

class Node():
    def __init__(self, x, y, parent=None):
        self.parent = parent
        self.x = x
        self.y = y

        self.f = 0
        self.g = 0
        self.h = 0

tileSize = 32
screenHeight = 40
screenWidth = 24
#run everytime player moves to determine best path to player
class aStar():
    @staticmethod
    def findPath(entity, player, collisionMap):
        start_x, start_y = math.ceil(entity.rect.x/tileSize), math.ceil(entity.rect.y/tileSize)
        end_x, end_y = math.ceil(player.rect.x/tileSize), math.ceil(player.rect.y/tileSize)
        start_node = Node(start_x, start_y, None)
        end_node = Node(end_x, end_y, None)
        open = []
        close = []
        open.append(start_node)

        while len(open) > 0:
            #print(len(close))
            current_node = open[0]
            cur_index = 0
            for index, item in enumerate(open):
                if item.f < current_node.f:
                    cur_index = index
                    current_node = item

            open.pop(cur_index)
            inClose = False
            # for closed_node in close:
                # if ((closed_node.x == current_node.x) and (closed_node.y == current_node.y)):
                    # inClose = True
                    # break
            # if inClose == False:
            close.append(current_node)

            if (current_node.x == end_node.x) and (current_node.y == end_node.y):
                path = []
                cur = current_node
                while cur != None:
                    path.append((cur.x, cur.y))
                    cur = cur.parent
                for index, node in enumerate(open):
                    open.pop(index)
                path = path[::-1]
                return [path, (current_node.g)]

            children = []
            for around_pos in [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,-1), (-1,1), (1,-1)]:
                adj_pos = ((around_pos[0] + current_node.x),(around_pos[1] + current_node.y))
                if (adj_pos[0] < 0 or adj_pos[0] > screenHeight - 1 or adj_pos[1] < 0 or adj_pos[1] > screenWidth - 1):
                    continue
                elif pygame.Surface.get_at(collisionMap, adj_pos) == (0,0,0):
                    continue
                
                new_node = Node(adj_pos[0], adj_pos[1], current_node)
                children.append(new_node)
            for child in children:
                closeEquals = False
                openEquals = False
                for closed_node in close:
                    if (child.x == closed_node.x) and (child.y == closed_node.y):
                        closeEquals = True
                        break
                
                # if (child.x == child.parent.x) and (child.y == child.parent.y):
                    # closeEquals = True

                child.g = current_node.g + 1
                child.h = ((end_x - child.x)**2) + ((end_y - child.y)**2)
                child.f = child.g + child.h

                for open_node in open:
                    if ((child.x == open_node.x) and (child.y == open_node.y)):
                        openEquals = True
                if (openEquals == True) or (closeEquals == True):
                    continue
                open.append(child)


 
