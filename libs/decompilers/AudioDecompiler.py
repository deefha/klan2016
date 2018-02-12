# common imports
import os, sys, datetime
from objdict import ObjDict
from tqdm import tqdm

# specific imports
from CommonDecompiler import CommonDecompiler



class AudioDecompiler(CommonDecompiler):

	PATTERN_PATH_WAVE = "%s%04d/"

	PATTERN_FILE_CONTENT = "%s%04d/content.bin"

	PATTERN_DECOMPILED_CONTENT = "decompiled://%s/%s/%s/%04d/content.bin"

	def fill_meta_data(self):
		super(AudioDecompiler, self).fill_meta_data()

		self.meta.data.waves = ObjDict()

		for wave_index, wave in enumerate(tqdm(self.library.data.waves, desc="data.waves", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			data_wave = ObjDict()
			data_wave.param_offset = wave.param_offset
			data_wave.content = ObjDict()

			if wave.content:
				#print "Wave #%d: param_offset=%d, data_size=%d, wave_size=%d, mode=%d" % (wave_index, wave.param_offset, wave.content.data_size, wave.content.wave_size, wave.content.mode)

				file_content = self.PATTERN_FILE_CONTENT % (self.PATH_DATA, wave_index)

				path_wave = self.PATTERN_PATH_WAVE % (self.PATH_DATA, wave_index)

				if not os.path.exists(path_wave):
					os.makedirs(path_wave)

				data_wave.content.data_size = wave.content.data_size
				data_wave.content.wave_size = wave.content.wave_size
				data_wave.content.mode = wave.content.mode
				data_wave.content.foo_1 = wave.content.foo_1
				data_wave.content.foo_2 = wave.content.foo_2
				data_wave.content.data = ObjDict()
				data_wave.content.data.param_data_size = wave.content.data.param_data_size

				if self.source.version == 1:
					data_wave.content.data.title = ""
				else:
					data_wave.content.data.title = ""
					#data_wave.content.data.title = wave.content.data.title

				data_wave.content.data.content = self.PATTERN_DECOMPILED_CONTENT % (self.issue.number, self.source.library, self.source_index, wave_index)

				#print "\tContent"
				with open(file_content, "wb") as f:
					f.write(wave.content.data.content)

			#else:
				#print "Wave #%d: param_offset=%d, no content" % (wave_index, wave.param_offset)

			self.meta.data.waves[str(wave_index)] = data_wave
