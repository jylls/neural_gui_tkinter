from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import font
import numpy as np
import scipy.io as sio
from spike_matrix import spike_matrix
from cov_matrix import cov_matrix
from z_scoring import z_scoring
import os.path
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from load_triggers import load_triggers
from load_spike_times import load_spike_times
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import pyglet
pyglet.font.add_file('basquiat_reg.otf')
import matplotlib.pyplot as plt

def menu_tkinter():

    def donothing():
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()



    def browseFilesNeural():
        filename = filedialog.askopenfilename(initialdir = "./",
                                              title = "Select a neural data file",
                                              filetypes = (("Numpy files",
                                                            "*.npy*"),
                                                           ("Matlab files",

                                                            "*.mat*")))
        # Change label contents
        label_file_explorer.configure(text="File Opened: "+filename)
        if os.path.isfile('./neural_data_path.npy'):
            os.remove('neural_data_path.npy')
        print(filename)
        np.save('neural_data_path.npy', filename)


    def browseFilesTrigger():
        filename = filedialog.askopenfilename(initialdir = "./",
                                              title = "Select a trigger file",
                                              filetypes = (("Numpy files",
                                                            "*.npy*"),
                                                           ("Matlab files",
                                                            "*.mat*")))

        if os.path.isfile('./trigger_path.npy'):
            os.remove('trigger_path.npy')

        np.save('trigger_path.npy', filename)


    def openNewWindow():
        menu_tkinter()


    root = Tk()

    #root.option_add('*Font', 'Basquiat')
    #f = font.nametofont('TkDefaultFont')

    root.geometry("500x500")

    label_file_explorer = Label(root,
                            text = "File Explorer using Tkinter",
                            width = 100, height = 4,
                            fg = "blue")

    def bin_data(c):
        tw=take_user_input_for_something()
        #my_entry = Entry(root)
        #my_entry.pack()
        if not os.path.isfile('./neural_data_path.npy'):
            print('Please open a neural data file first')
        elif not os.path.isfile('./trigger_path.npy'):
            print('Please open a trigger file first')

        else:
            dmr=1
            time_window=tw*0.001
            neural_data_path=np.load('./neural_data_path.npy',allow_pickle=True)
            neural_data_path=str(neural_data_path)
            print('path:::'+neural_data_path)
            #if neural_data_path[-4:]=='.npy':
                #   neural_data=np.load(neural_data_path,allow_pickle=True)
            spike_times,file_spikes=load_spike_times(neural_data_path)
            #elif neural_data_path[-4:]=='.mat':
            #neural_data=sio.loadmat(neural_data_path)

            trigger_path=np.load('./trigger_path.npy',allow_pickle=True)
            trigger_path=str(trigger_path)


            trig,file_trig=load_triggers(trigger_path,dmr)
            spt_mat=spike_matrix(spike_times,trig,time_window,cluster_list=None,dmr=1,shuffled=False)
            #fig = Figure(figsize = (5, 5),dpi = 100)
            c=comb[1]
            fig=comb[0]
            plot1= fig.add_subplot(111)
            plt.title('Density plot (time window='+str(tw)+' ms')
            plot1.clear()
            plot1.imshow(spt_mat,origin='lower left',aspect='auto',interpolation=None,cmap='cividis')
            #canvas = FigureCanvasTkAgg(fig,master = root,tag={'cvs'})
            c.draw()
            # placing the canvas on the Tkinter window
            c.get_tk_widget().pack()
            #canvas.delete('all')
            np.save('spike_matrix.npy',spt_mat)

    def zscored_matrix(comb):
        if not os.path.isfile('./spike_matrix.npy'):
            bin_data()

        spt_mat=np.load('spike_matrix.npy',allow_pickle=True)
        z_scored_mat=z_scoring(spt_mat)
        #fig = Figure(figsize = (5, 5),dpi = 100)
        c=comb[1]
        fig=comb[0]
        #canvas.delete("all")
        plot1= fig.add_subplot(111)
        plot1.clear()
        plot1.imshow(z_scored_mat,origin='lower left',aspect='auto',interpolation=None,cmap='cividis')
        #canvas = FigureCanvasTkAgg(fig,master = root)
        c.draw()
        # placing the canvas on the Tkinter window
        c.get_tk_widget().pack()
        np.save('z_scored_matrix.npy',z_scored_mat)


    def correlation_matrix(comb):
        if not os.path.isfile('./z_scored_matrix.npy'):
            zscored_matrix()
        z_scored_mat=np.load('./z_scored_matrix.npy',allow_pickle=True)
        cov_mat=cov_matrix(z_scored_mat)
        #fig = Figure(figsize = (5, 5),dpi = 100)
        c=comb[1]
        fig=comb[0]
        plot1= fig.add_subplot(111)
        plot1.clear()
        plot1.imshow(cov_mat,origin='lower left',aspect='auto',interpolation=None,cmap='cividis')
        #canvas = FigureCanvasTkAgg(fig,master = root)
        c.draw()
        # placing the canvas on the Tkinter window
        c.get_tk_widget().pack()
        np.save('correlation_matrix.npy',cov_mat)

    def pca_assembly(comb):
        if not os.path.isfile('./z_scored_matrix.npy'):
            zscored_matrix()
        z_scored_mat=np.load('./z_scored_matrix.npy',allow_pickle=True)
        dmr=1
        sig_eig_vec,bel_lam_min_vec,expl_var=assembly_detection(dmr,z_scored_mat)



    def take_user_input_for_something():
        user_input = simpledialog.askstring("Pop up for user input!", "What time window do you want for the binning (in ms)?")
        if user_input != "":
            user_input_int=int(user_input)
            return user_input_int




    menubar = Menu(root)
    fig = Figure(figsize = (5, 5),dpi = 100)
    c = FigureCanvasTkAgg(fig,master = root)
    comb=[fig,c]
    comb_bin=[fig,c,root]
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New window", command=openNewWindow)
    filemenu.add_command(label="Open neural data ('.npy' or '.mat')", command=browseFilesNeural)
    filemenu.add_command(label="Open trigger file ('.mat')", command=browseFilesTrigger)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Save as...", command=donothing)
    filemenu.add_command(label="Close", command=donothing)

    filemenu.add_separator()

    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)

    editmenu.add_separator()

    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)

    menubar.add_cascade(label="Edit", menu=editmenu)

    toolmenu = Menu(menubar, tearoff=0)
    toolmenu.add_command(label="Spike train matrix", command= lambda : bin_data(comb))
    toolmenu.add_command(label="z-normed spike matrix", command= lambda : zscored_matrix(comb))
    toolmenu.add_command(label="Correlation matrix", command= lambda: correlation_matrix(comb))
    #toolmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Tools", menu=toolmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)
    #c.draw()
    #c.get_tk_widget().pack()

    root.config(menu=menubar)#,bg='snow2')
    root.mainloop()



if __name__ == '__main__':
    menu_tkinter()
