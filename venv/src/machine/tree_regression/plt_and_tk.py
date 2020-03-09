#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @author : mythwind 
# contact : 774202013@qq.com
# @datetime : 2020/3/3 9:03 上午 
# @File : plt_and_tk.py
# @desc :

import tkinter
import numpy as np
from utils import file_utils
from tree_regression import  tree_regres
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ReDrawModel :
    def __init__(self,root):
        self.f = Figure(figsize=(5, 4), dpi=100)  # create canvas
        self.canvas = FigureCanvasTkAgg(self.f, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=3)
        self.raw_data = np.mat(file_utils.load_all_dataset('assets/sine.txt'))
        self.test_data = np.arange(np.min(self.raw_data[:, 0]), np.max(self.raw_data[:, 0]), 0.01)


def get_inputs(toln_entry, tols_entry) :
    try :
        toln = int(toln_entry.get())
    except :
        #  清楚错误的输入并使用默认值
        toln = 10
        print("输入toln错误，必须是integer数据")
        toln_entry.delete(0, tkinter.END)
        toln_entry.insert(0, '10')
    try:
        tols = float(tols_entry.get())
    except:
        #  清楚错误的输入并使用默认值
        tols = 10
        print("输入tols错误，必须是float数据")
        tols_entry.delete(0, tkinter.END)
        tols_entry.insert(0, '1.0')
    return toln, tols


def redraw(tols,toln,chk_btn_var,redraw_model) :
    redraw_model.f.clf()
    axs = redraw_model.f.add_subplot(111)
    if chk_btn_var.get() :
        if toln < 2: toln = 2
        mtree = tree_regres.create_tree(redraw_model.raw_data, tree_regres.model_leaf, tree_regres.model_error, (tols, toln))
        yhat = tree_regres.create_forecast(mtree, redraw_model.raw_data, tree_regres.model_tree_eval)
    else :
        mtree = tree_regres.create_tree(redraw_model.raw_data, ops = (tols, toln))
        yhat = tree_regres.create_forecast(mtree, redraw_model.test_data)
    ## .tolist()
    ## axs.scatter(redraw_model.raw_data[:,0], redraw_model.raw_data[:,1], s=5)
    axs.scatter(redraw_model.raw_data[:, 0].tolist(), redraw_model.raw_data[:, 1].tolist(), s=5)
    axs.plot(redraw_model.test_data, yhat, linewidth=2.0)
    redraw_model.canvas.draw()


def draw_new_tree(toln_entry, tols_entry, chk_btn_var, redraw_model) :
    toln, tols = get_inputs(toln_entry, tols_entry)
    redraw(tols, toln, chk_btn_var, redraw_model)


def test_tkinter() :
    root = tkinter.Tk()

    redraw_model = ReDrawModel(root)

    # tkinter.Label(root, text="Plot Place Holder").grid(row=0, columnspan=3)
    tkinter.Label(root, text="tolN").grid(row=1, column=0)
    toln_entry = tkinter.Entry(root)
    toln_entry.grid(row=1, column=1)
    toln_entry.insert(0, '10')
    tkinter.Label(root, text="tolS").grid(row=2, column=0)
    tols_entry = tkinter.Entry(root)
    tols_entry.grid(row=2, column=1)
    tols_entry.insert(0, '1.0')

    chk_btn_var = tkinter.IntVar()
    chk_btn = tkinter.Checkbutton(root, text="Model Tree", variable=chk_btn_var)
    chk_btn.grid(row=3, column=0, columnspan=2)

    tkinter.Button(root, text="ReDraw", command=draw_new_tree(toln_entry, tols_entry, chk_btn_var, redraw_model)).grid(row=1, column=2, columnspan=3)

    redraw(1.0, 10, chk_btn_var, redraw_model)
    root.mainloop()
