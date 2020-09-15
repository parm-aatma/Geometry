import numpy as np
import cv2 as cv
import math

########################################################################################################################
degree_symbol="\xb0"
class Line:
    def __init__(self,pt1,pt2,board,color=(0,0,0)):
        self.pt1=tuple(pt1)
        self.pt2=tuple(pt2)
        self.board=board
        self.img=board
        self.boards=[]
        self.color=color
        self.midpoint=(int((pt1[0]+pt2[0])/2),int((pt1[1]+pt2[1])/2))
        self.points_to_show = {"point1":self.pt1,"point2":self.pt2,"midpoint":self.midpoint}
        if pt2[0]-pt1[0]==0:
            self.slope=float('inf')
        else:
            self.slope=math.atan((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))*180/math.pi
        self.points=[]
        self.length= np.round(math.sqrt(math.pow(self.pt1[1]-self.pt2[1],2)+math.pow(self.pt1[0]-self.pt2[0],2)),2)
        self.equation=[]

    def __getitem__(self, item):
        if item==0:
            return self.equation
        elif item==1:
            return self.pt1
        elif item==2:
            return self.pt2
        elif item==3:
            return self.slope
        elif item==4:
            return self.length

    def getSlope(self,pt1,pt2):
        return math.atan((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))*180/math.pi

    def draw(self,onSame=False):
        if not onSame:
            self.boards.append(self.img)
            self.img=self.board
        cv.line(self.img, self.pt1, self.pt2, self.color, 2)
        for pt in self.points_to_show:
            cv.putText(self.img,f"{self.points_to_show[pt]}",self.points_to_show[pt],cv.FONT_HERSHEY_SIMPLEX,0.25,(0,0,0),1)

    def display(self):
        cv.imshow("Board", self.img)
        cv.waitKey(0)

    def reset_board(self):
        self.img = self.board

    def get_board(self):
        return self.img

    def onLine(self,query):
        if np.round(self.getSlope(self.pt1,query),2)==np.round(self.getSlope(query,self.pt2),2):
            return True
        return False

    def getLine(self):
        return [self.getEquation(rtrn=True),self.pt1,self.pt2,self.slope,self.length]

    def getEquation(self,display=False,rtrn=False):
        m=np.round((self.pt2[1]-self.pt1[1])/(self.pt2[0]-self.pt1[0]),2)
        c=np.round(self.pt1[1]-m*self.pt1[0],2)
        self.equation=[m,c]
        if display:
            if abs(m)!=1.0:
                print(f"y=({m}x)+{c}")
            elif m==-1.0:
                print(f"y=(-x)+{c}")
            else:
                print(f"y=(x)+{c}")
        if rtrn:
            return self.equation
########################################################################################################################

class Lines:
    def __init__(self,lines,board):
        if len(lines)<=1:
            raise ValueError("The module expects at least two lines")
        self.lines=lines
        self.intersectionPoints=[]
        self.board=board
        self.angle=[]

    def __getitem__(self, item):
        return self.lines[item]

    def getIntersection(self):
        for i in range(len(self.lines)-1):
            m1=self.lines[i][0][0]
            c1=self.lines[i][0][1]
            for j in range(i+1,len(self.lines)):
                m2 = self.lines[j][0][0]
                c2 = self.lines[j][0][1]
                if m1==m2:
                    continue
                x=np.round((c2-c1)/(m1-m2),2)
                y=np.round((m1*c2-c1*m2)/(m1-m2))
                cv.circle(self.board, (int(x),int(y)), 4, (0, 0, 0), -1)
                self.intersectionPoints.append((x,y,(i,j)))

    def display(self):
        cv.imshow("Lines",board)
        cv.waitKey(0)

    def getAngles(self):
        for i in range(len(self.lines)-1):
            m1=self.lines[i][0][0]
            for j in range(i+1,len(self.lines)):
                m2 = self.lines[j][0][0]
                self.angle.append((np.round(math.atan(m1-m2)*180/math.pi,2),(i,j)))

########################################################################################################################
board=np.ones((600,600,3))

line1=Line([100,100],[200,200],board,(255,0,0))
line1.draw()
board=line1.get_board()
line2=Line([100,100],[50,200],board,(0,0,255))
line2.draw()
board=line2.get_board()
line3=Line([200,200],[50,200],board,(0,255,0))
line3.draw()
board=line3.get_board()
lines=Lines([line1.getLine(),line2.getLine(),line3.getLine()],board)
lines.getIntersection()
lines.display()
lines.getAngles()
print(lines.intersectionPoints)
print(lines.angle)