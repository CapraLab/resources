'''A graphical representation of the board game Settlers of Catan. Currently 
    supports 2 players and ignores development cards, ports, and trading.
    Programmed by Laura Colbran and Omar Kaufman
    
    Requires the module graphics.py

    Contents:
        class RectangleButton
        class Dice
        class Resource
        class Player
        class Road
        class LandHex
        class Corner
        class Robber
        class Interface
        class SettlersGame
        
    Usage: python settlers.py
'''

from graphics import *
from math import *
from random import *


class RectangleButton:
    '''Amended from Andy Exley's module. Creates a rectangular button object
        with a given center, width, height, and label.'''
    
    # builds a button   
    def __init__(self, center, width, height, text):
        w, h = width / 2.0, height / 2.0
        self.xmin, self.xmax = center.getX() - w, center.getX() + w
        self.ymin, self.ymax = center.getY() - h, center.getY() + h
        self.rect = Rectangle(Point(self.xmin, self.ymin), 
                                Point(self.xmax, self.ymax))
        self.rect.setFill('white')
        self.rect.setOutline('grey')
        self.text = Text(center, text)
        self.deactivate()
    
    # draws the button in the graphics window
    def draw(self, window):
        self.rect.draw(window)
        self.text.draw(window)
    
    # undraws the button    
    def undraw(self):
        self.rect.undraw()
        self.text.undraw()
    
    def get_label(self):
        return self.text.getText()
    
    # returns True if Mouse click location (p) is within button bounds.
    def clicked(self, p):
        return (self.active and self.xmin <= p.getX() <= self.xmax and 
            self.ymin <= p.getY() <= self.ymax)
    
    # Deactivates the button.
    def deactivate(self):
        self.text.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False
    
    # Activates the button.
    def activate(self):
        self.text.setFill('black')
        self.rect.setWidth(2)
        self.active = True

class Dice:
    '''Creates a dice object and "rolls" it using a random number generator.
        Since Settlers uses 2 die, the roll method actually rolls twice, and 
        returns the sum of the two.'''
    def __init__(self):
        self.dice1 = 0
        self.dice2 = 0
    
    # Rolls both dice objects, returns sum of values.
    def roll(self):
        self.dice1 = randrange(1,7)
        self.dice2 = randrange(1,7)
        return self.dice1 + self.dice2
        

class Resource:
    '''Creates a list of the numbers of each resource the player holds. 
        Resources can be added and removed.'''
    def __init__(self, grain, sheep, lumber, brick, ore):
        self.resource_list = [grain, sheep, lumber, brick, ore]
    
    # returns list object.
    def get_resource_list(self):
        return self.resource_list

    def add_grain(self):
        self.resource_list[0] += 1
    
    def add_sheep(self):
        self.resource_list[1] += 1
    
    def add_lumber(self):
        self.resource_list[2] += 1
    
    def add_brick(self):    
        self.resource_list[3] += 1
    
    def add_ore(self):
        self.resource_list[4] += 1
        
    def use_grain(self):
        self.resource_list[0] -= 1
        
    def use_sheep(self):
        self.resource_list[1] -= 1
        
    def use_lumber(self):
        self.resource_list[2] -= 1
        
    def use_brick(self):
        self.resource_list[3] -= 1
        
    def use_ore(self):
        self.resource_list[4] -= 1
        
        
class Player:
    '''Stores information for each player. This includes identification,
        colour of blocks, score, and whether it is their turn. Methods include
        building settlements and roads, and switching turns.'''
    # Initialises player. Starts with appropriate stock, and enough resources
    # to lay initial settlements and roads.
    # takes colours to indicated settlements and upgrades for that player
    def __init__(self, number, color, color2):
        self.number = number
        self.score = 0
        self.turn = False
        self.color = color
        self.upgrade_color = color2
        self.stock = [15,5,4]
        self.settlement_list = []
        self.road_list = []
        self.resource_list = Resource(2,2,4,4,0)
    
    def get_score(self):
        return self.score
    
    def get_number(self):
        return self.number
        
    def get_color(self):
        return self.color
        
    def get_upgrade_color(self):
        return self.upgrade_color
    
    def get_stock(self):
        return self.stock
        
    def get_set_list(self):
        return self.settlement_list
        
    def get_road_list(self):
        return self.road_list
        
    def get_resource_list(self):
        return self.resource_list
        
    def is_turn(self):
        return self.turn
        
    # Consumes appropriate resources, adds score, adds settlement object
    # to a list.
    def add_settlement(self, settlement):       
        self.get_resource_list().use_brick()
        self.get_resource_list().use_grain()
        self.get_resource_list().use_lumber()
        self.get_resource_list().use_sheep()
        self.score += 1
        self.stock[1] -= 1
        self.settlement_list.append(settlement)
        
    # Upgrades existing settlement to a city. 
    # Alters stock and resources accordingly.
    def add_city(self, city):
        for i in range(3):
            self.get_resource_list().use_grain()
        for i in range(2):
            self.get_resource_list().use_ore()
        self.score += 1
        self.stock[2] -= 1
        self.stock[1] += 1
        
    # Adds a road to the list, alters stock and resources appropriately.
    def add_road(self, road):
        self.get_resource_list().use_lumber()
        self.get_resource_list().use_brick()
        self.stock[0] -= 1
        self.road_list.append(road)
        
    def switch_turn(self):
        if self.turn:
            self.turn = False
        else:
            self.turn = True
    

class Road:
    '''Creates line segments to represent roads. The line segments are defined
        between vertices (p1 and p2).'''
    def __init__(self, p1, p2):
        self.point_1 = p1
        self.point_2 = p2
        self.road = Line(self.point_1, self.point_2)
        self.road.setWidth(8)
    
    def get_corners(self):
        return (self.point_1,self.point_2)
    
    def build_road(self, win):
        self.road.draw(win)

    def set_fill(self, colour):
        self.road.setFill(colour)        
            
