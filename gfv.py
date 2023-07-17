import pygame as pg
import math
from sys import exit
import itertools
class Circle(pg.sprite.Sprite):
    def __init__(self,radius,start_pos,mass,x_vel,y_vel):
        super().__init__()
        self.image=pg.Surface([(radius*2),(radius*2)])
        self.image.fill('Black')
        self.rect=self.image.get_rect(center=start_pos)
        pg.draw.circle(self.image,'White',(radius,radius),radius,0)

        self.radius=radius
        self.mass=mass

        self.x_pos=start_pos[0]
        self.x_vel=x_vel
        self.x_acc=0

        self.y_pos=start_pos[1]
        self.y_vel=y_vel
        self.y_acc=0

        self.net_x_acc=0
        self.net_y_acc=0
        self.drawn=False
        self.collided=False
    def update_pos(self):
        self.rect.center=(round(self.x_pos),round(self.y_pos))

    def animate(self):
        #Euler integration
        self.x_vel+=self.x_acc
        self.y_vel+=self.y_acc

        self.x_pos+=self.x_vel
        self.y_pos+=self.y_vel
        self.update_pos()
    def still_draw(self):
        pg.draw.circle(screen,"White",(self.x_pos,self.y_pos),self.radius)
    def gravitate(self,othercircle):

        dx=abs(self.x_pos-othercircle.x_pos)
        dy=abs(self.y_pos-othercircle.y_pos)
        if dx<self.radius*2 and dy<self.radius*2:
            pass
        else:
            try:
                r=math.sqrt(dx**2+dy**2)
                a=G*othercircle.mass/r**2
                theta=math.asin(dy/r)

                if self.y_pos>othercircle.y_pos:
                    self.y_acc=(-math.sin(theta)*a)
                else:
                    self.y_acc=math.sin(theta)*a
                
                if self.x_pos>othercircle.x_pos:
                    self.x_acc=(-math.cos(theta)*a)
                else:
                    self.x_acc=math.cos(theta)*a
        
            except ZeroDivisionError:
                pass
    def net_acc(self,list,diag):
        for circle1,circle2 in list:
            if circle1==self:
                dx=abs(self.x_pos-circle2.x_pos)
                dy=abs(self.y_pos-circle2.y_pos)
                
                r=math.sqrt(dx**2+dy**2)
                if r !=0:
                    a=G*circle2.mass/r**2
                    theta=math.asin(dy/r)
                    if self.y_pos>circle2.y_pos:
                        self.net_y_acc+=(-math.sin(theta)*a)
                    else:
                        self.net_y_acc+=math.sin(theta)*a
                    
                    if self.x_pos>circle2.x_pos:
                        self.net_x_acc+=(-math.cos(theta)*a)
                    else:
                        self.net_x_acc+=math.cos(theta)*a
            if circle2==self:
                dx=abs(self.x_pos-circle1.x_pos)
                dy=abs(self.y_pos-circle1.y_pos)
                r=math.sqrt(dx**2+dy**2)
                if r !=0:
                    a=G*circle1.mass/r**2
                    theta=math.asin(dy/r)
                    if self.y_pos>circle1.y_pos:
                        self.net_y_acc+=(-math.sin(theta)*a)
                    else:
                        self.net_y_acc+=math.sin(theta)*a
                    
                    if self.x_pos>circle1.x_pos:
                        self.net_x_acc+=(-math.cos(theta)*a)
                    else:
                        self.net_x_acc+=math.cos(theta)*a
            else:
                pass
        if diag%2==0:
            pg.draw.line(screen,'Blue',self.rect.center,(self.x_pos,self.y_pos+(self.net_y_acc*100)),1)
            pg.draw.line(screen,"Blue",self.rect.center,((self.x_pos+(self.net_x_acc*100),self.y_pos)),1)
        else:
            pg.draw.line(screen,'Blue',self.rect.center,((self.x_pos+(self.net_x_acc*100),self.y_pos+(self.net_y_acc*100))))
    def check_collide(self,tuple,sprite):
        #m1v1+m2v2=(m1+m2)v3 - Conservation of momentum do it for both x and y components
        for circle1,circle2 in tuple:
            if pg.Rect.colliderect(circle1.rect,circle2.rect) and circle1.collided==False and circle2.collided== False:
                new_mass=circle1.mass+circle2.mass
                new_radius=math.cbrt((new_mass*3)/(4*math.pi))
                new_x_pos=(circle1.x_pos+circle2.x_pos)/2
                new_y_pos=(circle1.y_pos+circle2.y_pos)/2
                new_x_vel=((circle1.mass*circle1.x_vel)+(circle2.mass*circle2.x_vel))/new_mass
                new_y_vel=((circle1.mass*circle1.y_vel)+(circle2.mass*circle2.y_vel))/new_mass
                circle1.collided=True
                circle2.collided=True
                sprite.remove(circle1)
                sprite.remove(circle2)
                sprite.add(Circle(new_radius,(new_x_pos,new_y_pos),new_mass,new_x_vel,new_y_vel))
