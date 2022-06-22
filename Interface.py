
from json import load, dump
from os.path import basename
from tkinter import *
from tkinter import ttk, filedialog
import VisualManagementArea as vma
import time
from threading import Thread

options_path = "options.json"

screens_on = False

HSS = "hss"
OPEX = "opex"
QA = "qa"
PROJ = "proj"

def update_options(new_options) -> None:
    with open(options_path, 'w') as f:
        dump(new_options, f, indent=4)
    pass


class EllipsedLabel(ttk.Label):
    def __init__(self, master=None, text=None, width=None, textvariable=None, **kwargs):
        if text and width and len(text) > width:
            text = text[:width-3] + '...'

        if textvariable and width and len(textvariable.get()) > width:
            textvariable.set(textvariable.get()[:width-3] + '...')

        ttk.Label.__init__(self, master, text=text, width=width, textvariable=textvariable, **kwargs)

class Display():
    instances = []
    def __init__(self, master=None, file=None, key=None, display=None) -> None:

        self.textvariable = StringVar()
        Display.instances.append(self)

        self.__file = ''

        if file:
            self.__file = file
            self.textvariable.set(basename(self.__file))
        
        if display:
            self.display = display
        
        if key:
            self.key = key


        self.displayFrame = ttk.Frame(master, borderwidth=5, relief="ridge")

        displayLabel = EllipsedLabel(self.displayFrame, textvariable=self.textvariable, width=12, anchor='center')
        self.displayButton = ttk.Button(self.displayFrame, text="Browse", command=self.browse_button)

        self.__fix_display_frame(self.displayFrame, displayLabel, self.displayButton)

        pass

    def __fix_display_frame(self, displayFrame: ttk.Frame, displayLabel: ttk.Label, displayButton: ttk.Button) -> None:
        displayFrame.rowconfigure(0, weight=1)
        displayFrame.rowconfigure(1, weight=1)
        displayFrame.columnconfigure(0, weight=1)
        displayFrame.columnconfigure(1, weight=1)
        displayFrame.columnconfigure(2, weight=1)
        #Places label in middle
        displayLabel.grid(column=0, row=0, columnspan=3, sticky=(W,E,S))

        #Places button in middle
        displayButton.grid(column=1, row=1, sticky=(W,E,N))

        pass

    def update_file(self, new_file) -> None:
        self.__file = new_file
        self.textvariable.set(basename(self.__file))
        pass

    def browse_button(self) -> None:

        filename = filedialog.askopenfilename(filetypes=[("Media Files", ".png .mp4")])
        filename = filename.replace("/", "\\")

        if len(filename)>0:
            self.update_file(filename)
        pass

    def browse_button_state(self, trigger) -> None:
        if trigger == "auto":
            self.displayButton.state(["disabled"])
        elif trigger == "manual":
            self.displayButton.state(["!disabled"])
        
        pass

    def set_display(self, display) -> None:
        self.display = display
        pass

    def set_key(self, key) -> None:
        self.key = key

    def get_file(self) -> str:
        return self.__file

    def turn_on(self):
        if self.__file and self.display:
            vma.turnon_screen(self.__file, self.display)

            global screens_on 
            screens_on = True

        pass

    @classmethod
    def get_display_by_key(cls, find_key):
        return [inst for inst in cls.instances if inst.key==int(find_key)]