class LandHex:
    '''Builds hexes to make the board. Hexes consist of a placement, the 
        polygon, the centerpoint, the land type assignment (random each 
        game), the number (also random), and its corners.'''
    def __init__(self, place, hex_image, center, type, number, corners):
        self.placement = place
        self.tile = hex_image
        self.center = center
        self.landtype = type
        self.value = number
        self.robber = False
        self.c_list = corners
        
    def get_placement(self):
        return self.placement
        
    def get_tile(self):
        return self.tile
        
    def get_center(self):
        return self.center
        
    def get_c_list(self):
        return self.c_list    
    
    def get_landtype(self):
        return self.landtype
    
    def get_value(self):
        if self.robber == True:
            return 0
        else:
            return self.value
    
    def add_robber(self):
        self.robber = True
    
    def remove_robber(self):
        self.robber = False
        

class Corner:
    '''Defines the points at the intersections of the hexes. Is used to place
        settlements and roads, and to determine resource allocation.'''
    def __init__(self, center):
        self.color = None
        self.center = center
        self.Xmin = self.center.getX() - 10 
        self.Xmax = self.center.getX() + 10
        self.Ymin = self.center.getY() - 10
        self.Ymax = self.center.getY() + 10
        self.circle = Circle(self.center, 10)
        self.is_city = False    
    
    def get_center(self):
        return self.center
        
    def get_color(self):
        return self.color
    
    def get_bounds(self, p):
        return (self.Xmin <= p.getX() <= self.Xmax and 
            self.Ymin <= p.getY() <= self.Ymax)
    
    def city(self):
        return self.is_city
    
    # draws a settlement for a player in the window
    def build_settlement(self,player, win): 
        self.color = player.get_color()
        self.circle.setFill(self.color)
        self.circle.draw(win)
    
    # upgrades a settlement for a player in the window
    def upgrade(self, player, settlement, win):
        self.circle.undraw()
        self.circle.setFill(player.get_upgrade_color())
        self.circle.draw(win)
        self.is_city = True


class Robber:
    '''Defines the robber, which blocks resources from being produced on 
        a given hex.'''
    # Starts the robber on a random hex in the graphics window.
    def __init__(self, hex, win):
        self.win = win
        self.hex1 = hex
        
        self.robber_circ = Circle(Point(self.hex1.get_center()[0],\
            self.hex1.get_center()[1]), 30)
        self.robber_circ.setFill('peachpuff')
        self.robber_circ.draw(self.win)
        self.hex1.add_robber()
    
    # Moves the robber to a new random hex.   
    def move_robber(self, hex2):
        self.hex1.remove_robber()
        self.robber_circ.undraw()
        
        self.hex1 = hex2
        self.robber_circ = Circle(Point(self.hex1.get_center()[0],\
            self.hex1.get_center()[1]), 30)
        self.robber_circ.setFill('peachpuff')
        self.robber_circ.draw(self.win)
        self.hex1.add_robber()