""" 
    SPACE ~ pause
    v ~ show force vector without components
"""
        
def get_mass(radius,density):
    #density*volume=mass
    return density*((4/3)*math.pi*(radius**3))

   
def get_distance(start,end):
    x_vals=end[0]-start[0]
    y_vals=end[1]-start[1]
    idk=(x_vals**2)+(y_vals)**2
    return math.sqrt(idk)


pg.init()
screen=pg.display.set_mode((1000,1000))
pg.display.set_caption("Gravity")
#controlling frame rate
clock=pg.time.Clock()

#state control
mouse_down=False
apply_vel=False
temp_circle=None
pause=0
diag=0

#Big G
G=0.01
#sprite group
body_group=pg.sprite.Group()

while True:
    screen.fill("Black")
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            center=pg.mouse.get_pos()
            for circle in body_list:
                dx=abs(circle.x_pos-center[0])
                dy=abs(circle.y_pos-center[1])
                distance=math.sqrt(dx**2+dy**2)
                if distance<=circle.radius:

                    apply_vel=True
                    temp_circle=circle
            if not apply_vel:
                mouse_down=True
        if event.type==pg.MOUSEBUTTONUP:
            if mouse_down:
                mouse_down=False
                if center!=pg.mouse.get_pos():
                    mass=get_mass(rad,0.5)
                    body_group.add(Circle(rad,center,mass,0,0))
            if apply_vel:
                apply_vel=False
                coords=pg.mouse.get_pos()
                for circle in body_list:
                    if circle.x_pos==temp_circle.x_pos and circle.y_pos==temp_circle.y_pos:
                        circle.x_vel=(coords[0]-circle.x_pos)/10
                        circle.y_vel=(coords[1]-circle.y_pos)/10

        if event.type==pg.MOUSEMOTION:
            if mouse_down:
                screen.fill("Black")
                rad=int(get_distance(center,pg.mouse.get_pos()))
                pg.draw.circle(screen,'White',center,rad)
            if apply_vel:
                pg.draw.line(screen,'Green',(temp_circle.x_pos,temp_circle.y_pos),pg.mouse.get_pos())

        if event.type==pg.KEYDOWN:
            if event.key==pg.K_SPACE:
                pause+=1

        if event.type==pg.KEYDOWN:
            if event.key==pg.K_v:
                diag+=1

    body_list=list(body_group)
    body_pairs=list(itertools.combinations(body_list, 2))
    body_group.draw(screen)
    if pause%2==0:
        if len(body_list)>1:
            for body,otherbody in body_pairs:
                body.gravitate(otherbody)
                otherbody.gravitate(body)
                body.check_collide(body_pairs,body_group)
                #otherbody.check_collide(body_pairs,body_group)
                if not body.drawn:
                    body.net_acc(body_pairs,diag)
                    body.drawn=True
                if not otherbody.drawn:
                    otherbody.net_acc(body_pairs,diag)
                    otherbody.drawn=True
                body.animate()
                otherbody.animate()
            for body in body_list:
                body.drawn=False
                body.net_y_acc=0
                body.net_x_acc=0
        else:
            for circle in body_list:
                circle.animate()
    else:
        for circle in body_list:
            circle.still_draw()
    pg.display.update()
    clock.tick(60)
