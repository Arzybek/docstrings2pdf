from fpdf import FPDF


class pdfConverter:
    def __init__(self, parser, output):
        self.lister = parser
        self.output = output
        self.define_state()
        self.initialize_pdf()
        self.add_cells()
        self.create_pdf()

    def define_state(self):
        if (self.lister.state == 0):
            self.name = self.lister.name
            self.docstrings = self.lister.info.docstrings
            self.list = self.lister.info.classes + self.lister.info.functions
        elif (self.lister.state == 1):
            self.name = self.lister.current_class.name
            self.docstrings = self.lister.current_class.docstrings
            self.list = self.lister.current_class.functions
        elif (self.lister.state == 2 or 3):
            self.name = self.lister.current_func.name
            self.docstrings = self.lister.current_func.docstrings
            self.list = [self.lister.current_func.definition]

    def initialize_pdf(self):
        self.pdf = FPDF()
        self.pdf.add_page()

    def add_cells(self):
        if self.lister.state == 0:
            name = 'Module'
        elif self.lister.state == 1:
            name = 'Class'
        else:
            name = 'Func'
        self.pdf.set_font('Arial', size=20, style='U')
        self.pdf.cell(10, 10, txt='{} Name: '.format(name) + self.name, ln=1)
        self.pdf.set_font('Arial', size=15)
        self.pdf.cell(10, 10, txt='Docstring: ' + self.docstrings, ln=1)
        if (self.lister.state == 0):
            for one in self.list:
                if (hasattr(one, "functions")):
                    self.pdf.set_font('Arial', size=15, style='I')
                    self.pdf.cell(10, 10, txt='Class name: ' + one.name, ln=1)
                    self.pdf.set_font('Arial', size=12)
                    self.pdf.cell(10, 10, txt='Docstring: ' + one.docstrings, ln=1)
                    self.pdf.set_font('Arial', size=12)
                    self.pdf.cell(10, 10, txt='Parent: ' + str(one.parent), ln=1)
                    for another_one in one.functions:
                        self.pdf.set_font('Arial', size=12, style='I')
                        self.pdf.cell(10, 10, txt='Func name: ' + another_one.name, ln=1)
                        self.pdf.set_font('Arial', size=10)
                        self.pdf.cell(10, 10, txt='Docstring: ' + another_one.docstrings, ln=1)
                        self.pdf.set_font('Arial', size=10)
                        self.pdf.cell(10, 10, txt='Defn: ' + another_one.definition, ln=1)
                else:
                    self.pdf.set_font('Arial', size=15, style='I')
                    self.pdf.cell(10, 10, txt='Func name: ' + one.name, ln=1)
                    self.pdf.set_font('Arial', size=12)
                    self.pdf.cell(10, 10, txt='Docstring: ' + one.docstrings, ln=1)
                    self.pdf.set_font('Arial', size=12)
                    self.pdf.cell(10, 10, txt='Defn: ' + one.definition, ln=1)
        elif self.lister.state == 1:
            self.pdf.set_font('Arial', size=15)
            self.pdf.cell(10, 10, txt='Parent: ' + str(self.lister.current_class.parent), ln=1)
            for one in self.list:
                self.pdf.set_font('Arial', size=15, style='I')
                self.pdf.cell(10, 10, txt='Func name: ' + one.name, ln=1)
                self.pdf.set_font('Arial', size=12)
                self.pdf.cell(10, 10, txt='Docstring: ' + one.docstrings, ln=1)
                self.pdf.set_font('Arial', size=12)
                self.pdf.cell(10, 10, txt='Defn: ' + one.definition, ln=1)
        else:
            for one in self.list:
                self.pdf.set_font('Arial', size=15)
                self.pdf.cell(10, 10, txt='Defn: ' + one, ln=1)


    def create_pdf(self):
        self.pdf.output(self.output)