class MainInterface():

    class TV_map():

        with open(options_path, 'r') as options_file:
            options = load(options_file)

        def __init__(self) -> None:
            pass

        def map_display(self, trigger_vars: list) -> dict:
            layout_map = {HSS: [], OPEX: [], QA: [], PROJ: []}
            vars = self.trigger_variables_dict(trigger_vars)

            displays = self.options["DISPLAY_LAYOUT"]

            for category in layout_map:
                for key in displays[category]:
                    item = displays[category][key]["Display"]

                    disp = Display.get_display_by_key(item.split('Y')[1])[0]
                    disp.set_display(item)
                    layout_map[category].append([disp, item, vars[category], category, key])

            return layout_map

        def trigger_variables_dict(self, trigger_vars):
            return {HSS: trigger_vars[0], OPEX: trigger_vars[1], QA: trigger_vars[2], PROJ: trigger_vars[3]}

        def manage_files(self, layout_items) -> None:
            for layout_item in layout_items:
                if layout_item[2].get() == "manual":
                    self.options["DISPLAY_LAYOUT"][layout_item[3]][layout_item[4]]["last_file"] = layout_item[0].get_file()

            update_options(self.options)
            pass

        def get_last_files(self, layout_items):
            for layout_item in layout_items:
                if layout_item[2].get() == "manual":
                    layout_item[0].get()


    def __init__(self, root) -> None:

        # root
        root.title("Visual Management Area") # options.json
        root.geometry('1280x480')

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # mainframe content grid
        mainframe = ttk.Frame(root, padding="5 5 15 15") #needs grid settings

        displayFrame = ttk.Frame(mainframe, padding="2 2 2 2")
        
        AutoFrame = ttk.Frame(mainframe, padding="5 5 5 5")

        # variables
        self.HS_CB_Value = StringVar(value='auto')
        self.OpEx_CB_Value = StringVar(value='auto')
        self.QA_CB_Value = StringVar(value='auto')
        self.Projects_CB_Value = StringVar(value='auto')
        self.Auto_CB_Value = BooleanVar(value=True)


        # widgets
        #   Frames:

        disp10 = Display(displayFrame, key=10)
        disp11 = Display(displayFrame, key=11)
        disp4 = Display(displayFrame, key=4)
        disp5 = Display(displayFrame, key=5)
        disp6 = Display(displayFrame, key=6)
        disp7 = Display(displayFrame, key=7)
        disp8 = Display(displayFrame, key=8)
        disp9 = Display(displayFrame, key=9)

        layout = self.TV_map()
        layout = layout.map_display([self.HS_CB_Value, self.OpEx_CB_Value, self.QA_CB_Value, self.Projects_CB_Value])

        [self.button_state_update(i, layout) for i in [HSS, OPEX, QA, PROJ]]
        self.list_files_button(layout)

        #   Labels:
        autoLabel = ttk.Label(AutoFrame,text='Auto:')

        
        #   Checkboxes:
        hsCheckbox = ttk.Checkbutton(AutoFrame, text='H&S', variable=self.HS_CB_Value, onvalue='auto', offvalue='manual', command=lambda: self.button_state_update(HSS, layout))
        opexCheckbox = ttk.Checkbutton(AutoFrame, text='OpEx', variable=self.OpEx_CB_Value, onvalue='auto', offvalue='manual', command=lambda: self.button_state_update(OPEX, layout))
        qaCheckbox = ttk.Checkbutton(AutoFrame, text='QA', variable=self.QA_CB_Value, onvalue='auto', offvalue='manual', command=lambda: self.button_state_update(QA, layout))
        projectsCheckbox = ttk.Checkbutton(AutoFrame, text='Projects', variable=self.Projects_CB_Value, onvalue='auto', offvalue='manual', command=lambda: self.button_state_update(PROJ, layout))

        #   Buttons:
        resetButton = ttk.Button(mainframe, text='Restart', command= lambda: self.restart_button(layout))
        listfilesButton = ttk.Button(mainframe, text='Update Listed Files', command= lambda: self.list_files_button(layout))
        turnoffButton = ttk.Button(mainframe, text='Turn Off', command=self.turnoff_button)
        autoButton = ttk.Checkbutton(mainframe, text='Auto On/Off', onvalue=True, offvalue=False, variable=self.Auto_CB_Value, command=None)
        syncButton = ttk.Button(mainframe, text='Sync Files', command=self.sync_files)

        # grid sizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.grid(column=0, row=0, sticky=(N, S, W, E))
        displayFrame.grid(column=2, row=2, columnspan=5, rowspan=2, sticky=(N,S,E,W))
        AutoFrame.grid(column=0, columnspan=3, row=0, sticky=(N, W, S))

            #mainframe sizing
        for i in range(2, 8, 1):
            mainframe.columnconfigure(i, weight=3)
        for i in range(2, 6, 1):
            mainframe.columnconfigure(i, weight=4, minsize=60)
        for i in range(0, 6, 1):
            mainframe.rowconfigure(i, weight=2)
        for i in range(2, 4):
            mainframe.rowconfigure(i, weight=8)

            #diplayframe sizing
        for i in range(0,4):
            displayFrame.columnconfigure(i, weight=1)
        for i in range(0,2):
            displayFrame.rowconfigure(i, weight=1)


        # widget placement
        autoLabel.grid(column=0, row=0, columnspan=2, sticky=(N, W))

        hsCheckbox.grid(column=2, row=0, sticky=(W,N))
        opexCheckbox.grid(column=3, row=0, sticky=(N))
        qaCheckbox.grid(column=4, row=0, sticky=(E, N))
        projectsCheckbox.grid(column=5, row=0, sticky=(N))


        resetButton.grid(column=0, row=5, sticky=(W,E,S))
        listfilesButton.grid(column=7, row=5, columnspan=2, sticky=(E,S))
        turnoffButton.grid(column=1, row=5, columnspan=1, sticky=(W,S))
        syncButton.grid(column=7, row=5, sticky=(W, S))
        autoButton.grid(column=6, row=5, sticky=(E,S))

            #Display frames needed fixing
        disp10.displayFrame.grid(column=0, row=0, sticky=(W,E,S,N))
        disp11.displayFrame.grid(column=1, row=0, sticky=(W,E,S,N))
        disp4.displayFrame.grid(column=2, row=0, sticky=(W,E,S,N))
        disp5.displayFrame.grid(column=0, row=1, sticky=(W,E,S,N))
        disp6.displayFrame.grid(column=1, row=1, sticky=(W,E,S,N))
        disp7.displayFrame.grid(column=2, row=1, sticky=(W,E,S,N))
        disp8.displayFrame.grid(column=3, row=1, sticky=(W,E,S,N))
        disp9.displayFrame.grid(column=3, row=0, sticky=(W,E,S,N))

        AutoFunction = Thread(target=self.auto_on_off, args=(layout,))
        AutoFunction.start()

    def button_state_update(self, group, layout) -> None:
        for groupitem in layout[group]:
            groupitem[0].browse_button_state(groupitem[2].get())
        pass

    def turnoff_button(self) -> None:
        vma.turnoff_screens()
        global screens_on
        screens_on = False
        pass

    def list_files_button(self, layout) -> None:

        for group in layout:
            if layout[group][0][2].get() == "auto":
                n_files = len(layout[group])
                if group == HSS:
                    files = vma.safety_files(n_files)
                elif group == OPEX:
                    files = vma.oe_files(n_files)
                elif group == QA:
                    files = vma.quality_files(n_files)
                elif group == PROJ:
                    files = vma.projects_files(n_files)
                else:
                    quit()

                for i in range(len(files)):
                    layout[group][i][0].update_file(files[i])
            
            elif layout[group][0][2].get() == "manual":
                if layout[group][0][0].get_file():
                    self.TV_map().manage_files(layout[group])
                else:
                    self.TV_map().get_last_files(layout[group])

        pass

    def restart_button(self, layout) -> None:
        for group in layout:
            for groupitem in layout[group]:
                groupitem[0].turn_on()

    def auto_on_off(self, layout) -> None:
        onTime = self.TV_map().options["AUTO"]["On"].split(':') #[0]: hours, [1]: minutes
        offTime = self.TV_map().options["AUTO"]["Off"].split(':')

        if onTime[0]==0 and onTime[1]==0 and offTime[0]==0 and offTime[1]==0:
            return


        global screens_on

        while True:
            while self.Auto_CB_Value.get():
                currentTime = time.localtime() # [3]: hours, [4]: minutes
                if screens_on:
                    if int(currentTime[3]) > int(offTime[0]) or int(currentTime[3]) < int(onTime[0]):
                        self.turnoff_button()
                    elif int(currentTime[3]) == int(offTime[0]) and int(currentTime[4]) >= int(offTime[1]):
                        self.turnoff_button()
                    elif int(currentTime[3]) == int(onTime[0]) and int(currentTime[4]) <= int(offTime[1]):
                        self.turnoff_button()
                else:
                    if int(currentTime[3]) > int(onTime[0]) or int(currentTime[3]) < int(offTime[0]):
                        self.list_files_button(layout)
                        self.restart_button(layout)
                    elif int(currentTime[3]) == int(onTime[0]) and int(currentTime[4]) > int(onTime[1]):
                        self.list_files_button(layout)
                        self.restart_button(layout)
                    elif int(currentTime[3]) == int(offTime[0]) and int(currentTime[4]) < int(offTime[1]):
                        self.list_files_button(layout)                        
                        self.restart_button(layout)
                time.sleep(120)
            time.sleep(10)

    
    def sync_files(self):
        vma.sync_files("C:\\VM_Tasks\\xcopy_VM.cmd")
        pass

if __name__ == "__main__":

    root = Tk()
    root.title("Visual Management Area")

    interfa = MainInterface(root)

    root.mainloop()