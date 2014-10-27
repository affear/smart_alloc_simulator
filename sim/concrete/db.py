from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext	.declarative import declarative_base
from sqlalchemy.orm import sessionmaker	
from sqlalchemy import create_engine


Base = declarative_base()

class Host(Base):
	""""Class that declares the compute_node table which simulates the 
		compute_nodes table in nova db; it includes only fields useful for the simulation.
	"""

	__tablename__ = "compute_node"

	id = Column(Integer, primary_key=True)

	#Base metrics (virtual CPUs, RAM, Disk) with their usage counterpart
	vcpus = Column(Integer, nullable=False)
	memory_mb = Column(Integer, nullable=False)
	local_gb = Column(Integer, nullable=False)
	vcpus_used = Column(Integer, nullable=False)
	memory_mb_used = Column(Integer, nullable=False)
	local_gb_used = Column(Integer, nullable=False)

	#Hypervisor info
	hypervisor_type = Column(Text, nullable=False)
	hypervisor_version = Column(Integer, nullable=False)

	#CPU info (Json)
	cpu_info = Column(String(250), nullable=False)
	
	#Number of VMs running on the host
	running_vms = Column(Integer, nullable=True)

	#Hostname
	hypervisor_hostname = Column(Text, nullable=False)

	#List of supported instances
	supported_instances = Column(Text(), nullable=True)

def db_init(self):
	""""Creates the DB"""
	engine = create_engine('sqlite:///compute_node.db')
	Base.metadata.create_all(engine)


def db_populate(self):
	"""Populates the DB"""
	Base.metadata.bind = engine

	DBSession = sessionmaker(bind=engine)

	session = DBSession()

	new_host = Host(vcpus=12, memory_mb=16000, local_gb=500, vcpus_used=3, memory_mb_used=6656, local_gb_used=60, hypervisor_type="QEMU", hypervisor_version=2000000, cpu_info='{"vendor": "Intel", "model": "SandyBridge", "arch": "x86_64", "features": ["ssse3", "pge", "avx", "clflush", "sep", "syscall", "vme", "dtes64", "tsc", "xsave", "vmx", "xtpr", "cmov", "pcid", "est", "pat", "monitor", "smx", "lm", "msr", "nx", "fxsr", "tm", "sse4.1", "pae", "sse4.2", "pclmuldq", "acpi", "tsc-deadline", "mmx", "osxsave", "cx8", "mce", "mtrr", "rdtscp", "ht", "dca", "lahf_lm", "pdcm", "mca", "pdpe1gb", "apic", "sse", "pse", "ds", "pni", "tm2", "aes", "sse2", "ss", "pbe", "de", "fpu", "cx16", "pse36", "ds_cpl", "popcnt", "x2apic"], "topology": {"cores": 6, "threads": 2, "sockets": 1}}',running_vms=2, hypervisor_hostname="compute1", supported_instances='[["alpha", "qemu", "hvm"], ["armv7l", "qemu", "hvm"], ["cris", "qemu", "hvm"], ["i686", "qemu", "hvm"], ["i686", "kvm", "hvm"], ["lm32", "qemu", "hvm"], ["m68k", "qemu", "hvm"], ["microblaze", "qemu", "hvm"], ["microblazeel", "qemu", "hvm"], ["mips", "qemu", "hvm"], ["mipsel", "qemu", "hvm"], ["mips64", "qemu", "hvm"], ["mips64el", "qemu", "hvm"], ["ppc", "qemu", "hvm"], ["ppc64", "qemu", "hvm"], ["ppcemb", "qemu", "hvm"], ["s390x", "qemu", "hvm"], ["sh4", "qemu", "hvm"], ["sh4eb", "qemu", "hvm"], ["sparc", "qemu", "hvm"], ["sparc64", "qemu", "hvm"], ["unicore32", "qemu", "hvm"], ["x86_64", "qemu", "hvm"], ["x86_64", "kvm", "hvm"], ["xtensa", "qemu", "hvm"], ["xtensaeb", "qemu", "hvm"]]')
	session.add(new_host)
	session.commit()


#CRUD Operations






