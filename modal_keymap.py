import sublime
import sublime_plugin

import sys
import threading

if sys.platform == 'win32':
    sys.path.insert(4, 'C:\\Python39\\lib\\site-packages')
elif sys.platform == 'darwin':
    sys.path.insert(4, '/usr/lib/python3/dist-packages')
    sys.path.insert(4, '/usr/local/lib/python3.10/site-packages')
else:
    sys.path.insert(4, '/usr/lib/python3.10/site-packages')
    sys.path.insert(4, '/home/agent/.local/lib/python3.10/site-packages')



from pynput.keyboard import Key, Listener

# GREEN = 'ColorGreen'
# RED = 'ColorRed'

GREEN = 'DARKColorGreen'
RED = 'DARKColorRed'
RED = 'JWORT'
GREEN = 'JWORT_GREEN'

# GREEN = 'ColorGruvBlue'
# RED = 'ColorGruvRed'


active_view = sublime.active_window().active_view()

motion_repeat_digits = []
class PushRepeatDigit(sublime_plugin.TextCommand):
    def run(self, edit, digit):
        global motion_repeat_digits
        motion_repeat_digits.append(digit)


class EvtListener(sublime_plugin.EventListener):
    def on_init(self, views):
        global active_view
        active_view = sublime.active_window().active_view()
        sublime.active_window().run_command('toggle_green')
        for v in views:
            v.settings().set('command_mode', True)
            v.settings().set('word_mode', False)
            v.settings().set('subword_mode', False)
            v.settings().set('delete_mode', False)
            v.settings().set('visual_mode', False)

    def on_activated_async(self, view):
        global active_view
        active_view = view
        update_status(view)

    def on_new(self, view):
        view.settings().set('command_mode', True)
        sublime.active_window().run_command('toggle_green')

        
    def on_load(self, view):
        view.settings().set('command_mode', True)
        sublime.active_window().run_command('toggle_green')


    def on_post_text_command(self, view, command_name, args):
        if command_name == 'cut' or command_name == 'copy' or command_name == 'paste':
            # if not len(view.sel()) > 1:
                # view.run_command('deselect')
            view.settings().set('visual_mode', False)

        if command_name == 'find_under_expand':
            view.settings().set('visual_mode', False)

    #Jumping to a line
    def on_text_command(self, view, command_name, args):
        global motion_repeat_digits
        if command_name == 'move' and args['by'] == 'lines' and motion_repeat_digits:
            digit_as_char_in_list = [str(integer) for integer in motion_repeat_digits]
            digits_as_string = "".join(digit_as_char_in_list)
            nums_of_lines = int(digits_as_string) - 1
            motion_repeat_digits.clear()

            for x in range(nums_of_lines):
                view.run_command(command_name, args)


def caret_color(self, color):
    for view in sublime.active_window().views():
        if(view.settings().get('color_scheme') == "Packages/User/"+color+".sublime-color-scheme"):
            return

        view.settings().set('color_scheme', 'Packages/User/'+color+'.sublime-color-scheme')
        command_mode = color == GREEN
        view.settings().set('command_mode', command_mode)

    sett = sublime.load_settings("Preferences.sublime-settings")
    sett.set('color_scheme', 'Packages/User/'+color+'.sublime-color-scheme')
    sublime.save_settings("Preferences.sublime-settings")

    global active_view
    update_status(active_view)


class SpaceThenRedCommand(sublime_plugin.WindowCommand):
    def run(self):
        global active_view
        active_view.settings().set('command_mode', False)
        active_view.run_command('insert', {"characters": " "})
        r1 = threading.Thread(target=caret_color, args=(self, RED))
        r1.start()


class ToggleGreenCommand(sublime_plugin.WindowCommand):
    def run(self):
        global active_view
        active_view.settings().set('command_mode', True)
        r1 = threading.Thread(target=caret_color, args=(self, GREEN))
        r1.start()


class ToggleGreenInsertCommand(sublime_plugin.WindowCommand):
    def run(self):
        global active_view
        active_view.settings().set('command_mode', False)
        active_view.settings().set('command_mode_insert', True)


class ToggleRedCommand(sublime_plugin.WindowCommand):
    def run(self):
        global active_view
        active_view.settings().set('command_mode', False)
        r1 = threading.Thread(target=caret_color, args=(self, RED))
        r1.start()


class ToggleVisualCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.settings().get('visual_mode'):
            self.view.settings().set('visual_mode', False)
            self.view.run_command('deselect')
        else:
            self.view.settings().set('visual_mode', True)


def update_status(view):
    if view.settings().get('command_mode'):
        view.set_status('mode', 'COMMAND MODE')

    if not view.settings().get('command_mode'):
        view.set_status('mode', 'INSERT MODE')

    if view.settings().get('visual_mode'):
        view.set_status('mode', 'VISUAL MODE')

    if view.settings().get('word_mode'):
        view.set_status('mode', 'WORD MODE')

    if view.settings().get('subword_mode'):
        view.set_status('mode', 'SUBWORD MODE')


class d_down(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.settings().set('word_mode', True)


class s_down(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.settings().set('subword_mode', True)


class f_down(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.settings().set('delete_mode', True)
        self.view.settings().set('visual_mode', False)


def on_press(key):
    global active_view

    if key == Key.shift or key == Key.shift_r:
        if not active_view.settings().get('command_mode_insert'):
            sublime.active_window().run_command('toggle_red')

    if key == Key.esc:
        active_view.settings().set('visual_mode', False)
        active_view.run_command('deselect')


prev_key = ''


def on_release(key):
    global active_view, prev_key

    if key == Key.space and active_view.settings().get('command_mode_insert'):
        active_view.settings().set('command_mode_insert', False)
        active_view.settings().set('command_mode', True)

    try:
        if key.char.lower() == 's' and prev_key != 'a':
            active_view.settings().set('subword_mode', False)

        if key.char.lower() == 'd':
            active_view.settings().set('word_mode', False)

        if key.char.lower() == 'f':
            active_view.settings().set('delete_mode', False)

        if key.char.lower() == 'w':
            active_view.settings().set('prev_key_w', True)

        if key.char.lower() != 'w' and key.char.lower() != 'e' and (prev_key == 'w' or prev_key == 'e'):
            active_view.settings().set('prev_key_w', False)

        prev_key = key.char.lower()
    except AttributeError:
        pass

    # print('{0} release'.format(key))

    # update_status(active_view)

    # if key == Key.esc:
    #     active_view.settings().set('visual_mode', False)
    #     active_view.run_command('deselect')


listener = Listener(on_press=on_press,
                    on_release=on_release)
listener.start()

# listener = Listener(on_release=on_release)
# listener.start()
