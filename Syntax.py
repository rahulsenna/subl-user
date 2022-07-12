# import sublime
# import sublime_plugin

# import os
# import threading
# import re
# from User.ruamel import yaml
# import json

# dir = 'w:\\cpp\\code\\'
# syntax_file = "C:\\Users\\AgentOfChaos\\AppData\\Roaming\\Sublime Text 3\\Packages\\User\\CMine.sublime-syntax"

# defaults = ['true', 'false', 'for']
# parameters = []
# variables = []
# macros = []
# structs = []
# types  = []

# struct_str = ''
# type_str = ''

# def GetTypeData(filename):
# 	with open(filename) as f:
# 	    content = f.readlines()

# 	for line in content:
# 		if ("#define" in line):
# 			try:
# 				macro = re.search("^(#define)\\s+(\\w+)", line)
# 				if macro.group(2) not in macros:
# 					macros.append(macro.group(2))
# 			except:
# 				pass
# 		if (re.match("struct", line)):
# 			try:
# 				struct = re.search("^(struct)\\s+(\\w+)", line)
# 				if struct.group(2) not in structs:
# 					structs.append(struct.group(2))
# 			except:
# 				pass
# 		if (re.match("typedef", line)):
# 			try:
# 				typedef = re.search("^typedef\\s*\\w+\\s+(\\w+)|^typedef\\s*\\w+\\((\\w+)\\)", line)
# 				if (typedef.groups()[0]):
# 					if typedef.groups()[0] not in types:
# 						types.append(typedef.groups()[0])
# 				else:
# 					if typedef.groups()[1] not in types:
# 						types.append(typedef.groups()[1])
# 			except:
# 				pass


# def GetAllTypeData():
# 	files = os.listdir(dir)

# 	for file in files:
# 		GetTypeData(dir+file)


# def AddVarsAndParametes(self, view):
#   		if view.syntax().name != "C++" and view.syntax().name != "C":
#   			return

# 	  	filename = str(view.file_name())
# 	  	GetTypeData(filename)
  		
#   		param_re = re.compile(r"(?<=\()(.*)(?=\n{)", re.S)
#   		varab_re = re.compile(r"(?<=\{)(.*)", re.S)

#   		regions = view.find_by_selector('meta.function')  		
#   		for region in regions:
#   			text = view.substr(region)

#   			params = []
#   			varabs = []
#   			try:
#   				param_text = str(param_re.search(text).groups()[0])
#   				# print("paramText: ", param_text)
#   				varab_text = str(varab_re.search(text).groups()[0])
#   				# print("varabText: ", varab_text)

#   				params = re.findall(r"(?<!\.|\d)(\w+)(?:,|\)|\s=)", param_text)
#   				# print("params: ", params)
#   				varabs = re.findall(r"(?:"+'|'.join(structs)+'|'.join(types)+r")\s*\*?\s*(\w+)(?!\,)(?!\))(?:(?:\s+=)|(?:;))", varab_text)
#   				# print("varabs: ", varabs)

#   			except:
#   				# print("!!!Exception: ", text[0:20])
#   				pass
  			
#   			if params:
#   				for param in params:
#   					if param:
#   						if param not in parameters and param not in defaults:
#   							parameters.append(param)
#   			if varabs:
#   				for varab in varabs:
#   					if varab:
#   						if varab not in variables and varab not in defaults:
#   							variables.append(varab)


#   		# print(parameters)
#   		# print(variables)


#   		with open(syntax_file) as file:
#   			data = yaml.round_trip_load(file, preserve_quotes=True)


#   		data['variables']['my_structs'] = "|".join(structs)
#   		data['variables']['my_types'] = "|".join(types)
#   		data['variables']['my_macros'] = "|".join(macros)
#   		data['variables']['my_parameters'] = "|".join(parameters)
#   		data['variables']['my_vars'] = "|".join(variables)
#   		with open(syntax_file, 'w') as file:
#   			file.write('%YAML 1.2\n---\n')
#   			yaml.dump(data,file, Dumper=yaml.RoundTripDumper)


# class SyntaxListener(sublime_plugin.EventListener):
  	
#   	def on_init(self, views):
#   		r1 = threading.Thread(target=GetAllTypeData, args=())
#   		r1.start()
  	
#   	def on_post_save_async(self, view):
#   		AddVarsAndParametes(self, view)

#   	def on_activated_async(self, view):
#   		AddVarsAndParametes(self, view)

#   	def on_modified_async(self, view):
#   		r1 = threading.Thread(target=lsp_semantic, args=(self, view))
#   		r1.start()
