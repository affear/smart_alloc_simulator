"""
	The module for what is OUT of Openstack
"""

class User(object):
	"""docstring for User"""
	pass

class VM(object):
	"""docstring for VM"""
	pass

class PM(object):
	"""docstring for PM"""
	pass
		
class DB(object):
	"""docstring for DB"""
	pass

def _enum(**enums):
	return type('Enum', (), enums)
Metrics = _enum(VCPU='vcpu', RAM='ram', DISK='disk')
		