class Interface:
    '''Builds the board, buttons, user responses, etc.'''
    def __init__(self):
        # Window
        self.window = GraphWin('Settlers of Catan', 700, 700)
        self.window.setBackground('lightblue')
        self.roll = None
        self.drawn = False
        self.game_is_not_over = True 
        title = Text(Point(350,25), 'The Settlers of Catan')
        title.setStyle('italic')
        title.setFace('courier')
        title.setSize(20)
        title.setFill('mediumpurple')
        title.draw(self.window)
        
        # Draws the color key.
        k1 = Rectangle(Point(80,660),Point(100,680))
        k1.setFill('goldenrod')
        k1.draw(self.window)
        t1 = Text(Point(124,670),'=  Plain')
        t1.draw(self.window)
        
        k2 = Rectangle(Point(180,660),Point(200,680))
        k2.setFill('greenyellow')
        k2.draw(self.window)
        t2 = Text(Point(228,670),'=  Pasture')
        t2.draw(self.window)
        
        k3 = Rectangle(Point(280,660),Point(300,680))
        k3.setFill('forestgreen')
        k3.draw(self.window)
        t3 = Text(Point(325,670),'=  Forest')
        t3.draw(self.window)
        
        k4 = Rectangle(Point(380,660),Point(400,680))
        k4.setFill('firebrick')
        k4.draw(self.window)
        t4 = Text(Point(418,670), '=  Hill')
        t4.draw(self.window)
        
        k5 = Rectangle(Point(480,660),Point(500,680))
        k5.setFill('slategrey')
        k5.draw(self.window)
        t5 = Text(Point(533,670), '=  Mountain')
        t5.draw(self.window)
        
        k6 = Rectangle(Point(580,660),Point(600,680))
        k6.setFill('wheat')
        k6.draw(self.window)
        t6 = Text(Point(627,670), '=  Desert')
        t6.draw(self.window)
        
        # Draws the button to roll dice and begin turn.
        self.roll_butt = RectangleButton(Point(100,60),90,20,"Start Turn & Roll")
        self.roll_butt.draw(self.window)
        self.roll_butt.activate()
        
        # Allows to quit
        self.quit = RectangleButton(Point(600, 60), 60, 20, 'Quit')
        self.quit.draw(self.window)
        self.quit.activate()
        Text(Point(600,78),'Double Click!').draw(self.window)
        
        self.build = RectangleButton(Point(350, 60), 60, 20, 'Build')
        self.build.draw(self.window)
        self.build.activate()
        
        c = 350
        x = 30
        
        # List of corner centers.
        self.corner_center_list = [Point(c - 5.196 * x, c - 7 * x),
            Point(c - 3.464 * x, c - 8 * x), Point(c - 1.732 * x, c - 7 * x),
            Point(c, c - 8 * x), Point(c + 1.732 * x, c - 7 * x),
            Point(c + 3.464 * x, c - 8 * x), Point(c + 5.196 * x, c - 7 * x),
            Point(c + 5.196 * x, c - 5 * x), Point(c + 6.928 * x, c - 4 * x),
            Point(c + 6.928 * x, c - 2 * x), Point(c + 8.66 * x, c - x),
            Point(c + 8.66 * x, c + x), Point(c + 6.928 * x, c + 2 * x),
            Point(c + 6.928 * x, c + 4 * x), Point(c + 5.196 * x, c + 5 * x),
            Point(c + 5.196 * x, c + 7 * x), Point(c + 3.464 * x, c + 8 * x),
            Point(c + 1.732 * x, c + 7 * x), Point(c, c + 8 * x),
            Point(c - 1.732 * x, c + 7 * x), Point(c - 3.464 * x, c + 8 * x),
            Point(c - 5.196 * x, c + 7 * x), Point(c - 5.196 * x, c + 5 * x), 
            Point(c - 6.928 * x, c + 4 * x), Point(c - 6.928 * x, c + 2 * x), 
            Point(c - 8.66 * x, c + x), Point(c - 8.66 * x, c - x), 
            Point(c - 6.928 * x, c - 2 * x), Point(c - 6.928 * x, c - 4 * x), 
            Point(c - 5.196 * x, c - 5 * x), Point(c - 3.464 * x, c - 4 * x), 
            Point(c - 1.732 * x, c - 5 * x), Point(c, c - 4 * x), 
            Point(c + 1.732 * x, c - 5 * x), Point(c + 3.464 * x, c - 4 * x), 
            Point(c + 3.464 * x, c - 2 * x), Point(c + 5.196 * x, c - x), 
            Point(c + 5.196 * x, c + x), Point(c + 3.464 * x, c + 2 * x), 
            Point(c + 3.464 * x, c + 4 * x), Point(c + 1.732 * x, c + 5 * x), 
            Point(c, c + 4 * x), Point(c - 1.732 * x, c + 5 * x), 
            Point(c - 3.464 * x, c + 4 * x), Point(c - 3.464 * x, c + 2 * x), 
            Point(c - 5.196 * x, c + x), Point(c - 5.196 * x, c - x), 
            Point(c - 3.464 * x, c - 2 * x), Point(c - 1.732 * x, c - x), 
            Point(c, c - 2 * x), Point(c + 1.732 * x, c - x), 
            Point(c + 1.732 * x, c + x), Point(c, c + 2 * x), 
            Point(c - 1.732 * x, c + x)]
        
        # List of corner objects
        self.corner_list = []
        for i in self.corner_center_list:
            c1 = Corner(i)
            
            self.corner_list.append(c1)
        
        
        # List of centerpoints for hexes
        self.hex_center = [(c - 3.464 * x, c - 6 * x),(c, c - 6 * x),
                    (c + 3.464 * x, c - 6 * x),(c - 5.196 * x, c - 3 * x),
                    (c - 1.732 * x, c - 3 * x),(c + 1.732 * x, c - 3 * x), 
                    (c + 5.196 * x, c - 3 * x),(c - 6.928 * x, c),
                    (c - 3.464 * x, c),(c, c),(c + 3.464 * x, c),
                    (c + 6.928 * x, c),(c - 5.196 * x, c + 3 * x),
                    (c - 1.732 * x, c + 3 * x),(c + 1.732 * x, c + 3 * x),
                    (c + 5.196 * x, c + 3 * x),(c - 3.464 * x, c + 6 * x),
                    (c, c + 6 * x), (c + 3.464 * x, c + 6 * x)]
        
        # in landtype_list: 1 = fields, 2 = pasture, 3 = forest, 
        # 4 = clays, 5 = mountain
        landtype_list = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,6]
        number_list = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        shuffle(landtype_list)
        shuffle(number_list)
        desert = landtype_list.index(6)
        number_list.insert(desert, 0)
            
        
        self.hex_list = []
        for i in self.hex_center:
            hex = Polygon(Point(i[0], i[1] + 2 * x), 
                        Point(i[0] - 1.732 * x, i[1] + x),
                        Point(i[0] - 1.732 * x, i[1] - x), 
                        Point(i[0], i[1] - 2 * x),
                        Point(i[0] + 1.732 * x, i[1] - x), 
                        Point(i[0] + 1.732 * x, i[1] + x))
            self.hex_list.append(hex)
            
        # List of landhex objects, unique to each run of the program
        self.l = []
        LandHex1 = LandHex(1, self.hex_list[0],self.hex_center[0],
                landtype_list[0], number_list[0], [self.corner_list[0], 
                self.corner_list[1], self.corner_list[2], self.corner_list[31],
                self.corner_list[30], self.corner_list[29]])
        self.l.append(LandHex1)
        LandHex2 = LandHex(2, self.hex_list[1],self.hex_center[1],
                landtype_list[1], number_list[1], [self.corner_list[2], 
                self.corner_list[3], self.corner_list[4], self.corner_list[33], 
                self.corner_list[34], self.corner_list[31]])
        self.l.append(LandHex2)
        LandHex3 = LandHex(3, self.hex_list[2],self.hex_center[2],
                landtype_list[2], number_list[2], [self.corner_list[4], 
                self.corner_list[5], self.corner_list[6], self.corner_list[7],
                self.corner_list[34], self.corner_list[33]])
        self.l.append(LandHex3)
        LandHex4 = LandHex(4, self.hex_list[3],self.hex_center[3],
                landtype_list[3], number_list[3], [self.corner_list[28],
                self.corner_list[29], self.corner_list[30], self.corner_list[47],
                self.corner_list[46], self.corner_list[27]])
        self.l.append(LandHex4)
        LandHex5 = LandHex(5, self.hex_list[4],self.hex_center[4],
                landtype_list[4], number_list[4], [self.corner_list[30],
                self.corner_list[31], self.corner_list[32], self.corner_list[49],
                self.corner_list[48], self.corner_list[47]])
        self.l.append(LandHex5)
        LandHex6 = LandHex(6, self.hex_list[5],self.hex_center[5],
                landtype_list[5], number_list[5], [self.corner_list[32],
                self.corner_list[33], self.corner_list[34], self.corner_list[35],
                self.corner_list[50], self.corner_list[49]])
        self.l.append(LandHex6)
        LandHex7 = LandHex(7, self.hex_list[6],self.hex_center[6],
                landtype_list[6], number_list[6], [self.corner_list[34],
                self.corner_list[7], self.corner_list[8], self.corner_list[9],
                self.corner_list[36], self.corner_list[35]])
        self.l.append(LandHex7)
        LandHex8 = LandHex(8, self.hex_list[7],self.hex_center[7],
                landtype_list[7], number_list[7], [self.corner_list[26],
                self.corner_list[27], self.corner_list[46], self.corner_list[45],
                self.corner_list[24], self.corner_list[25]])
        self.l.append(LandHex8)
        LandHex9 = LandHex(9, self.hex_list[8],self.hex_center[8],
                landtype_list[8], number_list[8], [self.corner_list[46],
                self.corner_list[47], self.corner_list[48], self.corner_list[53],
                self.corner_list[44], self.corner_list[45]])
        self.l.append(LandHex9)
        LandHex10 = LandHex(10, self.hex_list[9],self.hex_center[9],
                landtype_list[9], number_list[9], [self.corner_list[48],
                self.corner_list[49], self.corner_list[50], self.corner_list[51],
                self.corner_list[52], self.corner_list[53]])
        self.l.append(LandHex10)
        LandHex11 = LandHex(11, self.hex_list[10],self.hex_center[10],
                landtype_list[10], number_list[10], [self.corner_list[50],
                self.corner_list[35], self.corner_list[36], self.corner_list[37],
                self.corner_list[38], self.corner_list[51]])
        self.l.append(LandHex11)
        LandHex12 = LandHex(12, self.hex_list[11],self.hex_center[11],
                landtype_list[11], number_list[11], [self.corner_list[36],
                self.corner_list[9], self.corner_list[10], self.corner_list[11],
                self.corner_list[12], self.corner_list[37]])
        self.l.append(LandHex12)
        LandHex13 = LandHex(13, self.hex_list[12],self.hex_center[12],
                landtype_list[12], number_list[12], [self.corner_list[24],
                self.corner_list[45], self.corner_list[44], self.corner_list[43], 
                self.corner_list[22], self.corner_list[23]])
        self.l.append(LandHex13)
        LandHex14 = LandHex(14, self.hex_list[13],self.hex_center[13],
                landtype_list[13], number_list[13], [self.corner_list[44],
                self.corner_list[53], self.corner_list[52], self.corner_list[41], 
                self.corner_list[42], self.corner_list[43]])
        self.l.append(LandHex14)
        LandHex15 = LandHex(15, self.hex_list[14],self.hex_center[14],
                landtype_list[14], number_list[14], [self.corner_list[52],
                self.corner_list[51], self.corner_list[38], self.corner_list[39],
                self.corner_list[40], self.corner_list[41]])
        self.l.append(LandHex15)
        LandHex16 = LandHex(16, self.hex_list[15],self.hex_center[15],
                landtype_list[15], number_list[15], [self.corner_list[38],
                self.corner_list[37], self.corner_list[12], self.corner_list[13],
                self.corner_list[14], self.corner_list[39]])
        self.l.append(LandHex16)
        LandHex17 = LandHex(17, self.hex_list[16],self.hex_center[16],
                landtype_list[16], number_list[16], [self.corner_list[22],
                self.corner_list[43], self.corner_list[42], self.corner_list[19], 
                self.corner_list[20], self.corner_list[21]])
        self.l.append(LandHex17)
        LandHex18 = LandHex(18, self.hex_list[17],self.hex_center[17],
                landtype_list[17], number_list[17], [self.corner_list[42],
                self.corner_list[41], self.corner_list[40], self.corner_list[17],
                self.corner_list[18], self.corner_list[19]])
        self.l.append(LandHex18)
        LandHex19 = LandHex(19, self.hex_list[18],self.hex_center[18],
                landtype_list[18], number_list[18], [self.corner_list[40],
                self.corner_list[39], self.corner_list[14], self.corner_list[15],
                self.corner_list[16], self.corner_list[17]])
        self.l.append(LandHex19)
        
        # Fills the hexes correctly for their assigned types.
        for i in range(19):
            if self.l[i].get_landtype() == 1:
                self.l[i].get_tile().setFill('goldenrod')
            elif self.l[i].get_landtype() == 2:
                self.l[i].get_tile().setFill('greenyellow')      
            elif self.l[i].get_landtype() == 3:
                self.l[i].get_tile().setFill('forestgreen')
            elif self.l[i].get_landtype() == 4:
                self.l[i].get_tile().setFill('firebrick')
            elif self.l[i].get_landtype() == 5:
                self.l[i].get_tile().setFill('slategrey')
            else:
                self.l[i].get_tile().setFill('wheat')
            self.l[i].get_tile().draw(self.window)

        # Puts the labels on each hex.
        for i in range(19):
            if self.l[i].get_value() != 0:
                circ = Circle(Point(self.hex_center[i][0],
                    self.hex_center[i][1]), x / 2)
                circ.setFill('white')
                circ.draw(self.window)
                num = self.l[i].get_value()
                number = Text(Point(self.hex_center[i][0],
                    self.hex_center[i][1]), str(num))
                number.setSize(14)
                if self.l[i].get_value() == 8 or self.l[i].get_value() == 6:
                    number.setFill('red')
                number.draw(self.window)
        
        # puts the robber in his starting place.
        for i in range(19): 
            if self.l[i].get_landtype() == 6:
                self.rob = Robber(self.l[i], self.window)


    def make_set(self, player):
        '''Makes a new settlement on the board for the player'''
        r = self.window.getMouse()
        quest = False
        
        for j in self.corner_list:
            if j.get_bounds(r):
                b = j
                quest = True

        if quest and b.get_color() == None: 
            player.add_settlement(b)
            b.build_settlement(player, self.window)

        else:
            self.make_set(player)              
                
    def make_road(self, player):
        '''Makes a new road on the board for the player'''
        r1 = self.window.getMouse()
        r2 = self.window.getMouse()
        self.corner_bounds_list1 = []
        self.corner_bounds_list2 = []

        for j in self.corner_list:
            if j.get_bounds(r1):
                b1 = j.get_center()
                self.corner_bounds_list1.append(b1)
            
        for k in self.corner_list:
            if k.get_bounds(r2):
                b2 = k.get_center()
                self.corner_bounds_list2.append(b2)
    
        if len(self.corner_bounds_list1) == 1 and \
            len(self.corner_bounds_list2) == 1 and \
            5000 >= ((b1.getX() - b2.getX()) ** 2 + \
            (b1.getY() - b2.getY()) ** 2) >= 3000:                      
            rd = Road(b1,b2)
            player.add_road(rd)
            rd.set_fill(player.get_color())
            rd.build_road(self.window)
        else:
            self.make_road(player)
                 
    def roll_button_actions(self, player1, player2):                    
        '''Assigns new die value and switches turn between players.'''
        self.p = self.window.getMouse()
        self.player1 = player1
        self.player2 = player2
        dice = Dice()
        
        if self.roll_butt.clicked(self.p):
            self.roll_butt.undraw()
            if self.roll:
                self.roll.undraw()
                self.val.undraw()
            
            # Displays roll value.
            self.val = Text(Point(200,60), 'Roll Value:')
            self.val.setFill('black')
            self.val.setSize(16)
            self.val.draw(self.window)
           
            self.roll_value = dice.roll()
            self.roll = Text(Point(250,60), self.roll_value)
            self.roll.setStyle('bold')
            self.roll.setFill('darkblue')
            self.roll.setSize(16)
            self.roll_butt.draw(self.window)
            self.roll.draw(self.window)
            
            # Moves the robber to a random hex.
            if self.roll_value == 7:
                r = self.window.getMouse()
                for i in self.hex_center:
                    if (r.getX() - i[0]) ** 2 + (r.getY() - i[1]) ** 2\
                        <= 400:
                        for j in self.l:
                            if j.get_center() == i:
                                self.rob.move_robber(j)
                    
                
            
            # Adds resources if settlement is present on hexes with roll value. If 
            # settlement is a city, player gets twice the resources.
            add_resources1 = []
            add_resources2 = []
            for q in self.l:
                for i in player1.get_set_list():
                    if i in q.get_c_list() and q.get_value() == self.roll_value:
                        if i.city():    
                            add_resources1.append(q)
                            add_resources1.append(q)
                        else:
                            add_resources1.append(q)
                for i in player2.get_set_list():
                    if i in q.get_c_list() and q.get_value() == self.roll_value:
                        if i.city():    
                            add_resources2.append(q)
                            add_resources2.append(q)
                        else:
                            add_resources2.append(q)
                        
            for p in add_resources1:
                if p.get_landtype() == 1:
                    player1.get_resource_list().add_grain()
                elif p.get_landtype() == 2:
                    player1.get_resource_list().add_sheep()
                elif p.get_landtype() == 3:
                    player1.get_resource_list().add_lumber()
                elif p.get_landtype() == 4:
                    player1.get_resource_list().add_brick()
                elif p.get_landtype() == 5:
                    player1.get_resource_list().add_ore()
                    
            for p in add_resources2:
                if p.get_landtype() == 1:
                    player2.get_resource_list().add_grain()
                elif p.get_landtype() == 2:
                    player2.get_resource_list().add_sheep()
                elif p.get_landtype() == 3:
                    player2.get_resource_list().add_lumber()
                elif p.get_landtype() == 4:
                    player2.get_resource_list().add_brick()
                elif p.get_landtype() == 5:
                    player2.get_resource_list().add_ore()
            
            
            self.player1.switch_turn()
            self.player2.switch_turn()
            self.display_stuff(player1,player2)            
    
    
    def is_quit_clicked(self):
        if self.quit.clicked(self.p):
            return True
        else:
            return False
    
    def end_game(self):
        self.game_is_not_over = False
    
    def game_not_over(self):
        return self.game_is_not_over
          
    # Method to initialise the game layout. Player can build a settlement
    # and a road.                
    def start_game(self, player):
        self.make_set(player)
        
        self.make_road(player)
        
        # Adds resources for hexes around second settlement.
        add_resources = []
        if len(player.get_set_list()) == 2:
            for q in self.l:
                if player.get_set_list()[1] in q.get_c_list():
                    add_resources.append(q)
            for p in add_resources:
                if p.get_landtype() == 1:
                    player.get_resource_list().add_grain()
                elif p.get_landtype() == 2:
                    player.get_resource_list().add_sheep()
                elif p.get_landtype() == 3:
                    player.get_resource_list().add_lumber()
                elif p.get_landtype() == 4:
                    player.get_resource_list().add_brick()
                elif p.get_landtype() == 5:
                    player.get_resource_list().add_ore()
            
    
    def display_stuff(self, player1, player2):
        '''Displays the information (stock, resources available, score)
            for each player. Redraws every time the while loop in play method 
            reiterates. Info is in bold for player whose turn it is.'''

        if self.drawn:
            self.rect1.undraw()
            self.rect2.undraw()
            self.n1.undraw()
            self.n2.undraw()
            
            self.s1.undraw()
            self.s2.undraw()
            self.s3.undraw()
            self.s4.undraw()
            self.s5.undraw()
            self.s6.undraw()
            self.s7.undraw()
            self.s8.undraw()
            self.s9.undraw()
            self.s10.undraw()
            self.s11.undraw()
            self.s12.undraw()
            self.s13.undraw()
            self.s14.undraw()
            
            self.r1.undraw()
            self.r2.undraw()
            self.r3.undraw()
            self.r4.undraw()
            self.r5.undraw()
            self.r6.undraw()
            self.r7.undraw()
            self.r8.undraw()
            self.r9.undraw()
            self.r10.undraw()
            self.r11.undraw()
            self.r12.undraw()
            self.r13.undraw()
            self.r14.undraw()
            self.r15.undraw()
            self.r16.undraw()
            self.r17.undraw()
            self.r18.undraw()
            self.r19.undraw()
            self.r20.undraw()
            self.r21.undraw()
            self.r22.undraw()
            
            self.score1.undraw()
            self.score2.undraw()
            self.score3.undraw()
            self.score4.undraw()
            
        self.drawn = True
        # Player 1 info
        self.rect1 = Rectangle(Point(10,410),Point(100,435))
        self.rect1.setFill(player1.get_color())
        self.rect1.draw(self.window)
        self.n1 = Text(Point(55,425), 'Player 1')
        self.n1.setSize(16)
        
        self.s1 = Text(Point(55,445), 'Items in Stock:')
        self.s1.setSize(14)
        self.s2 = Text(Point(30,460), player1.get_stock()[0])
        self.s3 = Text(Point(55,460), 'Roads')
        self.s4 = Text(Point(30,470), player1.get_stock()[1])
        self.s5 = Text(Point(70,470), 'Settlements')
        self.s6 = Text(Point(30,480), player1.get_stock()[2])
        self.s7 = Text(Point(53,480), 'Cities')

        self.r1 = Text(Point(75, 500), 'Resources Available:')
        self.r1.setSize(14)
        self.r2 = Text(Point(30,515), player1.get_resource_list().get_resource_list()[0])
        self.r3 = Text(Point(55,515), 'Grain')
        self.r4 = Text(Point(30,525), player1.get_resource_list().get_resource_list()[1])
        self.r5 = Text(Point(57,525), 'Sheep')
        self.r6 = Text(Point(30,535), player1.get_resource_list().get_resource_list()[2])
        self.r7 = Text(Point(57,535), 'Wood')
        self.r8 = Text(Point(30,545), player1.get_resource_list().get_resource_list()[3])
        self.r9 = Text(Point(55,545), 'Brick')
        self.r10 = Text(Point(30,555), player1.get_resource_list().get_resource_list()[4])
        self.r11 = Text(Point(50,555), 'Ore')
        
        self.score1 = Text(Point(26,575), 'Score:')
        self.score1.setSize(14)
        self.score2 = Text(Point(54,575), player1.get_score())
        self.score2.setSize(14)
        
        if player1.is_turn():   
            self.n1.setStyle('bold')
            self.n1.draw(self.window)
            
            self.s1.setStyle('bold')
            self.s1.draw(self.window)
            self.s2.setStyle('bold')
            self.s2.draw(self.window)
            self.s3.setStyle('bold')
            self.s3.draw(self.window)
            self.s4.setStyle('bold')
            self.s4.draw(self.window)
            self.s5.setStyle('bold')
            self.s5.draw(self.window)
            self.s6.setStyle('bold')
            self.s6.draw(self.window)
            self.s7.setStyle('bold')
            self.s7.draw(self.window)
            
            self.r1.setStyle('bold')
            self.r1.draw(self.window)
            self.r2.setStyle('bold')
            self.r2.draw(self.window)
            self.r3.setStyle('bold')
            self.r3.draw(self.window)
            self.r4.setStyle('bold')
            self.r4.draw(self.window)
            self.r5.setStyle('bold')
            self.r5.draw(self.window)
            self.r6.setStyle('bold')
            self.r6.draw(self.window)
            self.r7.setStyle('bold')
            self.r7.draw(self.window)
            self.r8.setStyle('bold')
            self.r8.draw(self.window)
            self.r9.setStyle('bold')
            self.r9.draw(self.window)
            self.r10.setStyle('bold')
            self.r10.draw(self.window)
            self.r11.setStyle('bold')
            self.r11.draw(self.window)
            
            self.score1.setStyle('bold')
            self.score1.draw(self.window)
            self.score2.setStyle('bold')
            self.score2.draw(self.window)
            
        else:
            self.n1.draw(self.window)
            
            self.s1.draw(self.window)
            self.s2.draw(self.window)
            self.s3.draw(self.window)
            self.s4.draw(self.window)
            self.s5.draw(self.window)
            self.s6.draw(self.window)
            self.s7.draw(self.window)
            
            self.r1.draw(self.window)
            self.r2.draw(self.window)
            self.r3.draw(self.window)
            self.r4.draw(self.window)
            self.r5.draw(self.window)
            self.r6.draw(self.window)
            self.r7.draw(self.window)
            self.r8.draw(self.window)
            self.r9.draw(self.window)
            self.r10.draw(self.window)
            self.r11.draw(self.window)
            
            self.score1.draw(self.window)
            self.score2.draw(self.window)
                    
        # Player 2  
        self.rect2 = Rectangle(Point(580,410),Point(670,435))
        self.rect2.setFill(player2.get_color())
        self.rect2.draw(self.window)
        self.n2 = Text(Point(625,425), 'Player 2')
        self.n2.setSize(16)
        
        self.s8 = Text(Point(615,445), 'Items in Stock:')
        self.s8.setSize(14)
        self.s9 = Text(Point(590,460), player2.get_stock()[0])
        self.s10 = Text(Point(615,460), 'Roads')
        self.s11 = Text(Point(590,470), player2.get_stock()[1])
        self.s12 = Text(Point(630,470), 'Settlements')
        self.s13 = Text(Point(590,480), player2.get_stock()[2])
        self.s14 = Text(Point(615,480), 'Cities')
        
        self.r12 = Text(Point(615, 500), 'Resources Available:')
        self.r12.setSize(14)
        self.r13 = Text(Point(590,515), player2.get_resource_list().get_resource_list()[0])
        self.r14 = Text(Point(615,515), 'Grain')
        self.r15 = Text(Point(590,525), player2.get_resource_list().get_resource_list()[1])
        self.r16 = Text(Point(617,525), 'Sheep')
        self.r17 = Text(Point(590,535), player2.get_resource_list().get_resource_list()[2])
        self.r18 = Text(Point(617,535), 'Wood')
        self.r19 = Text(Point(590,545), player2.get_resource_list().get_resource_list()[3])
        self.r20 = Text(Point(615,545), 'Brick')
        self.r21 = Text(Point(590,555), player2.get_resource_list().get_resource_list()[4])
        self.r22 = Text(Point(612,555), 'Ore')
        
        self.score3 = Text(Point(565,575), 'Score:')
        self.score3.setSize(14)
        self.score4 = Text(Point(592,575), player2.get_score())
        self.score4.setSize(14)
        
        if player2.is_turn():   
            self.n2.setStyle('bold')
            self.n2.draw(self.window)
            
            self.s8.setStyle('bold')
            self.s8.draw(self.window)
            self.s9.setStyle('bold')
            self.s9.draw(self.window)
            self.s10.setStyle('bold')
            self.s10.draw(self.window)
            self.s11.setStyle('bold')
            self.s11.draw(self.window)
            self.s12.setStyle('bold')
            self.s12.draw(self.window)
            self.s13.setStyle('bold')
            self.s13.draw(self.window)
            self.s14.setStyle('bold')
            self.s14.draw(self.window)
            
            self.r12.setStyle('bold')
            self.r12.draw(self.window)
            self.r13.setStyle('bold')
            self.r13.draw(self.window)
            self.r14.setStyle('bold')
            self.r14.draw(self.window)
            self.r15.setStyle('bold')
            self.r15.draw(self.window)
            self.r16.setStyle('bold')
            self.r16.draw(self.window)
            self.r17.setStyle('bold')
            self.r17.draw(self.window)
            self.r18.setStyle('bold')
            self.r18.draw(self.window)
            self.r19.setStyle('bold')
            self.r19.draw(self.window)
            self.r20.setStyle('bold')
            self.r20.draw(self.window)
            self.r21.setStyle('bold')
            self.r21.draw(self.window)
            self.r22.setStyle('bold')
            self.r22 .draw(self.window)
            
            self.score3.setStyle('bold')
            self.score3.draw(self.window)
            self.score4.setStyle('bold')
            self.score4.draw(self.window)
            
        else:
            self.n2.draw(self.window)
            
            self.s8.draw(self.window)
            self.s9.draw(self.window)
            self.s10.draw(self.window)
            self.s11.draw(self.window)
            self.s12.draw(self.window)
            self.s13.draw(self.window)
            self.s14.draw(self.window)
            
            self.r12.draw(self.window)
            self.r13.draw(self.window)
            self.r14.draw(self.window)
            self.r15.draw(self.window)
            self.r16.draw(self.window)
            self.r17.draw(self.window)
            self.r18.draw(self.window)
            self.r19.draw(self.window)
            self.r20.draw(self.window)
            self.r21.draw(self.window)
            self.r22.draw(self.window)
            
            self.score3.draw(self.window)
            self.score4.draw(self.window)
                       
    def show_info(self,player):  
        '''Displays and allows button clicks to build things during the player's turn.'''
        self.player = player       
        
        # Each type of build button is active only if player has sufficient resources.
        if self.build.clicked(self.p):            
            self.settle_butt = RectangleButton(Point(350, 85), 80, 20, 'Settlement')
            self.settle_butt.draw(self.window)
            if player.get_resource_list().get_resource_list()[0] > 0 and \
                player.get_resource_list().get_resource_list()[1] > 0 and \
                player.get_resource_list().get_resource_list()[2] > 0 and \
                player.get_resource_list().get_resource_list()[3] > 0:
                self.settle_butt.activate()
            
            self.road_butt = RectangleButton(Point(250, 85), 60, 20, 'Road')
            self.road_butt.draw(self.window)
            if player.get_resource_list().get_resource_list()[2] > 0 and \
                player.get_resource_list().get_resource_list()[3] > 0:
                self.road_butt.activate()
            
            self.upgrade_butt = RectangleButton(Point(470,85), 115, 20, \
                    'Upgrade Settlement')
            self.upgrade_butt.draw(self.window)
            if player.get_resource_list().get_resource_list()[0] > 2 and \
                player.get_resource_list().get_resource_list()[4] > 1:
                self.upgrade_butt.activate()
            
            q = self.window.getMouse()
            
            # If clicks are within certain radius of a corner, settlement is drawn.
            if self.settle_butt.clicked(q) and self.player.get_stock()[1] > 0:
                self.make_set(player)
                self.settle_butt.undraw()
                self.road_butt.undraw()
                self.upgrade_butt.undraw()
            
            # If clicks are within certain radius, a road is drawn.
            elif self.road_butt.clicked(q) and self.player.get_stock()[0] > 0:
                self.make_road(player)
                self.settle_butt.undraw()
                self.road_butt.undraw()
                self.upgrade_butt.undraw()
            
            # If click is within a certain radius of a corner and on an existing 
            # settlement, it is upgraded to be a city.
            elif self.upgrade_butt.clicked(q) and self.player.get_stock()[2] > 0:
                r = self.window.getMouse()
 
                self.corner_bounds_list = []
                
                for j in self.corner_list:
                    b1 = j.get_bounds(r)
                    self.corner_bounds_list.append(b1)

                for i in self.corner_bounds_list:
                    if i:    
                        index = self.corner_bounds_list.index(i)
                        if self.corner_list[index] in player.get_set_list():
                            ind = player.get_set_list().index(self.corner_list[index])
                            self.corner_list[index].upgrade(player, 
                                self.player.get_set_list()[ind], self.window)
                            self.player.add_city(self.corner_list[index])

                    else:
                        self.settle_butt.undraw()
                        self.road_butt.undraw()
                        self.upgrade_butt.undraw()
                self.settle_butt.undraw()
                self.road_butt.undraw()
                self.upgrade_butt.undraw()
            
            else:
                self.settle_butt.undraw()
                self.road_butt.undraw()
                self.upgrade_butt.undraw() 
                      
    def get_window(self):
        return self.window
    
    def close(self):
        self.window.getMouse()
        self.window.close() 

