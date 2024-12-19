__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""

from fpdf import FPDF

class pdf(FPDF):
    """
    A class for generating PDF release notes for a devcontainer.

    Args:
        file_path (str): The file path where the generated PDF will be saved.

    Attributes:
        file_path (str): The file path where the generated PDF will be saved.
    """

    def __init__(self, file_path: str):
        orientation = 'P'
        unit = 'mm'
        format = 'A4'
        super().__init__(orientation, unit, format)

        self.file_path = file_path


    def header(self):
        """
        Sets the header of the PDF document.
        """

        title = "Devcontainer release note"
        self.set_font('helvetica', 'B', 25)
        self.set_text_color(0, 0, 0)
        title_w = self.get_string_width(title) + 15
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        self.cell(title_w, 10, title, ln=True, align='C')
        self.image(f"{self.file_path}/BOSCH_TOP_RGB.png", x=10, y=10, w=30)
        self.ln(20)
    

    def footer(self):
        """
        Set the footer of the PDF document.
        """

        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')


    def __headline1(self, headline):
        """
        Adds a headline to the PDF document.

        Args:
            headline (str): The headline to be added.
        """

        self.add_page()
        self.set_font('helvetica', '', 18)
        self.set_text_color(0, 0, 0)
        self.cell(200, 5, headline, ln=True)
        self.ln()


    def __headline2(self, headline):
        """
        Adds a sub headline to the PDF document.

        Args:
            headline (str): The sub headline to be added.
        """

        self.set_font('helvetica', '', 14)
        self.set_text_color(0, 0, 0)
        self.cell(200, 5, headline, ln=True)


    def __chapter_text(self, text):
        """
        Sets the font and alignment for the chapter text and prints it in the PDF.

        Args:
            text (str): The text to be printed.

        """
        if text == "--No changes--":
            self.set_font('helvetica', 'I', 10)
        else:
            self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5, text, align="L")


    def __list_item(self, key, value, link=""):
        """
        Add a list item to the PDF document.

        Args:
            key (str): The key of the list item.
            value (str): The value of the list item.
            link (str, optional): The link associated with the list item. Defaults to "".
        """
        self.set_font('helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.cell(30, 7, key)
        if link:
            self.set_font('helvetica', 'U', 10)
            self.set_text_color(0, 0, 255)
            self.cell(0, 7, value, ln=True, link=link)
        else:
            self.set_text_color(0, 0, 0)
            self.cell(0, 7, value, ln=True)


    def __dockerfile_changes(self, dockerfile_changes):
        """
        Generate the section for Dockerfile changes in the release note.

        Args:
            dockerfile_changes (list): List of lines representing the changes in the Dockerfile.
        """
        self.__headline1("Dockerfile changes")
        if not dockerfile_changes:
            self.__chapter_text("--No changes--")
            return
        
        for line in dockerfile_changes:
            if line[0:3] == "---" or line[0:3] == "+++":
                continue
            if line[0:2] == "@@":
                self.ln()
            if line[0] == "+":
                self.set_text_color(0, 200, 100)
                self.__chapter_text(line)
            elif line[0] == "-":
                self.set_text_color(255, 0, 0)
                self.__chapter_text(line)
            else:
                self.set_text_color(0, 0, 0)
                self.__chapter_text(line)


    def __package_changes(self, kind, package_changes):
        """
        Generate the package changes section for a given kind of package.

        Args:
            kind (str): The kind of package.
            package_changes (dict): A dictionary containing the package changes.
        """
        self.__headline1(f"{kind} package changes")
        for key, value in package_changes.items():
            self.__headline2(f"{key}:")
            if value:
                self.__chapter_text("\n".join(value))
            else:
                self.__chapter_text("--No changes--")
            self.ln()


    def generate_pdf(self, version: str, commit_id: str, commit_url: str, docker_dir: str, build_reason: str, dockerfile_changes: list, apt_package_changes: dict, pip_package_changes: dict):
            """
            Generates a PDF release note with the given information.

            Args:
                version (str): The version of the release.
                commit_id (str): The ID of the commit.
                commit_url (str): The URL of the commit.
                docker_dir (str): The directory of the Dockerfile.
                build_reason (str) : Reason for the build
                dockerfile_changes (list): The list of changes made to the Dockerfile.
                apt_package_changes (dict): The dictionary of changes made to the Apt packages.
                pip_package_changes (dict): The dictionary of changes made to the Pip packages.
            """
            
            print("Generating PDF...")
            self.alias_nb_pages()
            self.set_auto_page_break(auto=True, margin=15)

            self.__headline1("General information")
            self.__list_item("Version:", version)
            self.__list_item(f"Commit Id:", commit_id, commit_url)
            self.__list_item(f"Used dockerfile:", f"{docker_dir}/Dockerfile")
            self.__list_item("Build Reason:", build_reason)

            self.__dockerfile_changes(dockerfile_changes)
            self.__package_changes("Apt", apt_package_changes)
            self.__package_changes("Pip", pip_package_changes)

            self.output(f"{self.file_path}/devcontainer_release_note_{version}.pdf")
