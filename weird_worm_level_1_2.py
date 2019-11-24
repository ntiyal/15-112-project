

import pygame
from pygame.locals import *
from pygame.color import *
from math import sqrt,pow
import pymunk
from pymunk import Vec2d
from pymunk import pygame_util


### Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_LINE = 1
COLLTYPE_BALL = 2


def flipy(y):
    """ convert pymunk coordinates to pygame coordinates"""
    return -y+600

## calculates the center of gravity form list of coorndinates of all positions of the body
def calculateCG(positions):
        Ycg = 0
        Xcg = 0
        tot = len(positions)
        for (x,y) in positions:
            Ycg += y
            Xcg += x
        return (round(Xcg/tot),round(Ycg/tot))

## callbacks functions for collision handler
def coll_begin(arbiter,space,data):
    return True
def coll_pre_solve(arbiter,space,data):
    return True
def coll_post_solve(arbiter,space,data):
    print("post  solve")
def coll_separate(arbiter,space,data):
    print("separated")

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

def main():
    running = True
    ### Physics stuff
    space = pymunk.Space()
    space.gravity = 0.0, -700.0

    ## 
    options = pymunk.pygame_util.DrawOptions(screen)
    

    #collision
    
    coll = space.add_collision_handler(COLLTYPE_BALL, COLLTYPE_LINE)
    coll.data["surface"] = screen
    coll._post_solve = coll_post_solve

    ## Balls
    # storing the ball bodies
    positions = []
    # storind the shape of the ball (circles)
    shapepositions = []
    

    ### creating ground and boundaries
    Left_bound = pymunk.Segment(space.static_body, (600,0),(600,600),25)
    Right_bound = pymunk.Segment(space.static_body, (0,0),(0,600),25)
    ground_shape = pymunk.Segment(space.static_body, (0,0),(600,0),25)
    Top_bound = pymunk.Segment(space.static_body, (0,600),(600,600),25)
    Top_bound.collision_type = COLLTYPE_LINE
    ground_shape.collision_type = COLLTYPE_LINE
    Left_bound.collision_type = COLLTYPE_LINE
    Right_bound.collision_type = COLLTYPE_LINE
    space.add(ground_shape,Right_bound,Left_bound,Top_bound)
    
    ### list to join bodies with the joints
    bodies = []
    
    ### creating ball object for level 1
    moment = pymunk.moment_for_circle(25,0,50)
    ball = pymunk.Body(25,moment)
    shape = pymunk.Circle(ball,50)
    ball.position = (300,75)
    space.add(ball,shape)
    '''
    ### creating balance object for level 2
    moment1 = pymunk.moment_for_segment(200,(-100,0),(100,0),5)
    moment2 = pymunk.moment_for_segment(200,(0,0),(0,-100),5)
    balance = pymunk.Body(400,moment1+moment2)
    shape1 = pymunk.Segment(balance,(-100,0),(100,0),5)
    shape2 = pymunk.Segment(balance,(0,0),(0,-100),5)
    balance.position = (300,125)
    space.add(balance,shape1,shape2)
    '''
    ### creating main body


    run_physics = False
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == MOUSEMOTION:
                if event.buttons[0]:
                    positions = []
                    run_physics = False
                    p = event.pos[0], flipy(event.pos[1])
                    moment = pymunk.moment_for_circle(10,0,12)
                    body = pymunk.Body(10,moment)
                    
                    body.position = p
                    bodies.append(body)

                    shape = pymunk.Circle(body,12)
                    
                    shape.friction = 0.5
                    shape.collision_type = COLLTYPE_BALL
                    space.add(body,shape)
                    shapepositions.append(shape)
                    
                    ## joining the bodies with joints (strings)
                    if len(bodies) == 2:
                        joint = pymunk.constraint.PinJoint(bodies[0],bodies[1])
                        joint._set_collide_bodies(False)

                        bodies = bodies[1:]
                        space.add(joint)
                        
                    '''
                    ## joining the bodies by joining the shapes
                    if len(bodies) == 2 and len(shapepositions) == 2:
                        
                        print("i hate you")
                        (x1,y1) = bodies[0].position
                        (x2,y2) = bodies[1].position
                        x = (x1+x2)//2
                        y = (y1+y2)//2
                        mass = bodies[0].mass + bodies[1].mass
                        moment = bodies[0].moment + bodies[1].moment
                        new_body = pymunk.Body(mass,moment)

                        new_body.position = (x,y)
                        new_body_shape1 = pymunk.Circle(new_body,12,(-abs(x-x1),-abs(y-y1)))
                        new_body_shape2 = pymunk.Circle(new_body,12,(abs(x-x2),abs(y-y2)))
                        new_body_shape = pymunk.Segment(new_body,(-abs(x-x1),-abs(y-y1)),(abs(x-x2),abs(y-y2)),12)
                        
                        space.remove(bodies[0],shapepositions[0],bodies[1],shapepositions[1])
                        space.add(new_body,new_body_shape,new_body_shape1,new_body_shape2)
                        shapepositions = [[new_body_shape2,new_body_shape,new_body_shape1]]
                        bodies = [new_body]
                        allshapes.append(new_body_shape1)
                    '''
            elif event.type == MOUSEBUTTONDOWN and event.button == 3: 
                pass
            elif event.type == MOUSEBUTTONUP : 
                run_physics = True
                
    
        
        ### Update physics
        if run_physics:
            dt = 1.0/60.0
            for x in range(1):
                space.step(dt)
                positions =[]

        ### Update screen
        screen.fill(THECOLORS["black"])

        ### Show pymunk objects
        space.debug_draw(options)
        
        ### getting all the positions of the shapes
        for ball in shapepositions:           
            v = ball.body.position
            p = int(v.x), int(flipy(v.y))

            ### drawing with pygame the main object according to pymunk coordinates
            pygame.draw.circle(screen, THECOLORS["white"], p, 12)
            positions.append(p)
               

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("LEVEL 0   fps: " + str(clock.get_fps()))

    pygame.quit()
def startScreen():
    font_name = pygame.font.match_font("arial")
    screen.fill(THECOLORS["black"])
    font = pygame.font.Font(font_name,22)
    text_surface = font.render("Start Game ----------> Press any key to start",True,THECOLORS["white"])
    text_rect = text_surface.get_rect()
    text_rect.midtop = (300,300)
    screen.blit(text_surface,text_rect)
    pygame.display.flip()
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
                pygame.quit()
            if event.type == pygame.KEYUP:
                wait = False
                main()

startScreen()