class Instructions():
    ''''Opens a window with game instructions.'''
    def __init__(self):
        self.window = GraphWin('Instructions', 600, 700)
        self.window.setBackground('white')
        self.roll = None
        self.drawn = False
        title = Text(Point(300,25), 'Instructions for The Settlers of Catan')
        title.setStyle('bold')
        title.setSize(20)
        title.setFill('darkgreen')
        title.draw(self.window)
        
        adapt = Text(Point(300,50), '*As simplified from the original board game \
by Laura Colbran and Omar Kaufman.*')
        adapt.setFill('darkblue')
        adapt.draw(self.window)
        
        goal = Text(Point(300,75), 'The Goal of the Game')
        goal.setStyle('bold')
        goal.draw(self.window)
        
        Text(Point(300,90), 'The goal of this game is to be the first player\
 to settle the island. This is determined by the number').draw(self.window)
        Text(Point(300,105), 'of victory points accumulated. Building settlements\
 and upgrading them to cities are worth 1 victory point each.').draw(self.window)
        Text(Point(300,120), 'The first player to 8 victory points wins.').draw(self.window)
        
        setup = Text(Point(300,145), 'Game Set-up')
        setup.setStyle('bold')
        setup.draw(self.window)
        Text(Point(300,160), 'Player 1 starts immediately after the window opens.\
 Click a corner to place a settlement, then click 2 adjacent') .draw(self.window)
        Text(Point(300,175), 'corners to draw a road. The road must be drawn \
connecting to settlement. After Player 1 has laid their first').draw(self.window)
        Text(Point(300,190), 'settlement and road, Player 2 does the same. Then\
 Player 2 lays another pair, followed by Player 1. Click the').draw(self.window)
        Text(Point(300,205), '"Start Turn & Roll" button, and game will \
proceed to normal play.').draw(self.window)
        
        play = Text(Point(300,230), 'Game Play')
        play.setStyle('bold')
        play.draw(self.window)
        Text(Point(300,245), 'Play is turn-based, with each player rolling\
 the die and having the opportunity to expand. With each turn players').draw(self.window)
        Text(Point(300,260), 'receive resources from hexes touching corners \
 where their settlements and cities are placed. During set-up,').draw(self.window)
        Text(Point(300,275), 'Players only receive resources from the second\
 settlement they placed. After that, they get one resource from').draw(self.window)
        Text(Point(300,290), 'each hex touching any settlement. Cities gain\
 two resources from each adjacent hex. The five resources').draw(self.window)
        Text(Point(300,305), 'available are Grain, Sheep, Lumber, Brick,\
 and Ore. These are yielded from plain, pasture, forest, hill, and').draw(self.window)
        Text(Point(300,320), 'mountain hexes respectively. The final land type\
 is the desert, which produces no resources. Resources are only').draw(self.window)
        Text(Point(300,335), "produced when their numbers, as indicated\
 in the center of each hex, are rolled. 6's and 8's are most common.").draw(self.window)
        Text(Point(300,360), 'During each turn, players have the opportunity\
 to build additional roads and settlements or upgrade existing').draw(self.window)
        Text(Point(300,375), "settlements. Each costs a certain amount of\
 resources from the player's hand. Settlements cost one brick, one").draw(self.window)
        Text(Point(300,390), "wood, one grain and one sheep to build. Roads\
 cost one wood and one brick each. Upgrading a settlement costs").draw(self.window)
        Text(Point(300,405), 'three grain and two ore. Cities are represented\
 by a darker coloured circle. With the exception of setup,').draw(self.window)
        Text(Point(300,420), 'settlements must connect to a preexisting road and be\
 at least 2 corners from the nearest neighbour. Roads also').draw(self.window)
        Text(Point(300,435), 'must be drawn connecting to another road or to\
 a settlement or city.').draw(self.window)
        
        rob = Text(Point(300,450), 'Robber')
        rob.setStyle('bold')
        rob.draw(self.window)
        Text(Point(300,465), 'The robber is represented by a pale cream circle\
 placed on a hex. It starts out on the desert, but every time').draw(self.window)
        Text(Point(300,480), 'a seven is rolled, the player whose turn it is\
 clicks the center of a hex to indicate where the robber').draw(self.window)
        Text(Point(300,495), ' should be placed. When it is on a hex, the hex\
 is unable to produce resources.').draw(self.window)
        
        diff = Text(Point(300,520), 'Differences from Original Board Game')
        diff.setStyle('bold')
        diff.draw(self.window)
        Text(Point(300,535), 'Unlike the original game, this version does not\
 permit trading with other players or with a "bank." Because of this,').draw(self.window)
        Text(Point(300,550), 'placement strategie for settlements is even more\
 important. This is also why the game only goes to 8 victory points.').draw(self.window)
        Text(Point(300,565), 'Due to the complexity of the programming such things,\
 we also ignored ports and Development Cards.').draw(self.window)
 
        fun = Text(Point(300,630), 'Have fun!')
        fun.setSize(20)
        fun.setStyle('bold')
        fun.setFill('firebrick')
        fun.draw(self.window)
        
