from shutil import get_terminal_size
from enum import Enum
from lucxbox.lib.color_string import Color, ColorString


class Status(Enum):
    okay = 1
    info = 2
    warning = 3
    error = 4


class Printer():
    def __init__(self,
                 line_width=get_terminal_size()[0] - 1,
                 content_color=Color.default,
                 title_color=Color.default,
                 box_color=Color.default,
                 line_offset_symbol=' ',
                 left_right_symbol='|',
                 corners_symbol='+',
                 top_bottom_symbol='-'):

        if line_width % 2 == 0:
            self._width = line_width
        else:
            self._width = line_width - 1

        self._color_content = content_color
        self._color_title = title_color
        self._color_box = box_color

        self._box_symbol_left_right = left_right_symbol
        self._box_symbol_top_bottom = top_bottom_symbol
        self._box_symbol_corners = corners_symbol
        self._line_symbol_offset = line_offset_symbol

        self._max_line_width = self._width - \
            (2 * len(self._box_symbol_left_right))
        self._max_title_width = self._width - \
            (2 * len(self._box_symbol_corners)) - \
            (2 * len(self._box_symbol_top_bottom)) - 2

    # pylint: disable=R0914, R0912
    def set_layout(self,
                   line_width=None,
                   content_color=None,
                   title_color=None,
                   box_color=None,
                   line_offset_symbol=None,
                   left_right_symbol=None,
                   corners_symbol=None,
                   top_bottom_symbol=None):
        if line_width:
            new_line_width = line_width
        else:
            new_line_width = self._width
        if content_color:
            new_content_color = content_color
        else:
            new_content_color = self._color_content
        if title_color:
            new_title_color = title_color
        else:
            new_title_color = self._color_title
        if box_color:
            new_box_color = box_color
        else:
            new_box_color = self._color_box
        if line_offset_symbol:
            new_line_offset_symbol = line_offset_symbol
        else:
            new_line_offset_symbol = self._line_symbol_offset
        if left_right_symbol:
            new_left_right_symbol = left_right_symbol
        else:
            new_left_right_symbol = self._box_symbol_left_right
        if corners_symbol:
            new_corners_symbol = corners_symbol
        else:
            new_corners_symbol = self._box_symbol_corners
        if top_bottom_symbol:
            new_top_bottom_symbol = top_bottom_symbol
        else:
            new_top_bottom_symbol = self._box_symbol_top_bottom

        self.__init__(new_line_width, new_content_color, new_title_color, new_box_color,
                      new_line_offset_symbol, new_left_right_symbol, new_corners_symbol, new_top_bottom_symbol)

    def divider(self):
        print(ColorString(self._box_symbol_corners + (self._width - 2) *
                          self._box_symbol_top_bottom + self._box_symbol_corners, self._color_box))

    @staticmethod
    def get_status_string(status, status_message=None):
        status_color = None
        status_content = None
        if status == Status.info:
            status_color = Color.cyan
            status_content = 'INFO'
        elif status == Status.okay:
            status_color = Color.green
            status_content = 'OK'
        elif status == Status.warning:
            status_color = Color.yellow
            status_content = 'WARNING'
        elif status == Status.error:
            status_color = Color.red
            status_content = 'ERROR'

        if status_message is not None:
            status_content = str(status_message)

        return ColorString('[', Color.grey) + ColorString(status_content, status_color) + ColorString(']', Color.grey)

    @staticmethod
    def get_string_parts_w_max_length(string, max_length):
        splitted_string = []
        current_string = string
        while len(current_string) > max_length:
            splitted_string.append(current_string[:max_length])
            current_string = current_string[max_length:]
        splitted_string.append(current_string)
        return splitted_string

    def title(self, title, color=None):
        title_splitted = Printer.get_string_parts_w_max_length(
            title, self._max_title_width)
        title_to_print = title_splitted[0]
        if len(title_splitted) > 1:
            title_to_print = title_to_print[:-3] + '...'

        title_to_print = ' ' + title_to_print + ' '

        if color:
            title_color = color
        else:
            title_color = self._color_title

        title_colored = ColorString(title_to_print, title_color)

        width_corners = 2 * len(self._box_symbol_corners)
        width_lines = (self._width - len(title_colored) - width_corners) / 2
        width_title_line_left = width_title_line_right = int(width_lines)

        if str(width_lines).split('.')[1] == '5':
            width_title_line_left += 1

        left = self._box_symbol_corners + \
            (width_title_line_left * self._box_symbol_top_bottom)
        right = (width_title_line_right *
                 self._box_symbol_top_bottom) + self._box_symbol_corners

        left_colored = ColorString(left, self._color_box)
        right_colored = ColorString(right, self._color_box)

        print(left_colored + title_colored + right_colored)

    def __print_box_line(self, content):
        content = ' ' + content + ' '
        left_box = ColorString(self._box_symbol_left_right, self._color_box)
        right_box = ColorString(
            ' ' * (self._max_line_width - len(content)) + self._box_symbol_left_right, self._color_box)
        print(left_box + content + right_box)

    def __print_without_status(self, content, offset=0, color=None):
        max_content_width = self._max_line_width - offset - 2
        content_splitted = Printer.get_string_parts_w_max_length(
            content, max_content_width)

        offset_string = offset * self._line_symbol_offset

        for content_part in content_splitted:
            to_print = offset_string + ColorString(content_part, color)
            self.__print_box_line(to_print)

    def __print_with_status(self, content, offset=0, color=None, status=None, status_content=None):
        status_string = Printer.get_status_string(status, status_content)
        status_string = ' ' + status_string

        max_content_width = self._max_line_width - \
            offset - len(status_string) - 2
        content_splitted = Printer.get_string_parts_w_max_length(
            content, max_content_width)

        offset_string = offset * self._line_symbol_offset

        for i, content_split in enumerate(content_splitted):
            content_colored = ColorString(content_split, color)
            to_print = None
            if i == len(content_splitted) - 1:
                to_print = content_colored + \
                    ((max_content_width - len(content_colored)) * ' ') + status_string
            else:
                to_print = content_colored
            to_print = offset_string + to_print
            self.__print_box_line(to_print)

    def print(self, content, offset=0, color=None, status=None, status_content=None):
        if status:
            self.__print_with_status(
                content, offset, color, status, status_content)
        else:
            self.__print_without_status(content, offset, color)
