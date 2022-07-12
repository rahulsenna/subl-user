# import sublime

# import os
# from sublime_plugin import EventListener
# from sublime_plugin import WindowCommand

# import threading
# import ctypes
# import sublime_plugin


# hwndSublime = ctypes.windll.user32.FindWindowA(b'PX_WINDOW_CLASS', None)
# def ChangeWintitle(self, name):
#       if(hwndSublime):
#         ctypes.windll.user32.SetWindowTextW(hwndSublime, name)


# class EnterInsertMode(sublime_plugin.TextCommand):
#     def run(self, edit):
#         r2 = threading.Thread(target=CaretColor, args=(self, 'red'))
#         r2.start()
#         self.view.settings().set('command_mode', False)
#         # self.view.settings().set('inverse_caret_state', False)

# class ExitInsertMode(sublime_plugin.TextCommand):
#     def run(self, edit):
#         r2 = threading.Thread(target=CaretColor, args=(self, 'green'))
#         r2.start()
#         self.view.settings().set('command_mode', True)
#         # self.view.settings().set('inverse_caret_state', True)




# def CaretColor(self, color):
#     for window in sublime.windows():
#         for view in window.views():
#             if(view.settings().get('color_scheme') == "Packages/User/"+color+".sublime-color-scheme"):
#                 return
#             settings = view.settings()
#             settings.set('color_scheme', 'Packages/User/'+color+'.sublime-color-scheme')

#     sett = sublime.load_settings("Preferences.sublime-settings")
#     sett.set('color_scheme', 'Packages/User/'+color+'.sublime-color-scheme')
#     sublime.save_settings("Preferences.sublime-settings")