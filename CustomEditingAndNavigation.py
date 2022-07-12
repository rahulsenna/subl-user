import sublime
import sublime_plugin


class OpenInOppositeGroupCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('clone_file')
        self.window.run_command('move_to_neighboring_group', {"forward": False})


class DeselectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        end = self.view.sel()[0].b
        pt = sublime.Region(end, end)
        self.view.sel().clear()
        self.view.sel().add(pt)


class SemicolonCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        self.view.run_command('move_to', {"to": "hardeol", "extend": False})
        if self.view.syntax().name == 'Python':
            return
        for region in reversed(self.view.sel()):
            region_begin = region.begin()
            current_line_reg = self.view.full_line(region)
            next_region = sublime.Region(current_line_reg.b +1, current_line_reg.b +1)
            next_line = self.view.substr(self.view.full_line(next_region))
            current_line = self.view.substr(current_line_reg)

            region_begin_next = region.begin() - 1
            prev_char = self.view.substr(region_begin_next)
            print(prev_char)
            if (prev_char != ";" and prev_char != "," and "{" not in next_line and "{" not in current_line
                and "#" not in current_line 
                and len(current_line.strip()) > 0):
                edit_region = sublime.Region(region_begin, region.end())
                self.view.replace(edit, edit_region, ";")
                edit_region = 0

        self.view.run_command('deselect')

class FormatLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        current_line_reg = self.view.full_line(self.view.sel()[0])
        print(current_line_reg)
        self.view.sel().add(current_line_reg)
        self.view.run_command("lsp_format_document_range")


class ToggleArrowCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        for region in reversed(self.view.sel()):
            if region.size() == 0:
                # Try one character beside the region to see what we've got
                region_begin = region.begin()
                next_char = self.view.substr(region_begin)
                region_begin_next = region.begin() - 1
                prev_char = self.view.substr(region_begin_next)
                if next_char == ".":
                    # Replace with arrow
                    edit_region = sublime.Region(region_begin, region.end() + 1)
                    self.view.replace(edit, edit_region, "->")
                elif next_char == "-":
                    # Check if it's an arrow
                    edit_region = sublime.Region(region_begin, region.end() + 2)
                    if self.view.substr(edit_region) == "->":
                        self.view.replace(edit, edit_region, ".")
                        # TODO: Switch back to behind the edit point
                elif next_char == ">":
                    # Check if it's an arrow (we might be in the middle, e.g. after dot conversion)
                    edit_region = sublime.Region(region_begin - 1, region.end() + 1)
                    if self.view.substr(edit_region) == "->":
                        self.view.replace(edit, edit_region, ".")
                elif prev_char == ".":
                    # Replace with arrow
                    edit_region = sublime.Region(region_begin_next, region.end())
                    self.view.replace(edit, edit_region, "->")
                elif prev_char == ">":
                    # Check if it's an arrow (we might be in the middle, e.g. after dot conversion)
                    edit_region = sublime.Region(region_begin_next - 1, region.end() )
                    if self.view.substr(edit_region) == "->":
                        self.view.replace(edit, edit_region, ".")

            else:
                # Try to see if the selected text is something we want to replace
                sel_text = self.view.substr(region)
                if sel_text == ".":
                    self.view.replace(edit, region, "->")
                elif sel_text == "->":
                    self.view.replace(edit, region, ".")




import os.path
import platform
def compare_file_names(x, y):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        return x.lower() == y.lower()
    else:
        return x == y


class SwitchHeaderSourceCommand(sublime_plugin.WindowCommand):
    def run(self, extensions=[]):
        group = 0 if self.window.active_group() else 1
        if not self.window.active_view():
            return

        fname = self.window.active_view().file_name()
        if not fname:
            return

        base, ext = os.path.splitext(fname)

        start = 0
        count = len(extensions)

        if ext != "":
            ext = ext[1:]

            for i in range(0, len(extensions)):
                if compare_file_names(extensions[i], ext):
                    start = i + 1
                    count -= 1
                    break

        for i in range(0, count):
            idx = (start + i) % len(extensions)

            new_path = base + '.' + extensions[idx]

            if os.path.exists(new_path):
                self.window.open_file(new_path, group=group)
                break

class RunExeCommand(sublime_plugin.WindowCommand):
    def run(self, extensions=[]):
        path = self.window.folders()[0]
        self.window.run_command("exec",  {"cmd": path +"\\misc\\runAPP.bat "+ path})

class FiftyLinesUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for i  in range(5):
            self.view.run_command("move", {"by": "stops", "empty_line": True, "forward": False, "extend": False} )

class FiftyLinesDownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for i  in range(5):
            self.view.run_command("move", {"by": "stops", "empty_line": True, "forward": True, "extend": False} )


class ReplaceLeftCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("move", {"by": "word_ends", "forward": False} )
        self.view.run_command("move", {"by": "word_ends", "forward": False} )

        self.view.run_command("find_under_expand")


class ReplaceRightCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("move", {"by": "word_ends", "forward": True} )
        self.view.run_command("find_under_expand")


class ReplaceUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("move", {"by": "lines", "forward": False} )
        self.view.run_command("find_under_expand")

class ReplaceDownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("move", {"by": "lines", "forward": True} )
        self.view.run_command("find_under_expand")


class ReplaceMultiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("find_under_expand")
        sublime.active_window().run_command('toggle_red')



import time
import threading


# def caret_color(self, color):
#     for window in sublime.windows():
#         for view in window.views():
#             if(view.settings().get('color_scheme') == "Packages/User/"+color+".sublime-color-scheme"):
#                 return
#             settings = view.settings()
#             settings.set('color_scheme', 'Packages/User/'+color+'.sublime-color-scheme')

#     sett = sublime.load_settings("Preferences.sublime-settings")
#     sett.set('color_scheme', 'Packages/User/'+color+'.sublime-color-scheme')
#     sublime.save_settings("Preferences.sublime-settings")


# class ToggleGreenCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         r1 = threading.Thread(target=caret_color, args=(self, 'ColorGreen'))
#         r1.start()


# class ToggleRedCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         r1 = threading.Thread(target=caret_color, args=(self, 'ColorRed'))
#         r1.start()


# class Listener(sublime_plugin.EventListener):
#     def on_post_text_command(self, view, command_name, args):
#         if command_name == 'lsp_symbol_definition':
#             r1 = threading.Thread(target=call_lsp_symbol_references, args=(self, view))
#             r1.start()


# def call_lsp_symbol_references(self, view):
#     time.sleep(.2)
#     sublime.active_window().active_view().run_command('lsp_symbol_references')
