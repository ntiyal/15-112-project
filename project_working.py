

import pygame

import time
from pygame.locals import *
from pygame.color import *
from math import sqrt,pow
import pymunk
from pymunk import Vec2d
from pymunk import pygame_util

pygame.font.init()

### Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_LINE = 1
COLLTYPE_BALL = 2
COLLTYPE_LEVEL3 = 3
COLLTYPE_GROUND = 4
COLLTYPE_RIGHT = 5
COLLTYPE_ROOF = 6

def flipy(y):
    """ convert pymunk coordinates to pygame coordinates"""
    return -y+600
def flip(positions):
    res = []
    for (x,y) in positions:
        res.append((x,flipy(y)))
    return res

## calculates the center of gravity form list of coorndinates of all positions of the body
def calculateCG(positions):
    if positions:
        Ycg = 0
        Xcg = 0
        tot = len(positions)
        for (x,y) in positions:
            Ycg += y
            Xcg += x
        return (round(Xcg/tot),round(Ycg/tot))

def rel(p,positions):
    res = []
    (x,y) = p
    for (a,b) in positions:
        res.append((a-x,b-y))
    return res

def relToCG(positions):
    res = []
    if positions:
        (x,y) = calculateCG(positions)
        for (a,b) in positions:
            res.append((a-x,b-y))
        return res

## function that fills in the drawing with pygame (with recursion)
def fillIn(screen, positions):
    if len(positions) <= 1:
        return 
    distance = sqrt(pow((positions[0][0]-positions[1][0]),2)+pow((positions[0][1]-positions[1][1]),2))
    if distance >= 10:
        if positions[0][0]-positions[1][0] != 0:
            pygame.draw.line(screen, (255, 255, 255), (positions[0][0],positions[0][1]), (positions[1][0],positions[1][1]), 25)
    return fillIn(screen, positions[1:])

## same in pymunk
def fillShape(space,body,positions):
    if len(positions) <= 1:
        return 
    distance = sqrt(pow((positions[0][0]-positions[1][0]),2)+pow((positions[0][1]-positions[1][1]),2))
    if distance >= 10:
        if positions[0][0]-positions[1][0] != 0:
            shape = pymunk.Segment(body,(positions[0][0],positions[0][1]), (positions[1][0],positions[1][1]), 12)
            shape.friction = 0.5
            #shape.color = (255,255,255)
            space.add(shape)
    return fillShape(space, body, positions[1:])

## callbacks functions for collision handler

def coll_pre_solve(arbiter,space,data):
    return True
def coll_post_solve(arbiter,space,data):
    print("post  solve")





