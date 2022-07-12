import sublime
import sublime_plugin

import re
import json

from sys import platform

class CompileJsonCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		
		compiler = 'clang '
		inc_flag = '-include '
		if platform == 'win32':
			inc_flag = '/FI'
			compiler = 'cl '

		compile_commands = []
		dict_includes = {}
		
		includes = ['{}Unknown.h'.format(inc_flag)] # force including some fake.h makes clangd behave much nicer, doesn't give you irrelevant nonsensical errors.
		
		clang_compiler_flags = '-Wno-error -Wno-shadow -Wno-deprecated-declarations -Wno-bool-conversion -Wno-writable-strings -Wno-null-dereference -Wno-string-compare -Wno-unused-variable -Wno-infinite-recursion -Werror=implicit-function-declaration -Wno-shadow-field-in-constructor-modified -Wno-shadow-ivar -Wuninitialized -Wunused-label -Wunused-lambda-capture'

		proj_dir = sublime.windows()[0].extract_variables()['project_path']

		build_script = proj_dir+'/misc/build.sh'
		if platform == 'win32':
			build_script = proj_dir+'\\misc\\build.bat'

		print(build_script)
	

		## fetching cpp file names and compile info from built.bat
		files_to_compile = []
		definitions = ''
		with open(build_script) as f: built_bat_text = f.readlines()
		for line in built_bat_text:
			if 'NO_COMPILE_COMANDS_HELPER' in line: return 0
			try:
			 	cpp_path = re.search(r'^cl.*\.\.(.*\.c(?:pp)?)', line).groups()[0]

			 	files_to_compile.append(proj_dir+cpp_path)
			except:
				pass
			try:
				if platform == 'darwin' or platform == 'linux':	
					definitions = re.search(r'^Definitions="(.*)"', line).groups()[0]
				if platform == 'win32':	
					definitions = re.search(r'^set\s*Definitions=(.*)', line).groups()[0]
				
			except:
				pass
		#################
		print(definitions)
		src_dir = ''
		for file in files_to_compile:
			filename = file.split('/')[-1]

			if platform == 'win32':
				filename = file.split('\\')[-1]
			src_dir = file.split(filename)[0]
			
			with open(file) as f: cpp_text = f.readlines()
			for line in cpp_text:
				if ("#include" in line):
					pound_include = re.search(r'\w+\.(?:cpp|h)', line).group()
					if '<' not in line: ## check if not a external header
						with open(src_dir + pound_include) as f: header_text = f.readlines() ## open and check #include files  if they have more #includes in 'em
						for row in header_text:
							if ("#include \"" in row):
								# header = re.search(r'\w+\.(?:cpp|h)', row).group()
								header = re.search(r'\w+\.h', row).group()
								if header and (inc_flag+header) not in includes: includes.append(inc_flag+header)

					if '.cpp' in pound_include:
						dict_includes[pound_include] = includes
						temp_dict = {"directory": src_dir.replace('\\', '/'),
									"command": compiler + definitions + ' '  + clang_compiler_flags + ' ' + 
									' '.join(dict_includes[pound_include]) +  ' /FS -c ' + src_dir + pound_include,
									"file": src_dir.replace('\\', '/') + pound_include}

						compile_commands.append(temp_dict.copy())
					includes.append(inc_flag+pound_include)

			dict_includes[filename] = []
			[(dict_includes[filename].append(item)) for item in includes if '.cpp' not in item]
			
			temp_dict = {"directory": src_dir.replace('\\', '/'),
						 "command": compiler + definitions + ' ' + clang_compiler_flags + ' ' +
						  ' '.join(dict_includes[filename]) + ' /FS -c ' + src_dir + filename,
						 "file": src_dir.replace('\\', '/') + filename}

			compile_commands.append(temp_dict.copy())

		# print(compile_commands.copy())

		json_object = json.dumps(compile_commands, indent = 4)
		
		compile_commands_json = "/build/compile_commands.json"
		if platform == 'win32':
			compile_commands_json = "\\build\\compile_commands.json"

		# print(json_object)
		with open(proj_dir + compile_commands_json, "w") as outfile:
		    outfile.write(json_object)


class CompileCommandsListener(sublime_plugin.EventListener):
  	# def on_post_save_async(self, view):
  	# 	view.run_command('compile_json')

  	def on_load_project_async(self, window):
  		window.views()[0].run_command('compile_json')

  	def on_modified_async(self, view):
  		try:
	  		cursor_region = view.line(view.sel()[0])
	  		text = view.substr(cursor_region)
	  		if '#include' in text:
	  			view.run_command('compile_json')
  		except:
  			pass