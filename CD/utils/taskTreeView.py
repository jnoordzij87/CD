from tkinter import *
from tkinter import ttk
import tkinter as tk
from ttkwidgets import CheckboxTreeview
from utils.paths import *
from datetime import datetime
import os
from utils.updater import *
import json


class TaskTreeView:

    def __init__(self, parent):
        self.CreateWindow(parent)
        
    
    def CreateWindow(self, parent):
        self.root = parent
        self.root.title("Tasks")
        
        self.rowcounter = 0

        #create the content frame
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        #create the treeview
        self.tree = CheckboxTreeview(self.mainframe)
        self.tree.grid(column=0, row=self.rowcounter, sticky=W)
        self.rowcounter+=1

        #fill the tree
        self.FillTree(self.tree)

        #create labels and entries for sources
        self.CreateSourceEntries()
        
        #create quit button
        quitbutton = ttk.Button(self.mainframe, text="Quit", command=self.Quit)
        quitbutton.grid(row=self.rowcounter, sticky=W)
        self.rowcounter+=1
        
        #create print button
        printbutton = ttk.Button(self.mainframe, text="Print", command=self.Print)
        printbutton.grid(row=self.rowcounter, sticky=W)
        self.rowcounter+=1
        
        #create continue button
        continuebutton = ttk.Button(self.mainframe, text="StartCopy", command=self.StartCopy)
        continuebutton.grid(row=self.rowcounter, sticky=W)
        self.rowcounter+=1

    def StartCopy(self):
        tasks = self.get_checked(self.tree)
        sourcePaths = self.GetSourceEntryValues()

        #save the sources for quick reruns
        self.SaveSources(sourcePaths)

        updater = Updater() 
        updater.Update(tasks, sourcePaths)
       
    def SaveSources(self, sourcePaths):
        with open('sourceconfig.txt', 'w') as outfile:
            json.dump(sourcePaths, outfile)

    def GetSourceEntryValues(self):
        """
        Returns sourcedirectories indexed by program
        """
        sourcePaths = {}
        for program,sourceEntry in self.SourceEntryLookup.items():
            #extract value from entry
            sourcePath = str(sourceEntry.Text.get())
            sourcePaths[str(program)] = sourcePath
        return sourcePaths

    def CreateSourceEntries(self):
        #start a lookup
        self.SourceEntryLookup = {}
        #read sourceconfig for fast loading of sources
        sources = self.ReadSourceConfig()
        #build entries for programs
        for program in Programs:
            #build label
            label = ttk.Label(self.mainframe, text = str(program.name) + " source dir")
            label.grid(row=self.rowcounter, sticky=W)
            #build entry
            entry = CustomEntry(self.mainframe)
            entry.grid(row=self.rowcounter+1, sticky = (W,E))
            #set entry value from sourceconfig
            storedvalue = sources[str(program)]
            entry.Text.set(storedvalue)
            #add entry to lookup
            self.SourceEntryLookup[program] = entry
            self.rowcounter+=2
    
    def ReadSourceConfig(self):
        with open('sourceconfig.txt') as json_file:
            sources = json.load(json_file)
            return sources

    def FillTree(self, tree):
        tree.insert("", "end", "1", text="Client")
        for env in Environments:
            tree.insert("1", "end", "1."+str(env.value), text=str(env.name))
        tree.insert("", "end", "2", text="WebService")
        for env in Environments:
            tree.insert("2", "end", "2."+str(env.value), text=str(env.name))
        
    def get_checked(self, tree):
        checked = []
        def rec_get_checked(item):
            if tree.tag_has('checked', item):
                checked.append(item)
            for ch in tree.get_children(item):
                rec_get_checked(ch)
        rec_get_checked('')
        return checked

    def Print(self):
        checkeditems = self.get_checked(self.tree)
        print(checkeditems)
    
    def Quit(self):
        print('quit')
        self.root.quit()
        self.root.destroy()
        
class CustomEntry(ttk.Entry):
    """
    a dynamically creatable entry for which the value can be obtained
    without a hardcoded variable bound to it
    """
    def __init__(self, master = None, **options):
        ttk.Entry.__init__(self, master, options)
        self.Text = StringVar()
        self.configure(textvariable=self.Text)