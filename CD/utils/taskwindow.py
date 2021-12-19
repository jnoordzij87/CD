from tkinter import *
from tkinter import ttk
import tkinter as tk
from ttkwidgets import CheckboxTreeview
from utils.paths import *
from datetime import datetime
import os
from utils.updater import *
import json


class TaskWindow:

    def __init__(self, parent):
        self.PathToSourceConfigFile = '../sourceconfig.txt'
        self.CreateWindow(parent)
    
    def StartCopy(self):
        tasks = self.GetCheckedTasks(self.tree)
        sourcePaths = self.GetSourceEntryValues()

        #save entered sources in sourceconfig file for quick reruns
        self.SaveSourceConfig(sourcePaths)

        updater = Updater() 
        updater.Update(tasks, sourcePaths)
    
    def CreateWindow(self, parent):
        
        self.rowcounter = 0

        self.root = parent
        self.root.title("Tasks")

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
        
        #create continue button
        continuebutton = ttk.Button(self.mainframe, text="StartCopy", command=self.StartCopy)
        continuebutton.grid(row=self.rowcounter, sticky=W)
        self.rowcounter+=1

    
       
    def SaveSourceConfig(self, sourcePaths):
        with open(self.PathToSourceConfigFile, 'w') as outfile:
            json.dump(sourcePaths, outfile)

    def ReadSourceConfig(self):
        if not os.path.isfile(self.PathToSourceConfigFile):
            return None
        else:
            with open(self.PathToSourceConfigFile) as json_file:
                sources = json.load(json_file)
                return sources

    def GetSourceEntryValues(self):
        sourcePaths = {}
        for version in Versions:
            sourcePaths[str(version)] = {}
            for program in Programs:
                entry = self.SourceEntryLookup[str(version)][str(program)]
                entryvalue = str(entry.Text.get())
                sourcePaths[str(version)][str(program)] = entryvalue
        return sourcePaths

    def CreateSourceEntryLookup(self):
        sourceEntries = {}
        for version in Versions:
            sourceEntries[str(version)] = {}
            for program in Programs:
                sourceEntries[str(version)][str(program)] = None
        return sourceEntries

    def CreateSourceEntries(self):
        #start a lookup
        self.SourceEntryLookup = self.CreateSourceEntryLookup()
        #read sourceconfig for fast loading of sources
        previousSources = self.ReadSourceConfig()
        #build entries for programs
        for version in Versions:
            for program in Programs:
                #build label
                labeltext = "{} {} source dir".format(str(version.name), str(program.name))
                label = ttk.Label(self.mainframe, text = labeltext)
                label.grid(row=self.rowcounter, sticky=W)
                #build entry
                entry = CustomEntry(self.mainframe)
                entry.grid(row=self.rowcounter+1, sticky = (W,E))
                #set entry value from sourceconfig
                if previousSources is not None:
                    storedvalue = previousSources[str(version)][str(program)]
                    entry.Text.set(storedvalue)
                #add entry to lookup
                self.SourceEntryLookup[str(version)][str(program)] = entry
                self.rowcounter+=2

    def FillTree(self, tree):
        tree.insert("", "end", "1", text="Client")
        for env in Environments:
            tree.insert("1", "end", "1."+str(env.value), text=str(env.name))
        tree.insert("", "end", "2", text="WebService")
        for env in Environments:
            tree.insert("2", "end", "2."+str(env.value), text=str(env.name))
        
    def GetCheckedTasks(self, tree):
        checked = []
        def rec_get_checked(item):
            if tree.tag_has('checked', item):
                checked.append(item)
            for ch in tree.get_children(item):
                rec_get_checked(ch)
        rec_get_checked('')
        return checked
    
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