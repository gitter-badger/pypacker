"""Virtual Router Redundancy Protocol."""

from .. import pypacker

class VRRP(pypacker.Packet):
	__hdr__ = (
		("vtype", "B", 0x21),
		("vrid", "B", 0),
		("priority", "B", 0),
		("count", "B", 0),
		("atype", "B", 0),
		("advtime", "B", 0),
		("_sum", "H", 0),	# _sum = sum
		)

	def __get_v(self):
		return self.vtype >> 4
	def __set_v(self, v):
		self.vtype = (self.vtype & ~0xf) | (v << 4)
	v = property(__get_v, __set_v)

	def __get_type(self):
		return self.vtype & 0xf
	def __set_type(self, v):
		self.vtype = (self.vtype & ~0xf0) | (v & 0xf)
	type = property(__get_type, __set_type)

	def __get_sum(self):
		if self.__needs_checksum_update():
			self.__calc_sum()
		return self._sum
	def __set_sum(self, value):
		self._sum = value
		self._sum_ud = True
	sum = property(__get_sum, __set_sum)


	def _unpack(self, buf):
		#l = []
		## fix: https://code.google.com/p/pypacker/issues/attachmentText?id=87
		#off = 0
		#for off in range(0, 4 * self.count, 4):
		#	l.append(self.data[off:off+4])
		#self.addrs = l
		#self.auth = self.data[off+4:]
		#self.data = ''
		pypacker.Packet._unpack(self, buf)

	def bin(self):
		if self.__needs_checksum_update():
			self.__calc_sum()
		return pypacker.Packet.bin(self)

	def __calc_sum(self):
		self.sum = 0
		object.__setattr__(self, "_sum", pypacker.in_cksum(pypacker.Packet.bin()) )

	def __needs_checksum_update(self):
		if hasattr(self, "_sum_ud"):
			return False
		return self._changed()