class gameScreen():
    def __init__(self,level):
        self.level = level
        self.count = 0
        self.c = 0
        self.sart_time = 0.0

        self.font=pygame.font.match_font("Curlz MT")
        self.x_start = 25
        self.x_end = 575
        self.y_start = 25
        self.y_end = 575
        ### Domain lists
        self.x_values = []
        self.y_values = []
        self.run = True
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        if self.level == 0:
            self.start()
        else:
            self.main()
    

    def customDomain(self,x,y):
        if x not in self.x_values and y not in self.y_values:
            return True
        return False

    def domain(self,x,y):
        if self.x_start < x < self.x_end and self.y_start < y < self.y_end:
            return True
        return False

    def text_objects(self,text, font):
        textSurface = font.render(text, True, (255,255,255))
        return textSurface, textSurface.get_rect()

    def squareButton(self,size,msg,x,y,w,h,action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen,(88,159,224,225),(x,y,w,h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, (90,110,223,255),(x,y,w,h))
        pygame.font.init()
        smallText = pygame.font.Font(self.font,size)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), y+h+10 )
        self.screen.blit(textSurf, textRect)
        

    def write(self,text):
        pygame.font.init()
        smallText = pygame.font.Font(self.font,25)
        textSurf, textRect = self.text_objects(text, smallText)
        textRect.center = (300,300)
        self.screen.blit(textSurf, textRect)
        
        
    def display(self):
        if self.level == 1:
            self.write("Make the ball hit the left wall")
        if self.level == 2:
            self.write("Make the ball touch the ground")
        if self.level == 3:
            self.write("Make exactly two balls fall in the glass")
        if self.level == 4:
            self.write("Make the ball touch the ground")
        if self.level == 5:
            self.write("Make the ball touch the right wall")
        if self.level == 6:
            self.write("Make the ball touch the left wall")
        if self.level == 7:
            self.write("Make the ball fall inside the glass")
        if self.level == 8:
            self.write("Make an object touch the roof")
        if self.level == 9:
            self.write("Make an object fall inside the glass")


    def button(self,msg,x,y,r,ic,ac,action=None):
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        d = sqrt((x-mouse[0])**2+(y-mouse[1])**2)
        if 0 < d < r+5 :
            pygame.draw.circle(self.screen, ac,(x,y),r)

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.circle(self.screen, ic,(x,y),r)
        if msg:
            pygame.font.init()

            smallText = pygame.font.Font(self.font,25)
            textSurf, textRect = self.text_objects(msg, smallText)
            textRect.center = (x,y+r*2)
            self.screen.blit(textSurf, textRect)



    def coll_begin(self,arbiter,space,data):
        
        if self.level == 1:
            self.count = 0
            self.waitScreen()
        if self.level == 2:
            self.count = 0
            self.waitScreen()
        if self.level == 3:
            self.c+=1
            if self.c == 2:
                self.count = 0
                self.waitScreen()
        if self.level == 4:
            self.count = 0
            self.waitScreen()
        if self.level == 5:
            self.count = 0
            self.waitScreen()
        if self.level == 6:
            self.count = 0
            self.waitScreen()
        if self.level == 7:
            self.count = 0
            self.waitScreen()
            
        if self.level == 8:
            self.count = 0
            self.waitScreen()
        if self.level == 9:
            self.count = 0
            self.waitScreen()
        return True
    def waitScreen(self):
        background = pygame.image.load('Game LOGO.jpeg')
        lvl = pygame.image.load("Level_button.png")
        lvl = pygame.transform.scale(lvl,(90,90)) 
        playAgain = pygame.image.load("PlayAgain_button.png")
        playAgain = pygame.transform.scale(playAgain,(75,75))
        Next = pygame.image.load("Next_button.png")
        Next = pygame.transform.scale(Next,(90,90))
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    quit()
            self.screen.fill(THECOLORS["black"])
            self.screen.blit(background,(0,0))
            
            self.button("Go to levels",130,430,40,(90,110,223,255),(88,159,224,225),action=self.levelScreen)
            self.button("Play again!",300,430,40,(90,110,223,255),(88,159,224,225),action=self.goToSameLevel)
            if self.level < 8:
                self.button("Go to next level",470,430,40,(90,110,223,255),(88,159,224,225),action=self.goToNextLevel)
                self.screen.blit(Next,(425,385))

            self.screen.blit(lvl,(85,385))
            self.screen.blit(playAgain,(262,392))
            pygame.display.update()
        
    def goToLevel(self,level):
        self.level=level
        return self.main
    def goToNextLevel(self):
        if self.count==0:
            self.level+=1
            self.count+=1
        return self.main()
    def goToSameLevel(self):
        if self.count==0:
            self.level=self.level
            self.count+=1
        return self.main()
    def levelScreen(self):
        home = pygame.image.load("home_button.png")
        home = pygame.transform.scale(home,(28,28))
        level_1 = pygame.image.load("level1_button.png")
        level_1 = pygame.transform.scale(level_1,(90,90))
        level_2 = pygame.image.load("level2_button.png")
        level_2 = pygame.transform.scale(level_2,(90,90))
        level_3 = pygame.image.load("level3_button.png")
        level_3 = pygame.transform.scale(level_3,(90,90))
        level_4 = pygame.image.load("level4_button.png")
        level_4 = pygame.transform.scale(level_4,(90,90))
        level_5 = pygame.image.load("level5_button.png")
        level_5 = pygame.transform.scale(level_5,(90,90))
        level_6 = pygame.image.load("level6_button.png")
        level_6 = pygame.transform.scale(level_6,(90,90))
        level_7 = pygame.image.load("level7_button.png")
        level_7 = pygame.transform.scale(level_7,(90,90))
        level_8 = pygame.image.load("level8_button.png")
        level_8 = pygame.transform.scale(level_8,(90,90))
        level_9 = pygame.image.load("level9_button.png")
        level_9 = pygame.transform.scale(level_9,(90,90))

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    quit()
            self.screen.fill(THECOLORS["black"])
            self.squareButton(25,"Level 0",75,75,100,100,self.goToLevel(1))
            self.squareButton(25,"Level 1",250,75,100,100,self.goToLevel(2))
            self.squareButton(25,"Level 2",425,75,100,100,self.goToLevel(3))
            self.squareButton(25,"Level 3",75,250,100,100,self.goToLevel(4))
            self.squareButton(25,"Level 4",250,250,100,100,self.goToLevel(5))
            self.squareButton(25,"Level 5",425,250,100,100,self.goToLevel(6))
            self.squareButton(25,"Level 6",75,425,100,100,self.goToLevel(7))
            self.squareButton(25,"Level 7",250,425,100,100,self.goToLevel(8))
            self.squareButton(25,"Level 8",425,425,100,100,self.goToLevel(9))
            ## level images
            self.screen.blit(level_1,(80,80))
            self.screen.blit(level_2,(255,80))
            self.screen.blit(level_3,(430,80))
            self.screen.blit(level_4,(80,255))
            self.screen.blit(level_5,(255,255))
            self.screen.blit(level_6,(430,255))
            self.screen.blit(level_7,(80,430))
            self.screen.blit(level_8,(255,430))
            self.screen.blit(level_9,(430,430))

            
            ##Go to start screen button
            self.button("",25,570,20,(90,110,223,255),(88,159,224,225),action=self.start)
            self.screen.blit(home,(10,555))
            
            pygame.display.update()
        
    def start(self):
        background = pygame.image.load('Game LOGO.jpeg')
        lvl = pygame.image.load("Level_button.png")
        lvl = pygame.transform.scale(lvl,(90,90)) 
        Next = pygame.image.load("Next_button.png")
        Next = pygame.transform.scale(Next,(90,90))
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    quit()
            self.screen.fill(THECOLORS["black"])
            self.screen.blit(background,(0,0))
            
            self.button("Go to levels",180,430,40,(90,110,223,255),(88,159,224,225),action=self.levelScreen)
            self.button("Play",420,430,40,(90,110,223,255),(88,159,224,225),action=self.goToLevel(1))
            
            self.screen.blit(lvl,(135,385))
            self.screen.blit(Next,(375,385))

            pygame.display.update()

    def main(self):
        self.count = 0
        once = True
        clock = pygame.time.Clock()
        
        
        ### Physics stuff
        space = pymunk.Space()
        space.gravity = 0.0, -1000.0
        space.collision_slop = 0.0

        ## 
        options = pymunk.pygame_util.DrawOptions(self.screen)

        ## Balls
        # storing the ball bodies
        positions = []
        
        ### creating ground and boundaries
        Right_bound = pymunk.Segment(space.static_body, (600,0),(600,600),25)
        Left_bound = pymunk.Segment(space.static_body, (0,0),(0,600),25)
        ground_shape = pymunk.Segment(space.static_body, (0,0),(600,0),25)
        Top_bound = pymunk.Segment(space.static_body, (0,600),(600,600),25)
        Top_bound.friction = 0.5
        Left_bound.friction = 0.5
        Right_bound.friction = 0.5
        ground_shape.friction = 0.5
        Top_bound.collision_type = COLLTYPE_ROOF
        ground_shape.collision_type = COLLTYPE_GROUND
        Left_bound.collision_type = COLLTYPE_LINE
        Right_bound.collision_type = COLLTYPE_RIGHT
        space.add(ground_shape,Right_bound,Left_bound,Top_bound)
        
        
        
        if self.level == 1:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 25
            self.y_end = 575
            
            ### dynamic objects: ball
            ### objective: make the ball hit the left wall
            #collision
            coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_LINE)
            coll.begin = self.coll_begin
            #objects
            moment = pymunk.moment_for_circle(25,0,50)
            ball = pymunk.Body(25,moment)
            shape = pymunk.Circle(ball,50)
            shape.collision_type = COLLTYPE_BALL
            shape.friction = 0.5
            #shape.color = (255,0,0)
            ball.position = (300,75)
            space.add(ball,shape)
            # Domain
            self.x_values += [shape.body.position[0]]
            self.y_values += [shape.body.position[1]]

        if self.level == 2:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 25
            self.y_end = 575            
            ### dynamic objects: ball on top of cross
            ### objective: make the ball touch the ground
            #collision
            coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_GROUND)
            coll.begin = self.coll_begin
            #objects
            moment = pymunk.moment_for_circle(15,0,15)
            ball = pymunk.Body(15,moment)
            shape = pymunk.Circle(ball,15)
            shape.collision_type = COLLTYPE_BALL
            shape.friction = 0.5
            ball.position = (300,150)
            space.add(ball,shape)

            moment1 = pymunk.moment_for_segment(200,(-50,-100),(50,100),10)
            moment2 = pymunk.moment_for_segment(200,(-50,100),(50,-100),10)
            cross = pymunk.Body(400,moment1+moment2)
            shape1 = pymunk.Segment(cross,(-50,-100),(50,100),10)
            shape2 = pymunk.Segment(cross,(-50,100),(50,-100),10)
            
            cross.position = (300,125)
            space.add(cross,shape1,shape2)

            self.x_values = [shape1.body.position[0],shape2.body.position[0]]
            self.y_values = [shape1.body.position[1],shape2.body.position[1]]


        if self.level == 3:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 25
            self.y_end = 575            
            ### static objects: shelf
            ### dynamic objects: 3 balls, glass
            ### objective: make only 2 balls go inside the glass
            # collision
            coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_LEVEL3)
            coll.begin = self.coll_begin
            # objects
            shelf = pymunk.Segment(space.static_body, (25,300),(150,300),10)

            moment1 = pymunk.moment_for_segment(200,(-100,-100),(100,-100),10)
            moment2 = pymunk.moment_for_segment(200,(-100,100),(-100,-100),10)
            moment3 = pymunk.moment_for_segment(200,(100,100),(100,-100),10)
            glass = pymunk.Body(600,moment1+moment2+moment3)
            glass.position = (300,150)
            shape1 = pymunk.Segment(glass,(-100,-100),(100,-100),10)
            shape2 = pymunk.Segment(glass,(-100,100),(-100,-100),10)
            shape3 = pymunk.Segment(glass,(100,100),(100,-100),10)
            shape1.friction = 0.5
            shape2.friction = 0.5
            shape3.friction = 0.5
            shape1.collision_type = COLLTYPE_LEVEL3
            moment = pymunk.moment_for_circle(50,0,10)
            ball1 = pymunk.Body(50,moment)
            ball2 = pymunk.Body(50,moment)
            ball3 = pymunk.Body(50,moment)
            ball1.position = (50,320)
            ball2.position = (70,320)
            ball3.position = (90,320)

            circ1 = pymunk.Circle(ball1,10)
            circ2 = pymunk.Circle(ball2,10)
            circ3 = pymunk.Circle(ball3,10)
            circ1.friction = 0.5
            circ2.friction = 0.5
            circ3.friction = 0.5
            circ1.collision_type = COLLTYPE_BALL
            circ2.collision_type = COLLTYPE_BALL
            circ3.collision_type = COLLTYPE_BALL

            space.add(glass,ball1,ball2,ball3,circ1,circ2,circ3,shape1,shape2,shape3,shelf)
        
        if self.level == 4:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 25
            self.y_end = 575            
            ## Objects: ball inside the arc
            ## Objective: get the ball outside the arc
            #collision
            coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_GROUND)
            coll.post_solve = self.coll_begin
            # Creating objects
            moment = pymunk.moment_for_circle(15,0,15)
            ball = pymunk.Body(15,moment)
            shape = pymunk.Circle(ball,15)
            shape.collision_type = COLLTYPE_BALL
            shape.friction = 0.5
            ball.position = (300,64)
            space.add(ball,shape)
            moment_arc = pymunk.moment_for_circle(200,40,50)
            arc = pymunk.Body(200,moment_arc)
            arc.position = (300,89)
            space.add(arc)
            for x in range(-50,51):
                y1 = sqrt(2500-(x)**2)
                y2 = - sqrt(2500-(x)**2)
                if y1 < 40:
                    shape1 = pymunk.Segment(arc,(x-1,y1-1),(x,y1),7)
                    space.add(shape1)
                shape2 = pymunk.Segment(arc,(x-1,y2+1),(x,y2),7)
                space.add(shape2)
        
        if self.level == 5:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 25
            self.y_end = 575           
            ## Objects: Segments to make an arc, ball that fits in the arc
            ## Objective: Make the ball touch the right wall
            # Collision
            coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_RIGHT)
            coll.post_solve = self.coll_begin
            # objects
            # static Objects
            shape = pymunk.Segment(space.static_body,(25,225),(225,225),5)
            middle = pymunk.Segment(space.static_body,(125,115),(125,135),5)
            ground = pymunk.Segment(space.static_body,(25,25),(575,25),5)
            space.add(shape,middle,ground)
            for x in range(126,225):
                y1 = sqrt(10000-(x-225)**2) + 125
                y2 = - sqrt(10000-(x-225)**2) + 125
                shape1 = pymunk.Segment(space.static_body,(x-1,y1-1),(x,y1),5)
                shape2 = pymunk.Segment(space.static_body,(x-1,y2+1),(x,y2),5)
                space.add(shape1,shape2)
            # dynamic objects
            moment = pymunk.moment_for_circle(400,80,90)
            ball = pymunk.Body(400,moment)
            ball.position = (225,125)
            space.add(ball)
            for x in range(-90,91):
                y1 = sqrt(8100-(x)**2)
                y2 = - sqrt(8100-(x)**2)
                shape1 = pymunk.Segment(ball,(x-1,y1-1),(x,y1),7)
                shape2 = pymunk.Segment(ball,(x-1,y2+1),(x,y2),7)
                shape1.friction = 0.5
                shape2.friction = 0.5
                shape1.collision_type = COLLTYPE_BALL
                shape2.collision_type = COLLTYPE_BALL
                space.add(shape1,shape2)

        if self.level == 6:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 25
            self.y_end = 575
            ## Objects: a ball inside a glass
            ## Objective: Make the ball hit the left wall
            # Collision
            coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_LINE)
            coll.post_solve = self.coll_begin
            # Objects
            moment = pymunk.moment_for_poly(300,[(225,225),(325,225),(225,25),(325,25)])
            glass = pymunk.Body(300,moment)
            glass.position = (300,85)
            line1 = pymunk.Segment(glass,(-50,50),(-50,-50),10)
            line2 = pymunk.Segment(glass,(-50,50),(50,50),10)
            line3 = pymunk.Segment(glass,(50,50),(50,-50),10)
            line1.friction = 0.5
            line2.friction = 0.5
            line3.friction = 0.5
            ball_moment = pymunk.moment_for_circle(50,0,12)
            ball = pymunk.Body(50,ball_moment)
            ball.position = (300,35)
            ball_shape = pymunk.Circle(ball,12)
            ball_shape.friction = 0.5
            ball_shape.collision_type = COLLTYPE_BALL
            space.add(glass,line1,line2,line3,ball,ball_shape)
            
        if self.level == 7:
            self.x_start = 25
            self.x_end = 300
            self.y_start = 25
            self.y_end = 575
            ## Objects: a ball on top of a bar and a glass/box
            ##Objective: Make the ball fall inside the glass
            ##Constraint: Can only draw in one half of the screen
            
            # Collision
            coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_LEVEL3)
            coll.post_solve = self.coll_begin
            # Constraint
            # Objects
            # Static
            bar = pymunk.Segment(space.static_body,(350,25),(350,125),12)
            space.add(bar)
            # Dynamic
            moment = pymunk.moment_for_circle(50,0,10)
            ball = pymunk.Body(50,moment)
            ball.position = (350,140)
            ball_shape = pymunk.Circle(ball,10)
            ball_shape.friction = 0.5
            ball_shape.collision_type = COLLTYPE_BALL
            moment = pymunk.moment_for_poly(200,[(-20,20),(-20,-20),(20,-20),(20,20)])
            glass = pymunk.Body(200,moment)
            glass.position = (500,45)
            line1 = pymunk.Segment(glass,(-20,20),(-20,-20),5)
            line2 = pymunk.Segment(glass,(-20,-20),(20,-20),5)
            line3 = pymunk.Segment(glass,(20,-20),(20,20),5)
            line2.collision_type = COLLTYPE_LEVEL3
            line1.friction = 0.5
            line2.friction = 0.5
            line3.friction = 0.5
            space.add(glass,ball,ball_shape,line1,line2,line3)

        if self.level == 8:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 25
            self.y_end = 400
            # no object
            # Objectif: Make an object hit the roof
            # Constraint: Can not draw in the upper quarter of the screen
            # Collision
            coll = space.add_collision_handler(COLLTYPE_DEFAULT, COLLTYPE_ROOF)
            coll.post_solve = self.coll_begin
    

        if self.level == 9:
            self.x_start = 25
            self.x_end = 575
            self.y_start = 300
            self.y_end = 575
            # static objects : 4 dots, hanging arc
            # dynamic object: open box
            # Objective: fill the box with any drawn object
            # Constraint: Can not draw in the upper half of the screen
            # Collision
            coll = space.add_collision_handler(COLLTYPE_DEFAULT, COLLTYPE_LEVEL3)
            coll.post_solve = self.coll_begin
            # Static object
            dot1 = pymunk.Body(body_type=pymunk.Body.STATIC)
            ball1 = pymunk.Circle(dot1,12)
            dot1.position = (250,100)
            dot2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            ball2 = pymunk.Circle(dot2,12)
            dot2.position = (200,125)
            dot3 = pymunk.Body(body_type=pymunk.Body.STATIC) 
            ball3 = pymunk.Circle(dot3,12)
            dot3.position = (350,100)
            dot4 = pymunk.Body(body_type=pymunk.Body.STATIC)
            ball4 = pymunk.Circle(dot4,12)
            dot4.position = (400,125)

            for x in range(276,326):
                y = sqrt(625-((x-300)**2))+275
                shape1 = pymunk.Segment(space.static_body,(x-1,y-1),(x,y),5)
                shape1.friction = 0.5
                space.add(shape1)

            # Dynamic object
            body = pymunk.Body(50,pymunk.moment_for_poly(50,[(275,75),(325,75),(275,25),(325,25)]))
            body.position = (300,75)
            shape1 = pymunk.Segment(body,(-25,25),(-25,-25),5)
            shape2 = pymunk.Segment(body,(-25,-25),(25,-25),5)
            shape3 = pymunk.Segment(body,(25,-25),(25,25),5)

            shape1.friction = 0.5
            shape2.friction =0.5
            shape3.friction = 0.5

            shape2.collision_type = COLLTYPE_LEVEL3
            space.add(shape1,shape2,shape3,body,ball1,ball2,ball3,ball4,dot1,dot2,dot3,dot4)

        run_physics = False
        positions = []
        objects = []
        p = (0,0)

        playAgain = pygame.image.load("PlayAgain_button.png")
        playAgain = pygame.transform.scale(playAgain,(28,28))
        home = pygame.image.load("home_button.png")
        home = pygame.transform.scale(home,(28,28))
        pause = pygame.image.load("pause_button.png")
        pause = pygame.transform.scale(pause,(28,28))
        qst = pygame.image.load("qst_button.png")
        qst = pygame.transform.scale(qst,(28,28))

        while self.run:


            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                    quit()
                
                elif event.type == MOUSEMOTION:
                    if event.buttons[0]:
                        
                        run_physics = False
                        p = int(event.pos[0]), int(flipy(event.pos[1]))
                        #print(self.x_values)
                        if self.domain(p[0],p[1]) and self.customDomain(p[0],p[1]):
                            positions.append(p)
                        
                elif event.type == MOUSEBUTTONUP : 
                    run_physics = True
                    once = True
                    moment = pymunk.moment_for_circle(10,0,12)
                    body = pymunk.Body(len(positions)*10,moment*len(positions))
                    if positions:
                        body.position = calculateCG(positions)
                        for p in relToCG(positions):
                            
                            obj = pymunk.Circle(body,12,p)
                            #obj.color = (255,255,255)
                            obj.friction = 0.5
                            obj.collision_type = COLLTYPE_DEFAULT
                            objects.append(obj)
                        space.add(objects,body)
                        fillShape(space,body,relToCG(positions))
                    positions = []
                    objects = []

            ### Update physics
            if run_physics:
                
                dt = 1.0/60.0
                for x in range(1):
                    space.step(dt)
                    

            ### Update self.screen
            self.screen.fill(THECOLORS["black"])
            if self.level == 7:
                self.screen.fill((170,4,19,255),(300,0,300,600))
            if self.level == 8:
                self.screen.fill((170,4,19,255),(0,0,600,200))
            if self.level == 9:
                self.screen.fill((170,4,19,255),(0,300,600,300))
            
                
            ### Show pymunk objects
            space.debug_draw(options)
            
            ### getting all the positions of the shapes
            for (x,y) in flip(positions):           
                
                pygame.draw.circle(self.screen, THECOLORS["white"], (x,y), 12)
            
            fillIn(self.screen, flip(positions))
            ##Play Again button
            self.button("",585,585,20,(90,110,223,255),(88,159,224,225),action=self.main)
            
            self.screen.blit(playAgain,(570,570))
            ##Go to start screen button
            self.button("",15,585,20,(90,110,223,255),(88,159,224,225),action=self.start)
            
            self.screen.blit(home,(1,568))
            ##Pause button
            self.button("",15,15,20,(90,110,223,255),(88,159,224,225),action=self.waitScreen)
           
            self.screen.blit(pause,(1,1))
            ##More info button
            ## Instructions
            self.button("",585,15,20,(90,110,223,255),(88,159,224,225),action=self.display)
           
            self.screen.blit(qst,(570,2))
            
            ### Flip self.screen
            
            pygame.display.flip()
            self.screen.fill(THECOLORS["black"])
            clock.tick(50)
            pygame.display.set_caption("KineDRAWtics")
            
        

game = gameScreen(0)

