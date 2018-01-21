import os, sys

from objdict import ObjDict
from CommonDecompiler import CommonDecompiler



class ModsDecompiler(CommonDecompiler):

	PATTERN_PATH_MOD = "%s/mods/%04d/"
	PATTERN_PATH_MOD_PATTERNS = "%s/mods/%04d/patterns/"
	PATTERN_PATH_SAMPLE = "%s/samples/"

	PATTERN_FILE_MOD_PATTERN = "%s/mods/%04d/patterns/%04d.bin"
	PATTERN_FILE_SAMPLE = "%s/samples/%04d.bin"

	def fill_meta_data(self):
		super(ModsDecompiler, self).fill_meta_data()

		self.meta.data.names = ObjDict()

		for names_index, name in enumerate(self.library.data.names):
			#self.meta.data.names[str(names_index)] = name
			self.meta.data.names[str(names_index)] = ""

		self.meta.data.mods = ObjDict()

		for mod_index, mod in enumerate(self.library.data.mods):
			data_mod = ObjDict()
			data_mod.param_offset = mod.param_offset
			data_mod.content = ObjDict()

			if mod.content:
				print "Mod #%d: param_offset=%d, name='%s', count_positions=%d, count_patterns=%d, count_samples=%d" % (mod_index, mod.param_offset, mod.content.name, mod.content.count_positions, mod.content.count_patterns, mod.content.count_samples)

				path_mod = self.PATTERN_PATH_MOD % (self.PATH_BLOBS, mod_index)
				path_mod_patterns = self.PATTERN_PATH_MOD_PATTERNS % (self.PATH_BLOBS, mod_index)

				if not os.path.exists(path_mod):
					os.makedirs(path_mod)

				if not os.path.exists(path_mod_patterns):
					os.makedirs(path_mod_patterns)

				#data_mod.content.name = mod.content.name
				data_mod.content.name = ""
				data_mod.content.count_positions = mod.content.count_positions
				data_mod.content.count_patterns = mod.content.count_patterns
				data_mod.content.count_samples = mod.content.count_samples
				#data_mod.content.foo = mod.content.foo
				data_mod.content.foo = ""

				data_mod.content.data = ObjDict()
				data_mod.content.data.param_count_patterns = mod.content.data.param_count_patterns
				data_mod.content.data.positions = mod.content.data.positions
				data_mod.content.data.patterns = ObjDict()

				for pattern_index, pattern in enumerate(mod.content.data.patterns):
					file_pattern = self.PATTERN_FILE_MOD_PATTERN % (self.PATH_BLOBS, mod_index, pattern_index)

					data_mod.content.data.patterns[str(pattern_index)] = "blobs://%s/%s/mods/%04d/patterns/%04d.bin" % (self.issue, self.source, mod_index, pattern_index)

					print "\tPattern #%d" % pattern_index
					f = open(file_pattern, "wb")
					f.write(pattern)
					f.close

			else:
				print "Mod #%d: param_offset=%d, no content" % (mod_index, mod.param_offset)

			self.meta.data.mods[str(mod_index)] = data_mod

		self.meta.data.samples = ObjDict()

		for sample_index, sample in enumerate(self.library.data.samples):
			data_sample = ObjDict()
			data_sample.param_offset = sample.param_offset
			data_sample.content = ObjDict()

			if sample.content:
				print "Sample #%d: param_offset=%d" % (sample_index, sample.param_offset)

				path_sample = self.PATTERN_PATH_SAMPLE % (self.PATH_BLOBS)

				if not os.path.exists(path_sample):
					os.makedirs(path_sample)

				data_sample.content.data_size = sample.content.data_size
				#data_sample.content.foo = sample.content.foo
				data_sample.content.foo = ""

				data_sample.content.data = ObjDict()
				data_sample.content.data.param_data_size = sample.content.data.param_data_size

				file_sample = self.PATTERN_FILE_SAMPLE % (self.PATH_BLOBS, sample_index)

				data_sample.content.data.content = "blobs://%s/%s/samples/%04d.bin" % (self.issue, self.source, sample_index)

				print "\tContent"
				f = open(file_sample, "wb")
				f.write(sample.content.data.content)
				f.close

			else:
				print "Sample #%d: param_offset=%d, no content" % (sample_index, sample.param_offset)

			self.meta.data.samples[str(sample_index)] = data_sample



	def fill_meta_header(self):
		super(ModsDecompiler, self).fill_meta_header()

		self.meta.header2 = ObjDict()
		self.meta.header2.count_mods = self.library.header2.count_mods
		self.meta.header2.count_samples = self.library.header2.count_samples
		self.meta.header2.foo = self.library.header2.foo



	def fill_meta_fat(self):
		self.meta.fat_mods = ObjDict()
		self.meta.fat_mods.offsets = ObjDict()

		print "Mods count: %d" % self.library.header2.count_mods

		for offset_index, offset in enumerate(self.library.fat_mods.offsets):
			print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat_mods.offsets[str(offset_index)] = offset

		self.meta.fat_samples = ObjDict()
		self.meta.fat_samples.offsets = ObjDict()

		print "Samples count: %d" % self.library.header2.count_samples

		for offset_index, offset in enumerate(self.library.fat_samples.offsets):
			print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat_samples.offsets[str(offset_index)] = offset
