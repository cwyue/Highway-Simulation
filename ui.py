import math
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Tkinter import *
import settings

import Queue
import threading
import warnings

from numpy import arange, sin, pi
from time import sleep

import highway
import multilane
import time
import random

class UI (object):
    # UI config
    programTitle = "Traffic Simulation Software Version 1.0"
    animationSize = (8, 8)
    animationDpi = 100
    refreshInterval = 0.3  # refresh frame interval in second
    
    def __init__(self):
        # UI preparation
        warnings.filterwarnings ("ignore")  # ignore warnings
        plt.use ('TKAgg')  # use matplotlib in Tkinter
        self.root = Tk ()
        self.root.resizable (False, False)  # disable window size change
        self.root.title (self.programTitle)  # program title
        
        # set frames
        f1 = Frame(self.root,bd=4,relief='groove')
        f2 = Frame(self.root,bd=4,relief='groove')
        f3 = Frame(self.root,bd=4,relief='groove')
        f4 = Frame(self.root,bd=4,relief='groove')
        f1.grid(row=1,column=0,rowspan=26)
        f2.grid(row=1,column=1,rowspan=8,columnspan=3)
        f3.grid(row=10,column=1,rowspan=12,columnspan=3)
        f4.grid(row=23,column=1,columnspan=3)

        # set views
        Label(self.root,text='Display Window:').grid(row=0,column=0,sticky=W)

        Label(self.root,text='Current Status:').grid(row=0,column=1,sticky=W)

        Label(f2,text='Current Iteration:').grid(row=0,column=0,sticky=W)
        self.curr_iter = Label(f2,text='0/0')
        self.curr_iter.grid(row=1,column=0,sticky=W)

        Label(f2,text='Traffic Light Interval:').grid(row=2,column=0,sticky=W)
        self.traffic_light_interval = Label(f2,text='OFF')
        self.traffic_light_interval.grid(row=3,column=0,sticky=W)
        
        Label(f2,text='Traffic Light Duration:').grid(row=4,column=0,sticky=W)
        self.traffic_light_duration = Label(f2,text='OFF')
        self.traffic_light_duration.grid(row=5,column=0,sticky=W)

        Label(f2,text='Traffic Jam Duration:').grid(row=6,column=0,sticky=W)
        self.traffic_jam_duration = Label(f2,text='OFF')
        self.traffic_jam_duration.grid(row=7,column=0,sticky=W)

        Label(self.root,text='Settings:').grid(row=9,column=1,sticky=W)

        Label(f3,text='Set Iteration:').grid(row=0,column=0,sticky=W)
        self.set_iter = Entry(f3)
        self.set_iter.grid(row=1,column=0,columnspan=3,sticky=N)

        Label(f3,text='Traffic Light Mode:').grid(row=2,column=0,sticky=W)
        self.set_traffic_light_mode = Label(f3,text='ON')
        self.set_traffic_light_mode.grid(row=2,column=0,sticky=E)
        self.set_traffic_light_mode_btn = Button(f3,text='Toggle',command=self.traffic_light_mode_toggle)
        self.set_traffic_light_mode_btn.grid(row=3,column=0,columnspan=3)

        Label(f3,text='Set Traffic Light Interval:').grid(row=4,column=0,sticky=NW)
        self.set_traffic_light_interval = Entry(f3)
        self.set_traffic_light_interval.grid(row=5,column=0,columnspan=3,sticky=N)

        Label(f3,text='Set Traffic Light Duration:').grid(row=6,column=0,sticky=NW)
        self.set_traffic_light_duration = Entry(f3)
        self.set_traffic_light_duration.grid(row=7,column=0,columnspan=3,sticky=N)

        Label(f3,text='Traffic Jam Mode:').grid(row=8,column=0,sticky=NW)
        self.set_traffic_jam_mode = Label(f3,text='ON')
        self.set_traffic_jam_mode.grid(row=8,column=0,sticky=E)
        self.set_traffic_jam_mode_btn = Button(f3,text='Toggle',command=self.traffic_jam_mode_toggle)
        self.set_traffic_jam_mode_btn.grid(row=9,column=0,columnspan=3)

        Label(f3,text='Set Traffic Jam:').grid(row=10,column=0,sticky=NW)
        self.set_traffic_jam_start = Entry(f3,width = 8)
        self.set_traffic_jam_start.grid(row=11,column=0,columnspan=3,sticky=NW)
        Label(f3,text='To').grid(row=11,column=0,columnspan=3,sticky=N)
        self.set_traffic_jam_end = Entry(f3,width = 8)
        self.set_traffic_jam_end.grid(row=11,column=0,columnspan=3,sticky=NE)

        Label(self.root,text='Animation Control:').grid(row=22,column=1,sticky=NW)
        self.play = Button(f4,text='Play',command=self.play)
        self.play.grid(row=0,column=0,sticky=NW)
        # self.pause = Button(f4,text='Pause',state="disabled")
        # self.pause.grid(row=0,column=1,sticky=N)
        self.stop = Button(f4,text='Stop',command=self.stop)
        self.stop.grid(row=0,column=2,sticky=E)

        Label(self.root,text='Error Message:').grid(row=24,column=1,sticky=NW)
        self.message = Label(self.root,text='Normal',fg="black")
        self.message.grid(row=25,column=1,columnspan=3,sticky=N)


        # draw matplotlib output to Tkinter
        self.figure = Figure (figsize=(self.animationSize[0], self.animationSize[1]), dpi=self.animationDpi)  # set figure
        self.canvas = FigureCanvasTkAgg (self.figure, master=f1)  # TODO: subject to change root to frame
        self.canvas.get_tk_widget ().grid (row=1, column=0, rowspan=26)  # TODO: subject to change canvas position
        
        # set window in the center of the screen
        # ===== quote http://www.jb51.net/article/61962.htm =====
        self.root.update ()  # update window (must do)
        curWidth = self.root.winfo_reqwidth ()  # get current width
        curHeight = self.root.winfo_height ()  # get current height
        scnWidth, scnHeight = self.root.maxsize ()  # get screen width and height
        # now generate configuration information
        tmpcnf = '%dx%d+%d+%d' % (curWidth, curHeight, (scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
        self.root.geometry (tmpcnf)
        # ===== end quote =====
        
        # set message queue
        self.messageQueue = Queue.Queue ()
        self.masterMessageQueue = Queue.Queue()
        

    def drawFrame(self, x, y, num):
        self.figure.clf()
        colors = ['red', 'orange', 'yellow', "green", "blue", 'purple', 'pink', "black"]
        for i in range(num):
            ax = self.figure.add_subplot (111)
            ax.scatter (x[i], y[i], s=8, color=colors[i])
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
        if self.set_traffic_jam_mode.cget("text") == "ON":
            self.figure.add_subplot (111).scatter ([1215, 1250],[1725, 1762], s=40, color="black", marker="x")
            self.figure.legend(["Lane 0","Lane 1","Lane 2","Lane 3","Lane 4","Merge 0","Merge 1","Exit", "Accident"], loc="lower left", bbox_to_anchor=(0.05,0.05))
        else:
            self.figure.legend(["Lane 0","Lane 1","Lane 2","Lane 3","Lane 4","Merge 0","Merge 1","Exit"], loc="lower left", bbox_to_anchor=(0.08,0.08))
        
        fig = self.figure.gca()
        # ax.spines['right'].set_visible(False)
        fig.set_ylim ([-200, 3500])
        fig.set_xlim ([-300, 3000])
        fig.xaxis.set_visible(False)
        fig.yaxis.set_visible(False)
        self.figure.tight_layout(pad=0)

        self.canvas.show ()

    def processMessage(self):
        while True:
            if not self.messageQueue.empty ():
                x, y, i = self.messageQueue.get ()
                num = len(x)
                self.drawFrame (x, y, num)
                self.curr_iter.config(text=str(i+1) + "/" + self.curr_iter.cget("text").split("/")[1])
                if self.curr_iter.cget("text").split("/")[0] == self.curr_iter.cget("text").split("/")[1]:
                    self.masterMessageQueue.put(1)
                    self.play.config(state="normal")
            if not self.masterMessageQueue.empty():
                self.messageQueue = Queue.Queue()
                self.figure.clf()
            sleep(self.refreshInterval)

    def sendMessage(self, x, y, i):
        # x, y = self.processData (highways)
        self.messageQueue.put ((x, y, i))

    def mainloop(self):
        self.root.mainloop ()

    def traffic_light_mode_toggle(self):
        if self.set_traffic_light_mode.cget("text") == "ON":
            self.set_traffic_light_mode.config(text="OFF")
            self.set_traffic_light_duration.config(state=DISABLED)
            self.set_traffic_light_interval.config(state=DISABLED)
        else:
             self.set_traffic_light_mode.config(text="ON")
             self.set_traffic_light_duration.config(state=NORMAL)
             self.set_traffic_light_interval.config(state=NORMAL)

    def traffic_jam_mode_toggle(self):
        if self.set_traffic_jam_mode.cget("text") == "ON":
            self.set_traffic_jam_mode.config(text="OFF")
            self.set_traffic_jam_start.config(state=DISABLED)
            self.set_traffic_jam_end.config(state=DISABLED)
        else:
             self.set_traffic_jam_mode.config(text="ON")
             self.set_traffic_jam_start.config(state=NORMAL)
             self.set_traffic_jam_end.config(state=NORMAL)

    def play(self):
        try:
            iteration = int(self.set_iter.get())
        except:
            self.message.config(text="Invalid iteration value.",fg="red")
            return
        if iteration <= 0:
            self.message.config(text="Invalid iteration value.",fg="red")
            return

        if self.set_traffic_light_mode.cget("text") == "OFF":
            interval = -1
            duration = -1
        else:
            try:
                interval = int(self.set_traffic_light_interval.get())
            except:
                self.message.config(text="Invalid interval value.",fg="red")
                return
            if interval <= 0:
                self.message.config(text="Invalid interval value.",fg="red")
                return

            try:
                duration = int(self.set_traffic_light_duration.get())
            except:
                self.message.config(text="Invalid duration value.",fg="red")
                return
            if duration <= 0:
                self.message.config(text="Invalid duration value.",fg="red")
                return

        if self.set_traffic_jam_mode.cget("text") == "OFF":
            jam_start = -1
            jam_end = -1
        else:
            try:
                jam_start = int(self.set_traffic_jam_start.get())
            except:
                self.message.config(text="Invalid start value.",fg="red")
                return
            if jam_start <= 0:
                self.message.config(text="Invalid start value.",fg="red")
                return

            try:
                jam_end = int(self.set_traffic_jam_end.get())
            except:
                self.message.config(text="Invalid end value.",fg="red")
                return
            if jam_end <= 0 or jam_end <= jam_start:
                self.message.config(text="Invalid end value.",fg="red")
                return

        # config
        self.message.config(text="Normal",fg="black")
        self.masterMessageQueue = Queue.Queue()
        self.messageQueue = Queue.Queue()
        self.curr_iter.config(text="0/"+str(iteration))
        self.play.config(state="disabled")

        if jam_start == -1:
            self.traffic_jam_duration.config(text="OFF")
        else:
            self.traffic_jam_duration.config(text=self.set_traffic_jam_start.get()+" to "+self.set_traffic_jam_end.get())

        if interval == -1:
            self.traffic_light_interval.config(text="OFF")
            self.traffic_light_duration.config(text="OFF")
        else:
            self.traffic_light_interval.config(text=str(interval))
            self.traffic_light_duration.config(text=str(duration))

        workerThread = threading.Thread(target=self.run, args=(iteration, interval, duration, jam_start, jam_end))
        workerThread.setDaemon(True)
        workerThread.start()

    def stop(self):
        self.masterMessageQueue.put(1)
        self.play.config(state="normal")

    def run(self, iteration_num, interval, duration, jam_start, jam_end):
        iteration = iteration_num
        acc_start = jam_start
        acc_stop = jam_end
        hwy = highway.Highway ()
        basemap = settings.UI_BASEMAP
        accident = "ON"                 # toggle between ON and OFF
        traffic_light = "ON"            # toggle between ON and OFF

        if interval == -1:
            traffic_light = "OFF"
        if jam_start == -1:
            accident = "OFF"

        traff_intv = interval
        traff_dura = duration
        for itr in range (iteration):

            if accident == "ON":
                # Interface for calling traffic accidents: hwy.update_states(itr, flag)
                # flag = 1: traffic accident; flag = 0: no accident
                if itr > acc_start or itr < acc_stop:
                    hwy.update_states(itr, 0.3, 1)
                else:
                    hwy.update_states(itr, 0.3, 0)
            
            if traffic_light == "ON":
                if itr % (traff_intv + traff_dura) == 0:
                    hwy.mergelane.e_prob1 = 0
                elif itr % (traff_intv + traff_dura) == traff_intv:
                    hwy.mergelane.e_prob1 = 0.7
                if itr == iteration - 1:
                    hwy.mergelane.e_prob1 = 0.5
            
            if accident == "OFF":
                hwy.update_states (itr, 0.3, 0)
            
            res1 = hwy.multiway.lanes
            res2 = hwy.mergelane.lanes
            res3 = hwy.exitway.lanes
            
            res = [[] for _ in range (8)]
            res[:5] = res1
            res[5:7] = res2
            res[7] = res3
            
            x = [[] for _ in range (8)]
            y = [[] for _ in range (8)]
            for i, lanex in enumerate (res):
                for j, c in enumerate (lanex.cells):
                    if c != None:
                        id = c.id
                        xi, yi = basemap[i][j]
                        x[id].append (xi)
                        y[id].append (yi)
            
            
            if itr % 30 == 0 or itr % 30 == 1 or itr % 30 == 2:
                print "\n----------------- The %dth Run: -----------------" % (itr)
                for i, lane in enumerate (res):
                    count = 0
                    v_sum = 0
                    for j, c in enumerate (lane.cells):
                        if c != None:
                            count += 1
                            v_sum += c.speed
                    print "Num of vehicles on Lane %d is %d" % (i, count)
                    print "Average speed of vehicles on Lane %d is %f" % (i, float(10*v_sum)/count)
                    
                    count_enter = 0
                    v_sum_enter = 0
                    count_exit = 0
                    v_sum_exit= 0
                    
                    if i in range(5):
                        a, b, c = 100, 151, 50
                    else:
                        a, b, c = 30, 51, 0
                    d = b - a - 1
                    
                    for j in range(a, b):
                        if lane.cells[j] != None:
                            count_enter += 1
                            v_sum_enter += lane.cells[j].speed
                        if lane.cells[c-j] != None:
                            count_exit += 1
                            v_sum_exit += lane.cells[c-j].speed
                    
                    print "Sparsity(at entrance): %f" % (float(count_enter)/d)
                    print "Sparsity(at exit): %f" % (float(count_exit)/d)
                    
                    if count_enter == 0:
                        print "No Entrance"
                    else:
                        print "Enter Speed (at entrance): %f" % (float(v_sum_enter)/count_enter)
            
                    if count_exit == 0:
                        print "No Exit"
                    else:
                        print "Exit Speed (at exit): %f" % (float (v_sum_exit)/count_exit)
                    
                    print
                    
            # send data to UI
            self.sendMessage (x, y, itr)
            if not self.masterMessageQueue.empty():
                return
