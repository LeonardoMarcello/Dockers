#!/usr/bin/env python3

import time
import tkinter
import rospy
from std_msgs.msg import *
from papillarray_ros_v2.msg import SensorState
from papillarray_ros_v2.srv import BiasRequest
import matplotlib.pyplot as plt
import numpy
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

class interface:
    def __init__(self):
        # --- ROS PARAMETERS & DYNAMIC TOPICS ---
        # Get parameters passed from Docker/Launch file
        self.sensor_name = rospy.get_param('~sensor_name', 'Hub 0 - Sensor 0')
        # Scaling factor for High DPI screens (1.0 is default, try 1.5 or 2.0)
        self.gui_scaling = rospy.get_param('~gui_scaling', 1.0)
        
        # Use relative names to allow remapping
        self.topic_name = 'hub_0/sensor_0'
        self.service_name = 'hub_0/send_bias_request'

        ## Listener
        self.sub = rospy.Subscriber(self.topic_name, SensorState, self.callback)

        ## Reset previous bias (Service Proxy)
        try:
            rospy.wait_for_service(self.service_name, timeout=2.0)
            self.bias_srv = rospy.ServiceProxy(self.service_name, BiasRequest)
            self.bias_srv()
        except rospy.ROSException:
            rospy.logwarn("Bias service not available yet.")

        ## Variables
        self.msgZ = [0]*9
        self.msgY = [0]*9
        self.msgX = [0]*9
        self.msgGF = [0,0,0]
        self.dec = 65
        self.size = "1500x1000"
        self.width = 20
        self.buffer_size = 130
        self.timelist = numpy.linspace(-5, 0, self.buffer_size)
        
        self.graphX = [[0 for s in range(self.buffer_size)] for p in range (9)]
        self.graphY = [[0 for s in range(self.buffer_size)] for p in range (9)]
        self.graphZ = [[0 for s in range(self.buffer_size)] for p in range (9)]
        self.graphGX, self.graphGY, self.graphGZ = [0]*self.buffer_size, [0]*self.buffer_size, [0]*self.buffer_size

        self.arrowcoordX = [125, 125, 125, 190, 190, 190, 255, 255, 255]
        self.arrowcoordY = [215, 150, 85, 215, 150, 85, 215, 150, 85]

        ## Making the main window
        self.window = tkinter.Tk()
        # FIX: Scaling for Docker/High DPI
        self.window.tk.call('tk', 'scaling', self.gui_scaling)
        
        self.window.title(self.sensor_name)
        self.window.geometry(self.size)
        
        # FIX: Allow the grid to resize
        for i in range(5): self.window.grid_columnconfigure(i, weight=1)
        for i in range(18): self.window.grid_rowconfigure(i, weight=1)

        ## UI Elements
        self.canvas0 = tkinter.Canvas(self.window)
        label0 = tkinter.Label(self.window, text=self.sensor_name, font=("Arial Bold", 20))
        label0.grid(column=1, row=0, sticky="nsew")

        self.reset_text = tkinter.Label(self.window, text="")
        self.reset_text.grid(column=4, row=1)

        self.canvas0.create_rectangle(90,50,290,250, outline="grey", fill="light grey", width=2)
        self.circle_list = []
        for j in range(3):
            for i in range(3):
                self.circle_list.append(self.canvas0.create_oval(100+i*self.dec,60+j*self.dec,150+i*self.dec,110+j*self.dec, outline="black",fill="pink", width=2))
        
        self.canvas0.grid(column=1, row=1, sticky="nsew")

        ## Legend
        self.canvasT = tkinter.Canvas(self.window)
        self.canvasT.create_rectangle(50, 65, 200, 215, fill = 'white')
        self.canvasT.create_text(150, 100, text = 'X force', font = ('Arial', 10))
        self.canvasT.create_text(150, 140, text = 'Y force', font = ('Arial', 10))
        self.canvasT.create_text(150, 180, text = 'Z force', font = ('Arial', 10))
        self.canvasT.create_line(70, 100, 110, 100, fill = 'red', width = 2)
        self.canvasT.create_line(70, 140, 110, 140, fill = 'green', width = 2)
        self.canvasT.create_line(70, 180, 110, 180, fill = 'blue', width = 2)
        self.canvasT.grid(column=0, row=1, sticky="nsew")

        ## Pillars & Display setup (Truncated for brevity, logic remains same)
        self.pillars = [tkinter.Label(self.window, text=f'Pillar {i}', font=("Arial", 12)) for i in range(9)]
        self.displayX = [tkinter.Label(self.window, text="0.0", font=("Arial", 10)) for i in range(9)]
        self.displayY = [tkinter.Label(self.window, text="0.0", font=("Arial", 10)) for i in range(9)]
        self.displayZ = [tkinter.Label(self.window, text="0.0", font=("Arial", 10)) for i in range(9)]
        
        k = 0
        for j in range(3):
            for i in range(3):
                self.pillars[k].grid(column=j, row=12-5*i, sticky="nsew")
                k += 1

        self.GFlabel = tkinter.Label(self.window, text='Global Forces', font=("Arial", 14))
        self.GFlabel.grid(column=4, row=7, sticky="nsew")
        self.displayGF = [tkinter.Label(self.window, text="0.0", font=("Arial", 12)) for i in range(3)]

        ## Matplotlib graphs
        self.plots = []
        self.lines = []
        self.canvasG = []

        x = 0
        for j in range(3):
            for i in range (3):
                # FIX: Set background color and tight layout
                fig, ax = plt.subplots(figsize=(2, 2), dpi=100)
                fig.set_facecolor('#f0f0f0') 
                lineX, = ax.plot(self.timelist, self.graphX[x], color='red')
                lineY, = ax.plot(self.timelist, self.graphY[x], color='green')
                lineZ, = ax.plot(self.timelist, self.graphZ[x], color='blue')
                self.lines.extend([lineX, lineY, lineZ])
                
                ax.set_ylim(-1, 10)
                ax.tick_params(labelsize=7)
                
                canvas = FigureCanvasTkAgg(fig, master=self.window)
                canvas.get_tk_widget().grid(column=j, row=13-5*i, sticky="nsew")
                self.canvasG.append(canvas)
                x += 1

        # Global Force Graph
        self.figGF, self.axGF = plt.subplots(figsize=(2, 2), dpi=100)
        self.lineGFX, = self.axGF.plot(self.timelist, self.graphGX, color='red')
        self.lineGFY, = self.axGF.plot(self.timelist, self.graphGY, color='green')
        self.lineGFZ, = self.axGF.plot(self.timelist, self.graphGZ, color='blue')
        self.axGF.set_ylim(-5, 20)
        self.canvasGF = FigureCanvasTkAgg(self.figGF, master=self.window)
        self.canvasGF.get_tk_widget().grid(column=4, row=8, sticky="nsew")

        # Arrows & Buttons
        self.arrowX, self.arrowY = [None]*18, [None]*18
        self.fillcolor = [None]*9
        for l in range(9):
            self.arrowX[l] = self.canvas0.create_line(self.arrowcoordX[l], self.arrowcoordY[l], self.arrowcoordX[l], self.arrowcoordY[l]+20, arrow=tkinter.LAST)
            self.arrowY[l] = self.canvas0.create_line(self.arrowcoordX[l], self.arrowcoordY[l], self.arrowcoordX[l]-20, self.arrowcoordY[l], arrow=tkinter.LAST)
            self.arrowX[l+9] = self.canvas0.create_line(self.arrowcoordX[l], self.arrowcoordY[l], self.arrowcoordX[l], self.arrowcoordY[l]-20, arrow=tkinter.LAST)
            self.arrowY[l+9] = self.canvas0.create_line(self.arrowcoordX[l], self.arrowcoordY[l], self.arrowcoordX[l]+20, self.arrowcoordY[l], arrow=tkinter.LAST)

        self.reset_button = tkinter.Button(self.window, text="Request Bias", command=self.button_press)
        self.reset_button.grid(column=4, row=0, sticky="nsew")
        self.close_button = tkinter.Button(self.window, text="Close", bg="red", fg="yellow", command=self.close_interface)
        self.close_button.grid(column=4, row=2, sticky="nsew")

        self.update()

    def callback(self, data):
        self.msgX = [round(data.pillars[i].fX, 4) for i in range(9)]
        self.msgY = [round(data.pillars[i].fY, 4) for i in range(9)]
        self.msgZ = [round(data.pillars[i].fZ, 4) for i in range(9)]
        self.msgGF = [round(data.gfX, 4), round(data.gfY, 4), round(data.gfZ, 4)]

    def button_press(self):
        self.reset_text.config(text="Calibrating...")
        try: self.bias_srv()
        except: rospy.logerr("Bias Service Call Failed")
        self.window.after(1000, lambda: self.reset_text.config(text=""))

    def update(self):
        # Update Pillar Graphs
        for k in range(9):
            # Shift buffer
            self.graphX[k] = self.graphX[k][1:] + [self.msgX[k]]
            self.graphY[k] = self.graphY[k][1:] + [self.msgY[k]]
            self.graphZ[k] = self.graphZ[k][1:] + [self.msgZ[k]]
            # Update lines
            self.lines[3*k].set_ydata(self.graphX[k])
            self.lines[3*k+1].set_ydata(self.graphY[k])
            self.lines[3*k+2].set_ydata(self.graphZ[k])
            self.canvasG[k].draw_idle() # draw_idle is more efficient than draw()

        # Update Global Graph
        self.graphGX = self.graphGX[1:] + [self.msgGF[0]]
        self.graphGY = self.graphGY[1:] + [self.msgGF[1]]
        self.graphGZ = self.graphGZ[1:] + [self.msgGF[2]]
        self.lineGFX.set_ydata(self.graphGX)
        self.lineGFY.set_ydata(self.graphGY)
        self.lineGFZ.set_ydata(self.graphGZ)
        self.canvasGF.draw_idle()

        self.change_color()
        self.add_arrow()
        self.window.after(30, self.update) # ~30FPS is enough for GUI

    def change_color(self):
        # Map pillar index to the circle_list index based on your grid layout
        # This ensures the correct circle turns red when you press a pillar
        mapping = {0:6, 1:3, 2:0, 3:7, 4:4, 5:1, 6:8, 7:5, 8:2}
        
        for l in range(len(self.msgZ)):
            k = mapping.get(l)
            force = self.msgZ[l]
            
            if force < -0.1:
                color = 'grey'
            elif force < 0.1:
                color = '#fcc3d5' # Light Pink (Default)
            elif force < 0.5:
                color = '#f592b5'
            elif force < 1.0:
                color = '#f3719e'
            elif force < 2.0:
                color = '#f05088'
            elif force < 4.0:
                color = '#e7125c'
            elif force < 7.0:
                color = '#840a34'
            else:
                color = '#42051a' # Dark Red (High Force)
            
            self.canvas0.itemconfig(self.circle_list[k], fill=color)
            self.fillcolor[l] = color

    def add_arrow(self):
        for l in range(9):
            # Check if arrows exist and fillcolor is set
            if self.arrowX[l] is None or self.fillcolor[l] is None:
                continue
                
            # X-axis arrows (Threshold 0.3)
            if self.msgX[l] > 0.3:
                self.canvas0.itemconfig(self.arrowX[l], fill='black')
                self.canvas0.itemconfig(self.arrowX[l+9], fill=self.fillcolor[l])
            elif self.msgX[l] < -0.3:
                self.canvas0.itemconfig(self.arrowX[l+9], fill='black')
                self.canvas0.itemconfig(self.arrowX[l], fill=self.fillcolor[l])
            else:
                self.canvas0.itemconfig(self.arrowX[l], fill=self.fillcolor[l])
                self.canvas0.itemconfig(self.arrowX[l+9], fill=self.fillcolor[l])

            # Y-axis arrows (Threshold 0.3)
            if self.msgY[l] > 0.3:
                self.canvas0.itemconfig(self.arrowY[l], fill='black')
                self.canvas0.itemconfig(self.arrowY[l+9], fill=self.fillcolor[l])
            elif self.msgY[l] < -0.3:
                self.canvas0.itemconfig(self.arrowY[l+9], fill='black')
                self.canvas0.itemconfig(self.arrowY[l], fill=self.fillcolor[l])
            else:
                self.canvas0.itemconfig(self.arrowY[l], fill=self.fillcolor[l])
                self.canvas0.itemconfig(self.arrowY[l+9], fill=self.fillcolor[l])

    def close_interface(self):
        plt.close('all')
        self.window.destroy()

if __name__ == '__main__':
    rospy.init_node('sensor_display', anonymous=True)
    sensor = interface()
    sensor.window.mainloop()