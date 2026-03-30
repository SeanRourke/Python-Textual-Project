from textual.app import App, ComposeResult
from textual.widgets import Select, Label, Header, Footer, Static, Button, OptionList
from textual import on
import swim_utils
from textual.reactive import reactive
from textual.containers import ScrollableContainer
import os
import webbrowser

FOLDER = "swimdata/"

name_set = set()
files = os.listdir(FOLDER)
for filename in files:
    name = filename.split('-')[0]
    name_set.add(name)
name_list = list(name_set)
name_list.sort()
swim_list = []
swim_select = OptionList(swim_list)
swim_select.add_class("hidden")
swimmer_title = Label("Select Swimmer")
swim_title = Label(("Select Swim"), classes="hidden")
swimmer_list = Select(((name, name) for name in name_list), id="swimmers")
selected_name = " "
distance = " "
stroke = " "
times = []
values = []
option = " "
suffix = ".txt"
data = []
converts = []
title = " "
confirm = Label(("Would you like to view another set of results"), classes="hidden")
yes = Button(("Yes"), id="yes", classes="hidden", variant="success")
no = Button(("No"), id="no", classes="hidden", variant="error")


class Buttons(Static):


    def compose(self):
        yield yes
        yield no


    @on(Button.Pressed, "#yes")
    def restart(self):
        swimmer_title.remove_class("hidden")
        swimmer_list.remove_class("hidden")
        confirm.add_class("hidden")
        yes.add_class("hidden")
        no.add_class("hidden")


    @on(Button.Pressed, "#no")
    def close(self):
        app.exit()


class Menus(Static):
    

    @on(Select.Changed, "#swimmers")
    def swimmer_changed(self, event:Select.Changed):
        """ When the selection is made from the list of swimmers, display list of swims for that
        swimmer.
        """

        swim_title.remove_class("hidden")
        self.selected_name = event.value
        if self.selected_name in name_list:
            swim_list = []
            for filename in files:
                filename = filename.removesuffix(".txt")
                name = filename.split('-')[0]
                if name == self.selected_name:
                    self.age = str(filename.split('-')[1])
                    swim = str((filename.split('-')[2]) + '-' + (filename.split('-')[3]))                    
                    swim_list.append(str(swim))
        swim_select.clear_options()
        swim_select.add_options(swim_list)
        swim_select.remove_class("hidden")
        self.mount(swim_select)
        

    @on(OptionList.OptionSelected)
    def swim_changed(self, event:OptionList.OptionSelected):
        """ When the swim is selected for the chosen swimmer, get that swimmer's data from their textfile
        and call for the creation of html file using their data. Remove the selections from the screen, ask 
        if the user wants to see another set of results and display buttons for yes and no
        """

        index = event.option_index
        option = swim_select.get_option_at_index(index).prompt
        self.distance = str(option.split('-')[0])
        self.stroke = str(option.split('-')[1])
        selected_file = str(self.selected_name + '-' + self.age + '-' + self.distance + '-' + self.stroke + suffix)
        self.data = swim_utils.get_swimmers_data(selected_file)
        self.create_html(self.data)
        swimmer_title.add_class("hidden")
        swimmer_list.add_class("hidden")
        swim_title.add_class("hidden")
        swim_select.add_class("hidden")
        confirm.remove_class("hidden")
        yes.remove_class("hidden")
        no.remove_class("hidden")


    def create_html(self, data):
        """ Given the data of a swimmer, create html file of a bar chart of their data and display the average of the times
        """

        self.selected_name, self.age, self.distance, self.stroke, self.times, self.values, self.average = self.data

        self.converts = []

        for n in self.values:
            self.converts.append(swim_utils.convert2range(n, 0, max(self.values)+50, 0, 400))

        self.title = f"{self.selected_name} (Under {self.age}) {self.distance} - {self.stroke}"

        header = f"""

        <!DOCTYPE html>
        <html>
            <head>
                <title>
                    {self.title}
                </title>
            </head>
            <body>
                <h3>{self.title}</h3>

        """

        body = ""
        for t, c in zip(self.times, self.converts):
            svg = f"""
                    <svg height="30" width="400">
                        <rect height="30" width="{c}" style="fill:rgb(0,0,255);" />
                    </svg>{t}<br />
                """
            body = body + svg

        footer = f"""
                <p>Average: {self.average}</p>
            </body>
        </html>
        """

        html = header + body + footer

        html_name = f"{self.selected_name}-{self.age}-{self.distance}-{self.stroke}.html"

        with open(html_name, "w") as df:
            print(html, file=df)

        webbrowser.open(os.path.realpath(html_name))

    
    def compose(self):
        yield swimmer_title
        yield swimmer_list
        yield swim_title
        yield confirm
        self.selected_name = None
        self.age = None
        self.stroke = None
        self.distance = None
        self.data = None
        self.times = None
        self.values = None
        self.converts = None
        self.average = None
        self.title = None


class SwimApp(App):

    CSS_PATH = "assignment.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with ScrollableContainer(id="container"):
            yield Menus() 
            yield Buttons()  


if __name__ == "__main__":
    app = SwimApp()
    app.run()