class SettlersGame():
    '''Creates a template for the game.'''
    def __init__(self):
        self.player_1 = Player(1,'royalblue', 'darkblue')
        self.player_2 = Player(2, 'thistle', 'purple')       
        self.board = Interface()
        self.rules = Instructions()        
        self.player_2.switch_turn()
    
    # Allows players to set up initial settlements and roads in correct order.    
    def start(self):
        self.board.start_game(self.player_1)
        self.board.start_game(self.player_2)
        self.board.start_game(self.player_2)
        self.board.start_game(self.player_1)
    
    # manages gameplay until a player wins
    def play(self):
        while self.board.game_not_over():
            self.board.roll_button_actions(self.player_1, self.player_2)
            # Calls show_info() for whichever player has the turn.
            if self.board.is_quit_clicked():
                self.board.end_game()
            if self.player_1.is_turn():
                self.board.show_info(self.player_1)
            else:
                self.board.show_info(self.player_2)
                        
            if self.player_1.get_score() == 8 or self.player_2.get_score() == 8:
                if self.player_1.get_score() == 8:
                    yay = Text(Point(350,620), 'Player 1 Wins!')
                    yay.setSize(30)
                    yay.setFill('black')
                    yay.setStyle('bold')
                    yay.draw(self.board.get_window())
                else:
                    yay = Text(Point(350,620), 'Player 2 Wins!')
                    yay.setSize(30)
                    yay.setFill('black')
                    yay.setStyle('bold')
                    yay.draw(self.board.get_window())                
                self.board.end_game()
        self.board.close() 
        
                               
def main():
    game = SettlersGame()
    game.start()
    game.play()
            
if __name__ == '__main__':
    main()
