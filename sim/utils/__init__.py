def class_for_name(class_path):
	"""Returns the class given its path as a string"""
	mod_path = '.'.join(class_path.split('.')[0:-1])
	class_name = class_path.split('.')[-1]
	mod = __import__(mod_path)
	components = mod_path.split('.')
	for comp in components[1:]:
		mod = getattr(mod, comp)
	clazz = getattr(mod, class_name)
	return clazz