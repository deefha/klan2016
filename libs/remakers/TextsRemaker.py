# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from PIL import Image
from CommonRemaker import CommonRemaker



class TextsRemaker(CommonRemaker):

	def __init__(self, issue, source, source_index):
		super(TextsRemaker, self).__init__(issue, source, source_index)

		self.CHARTABLE = u"ČüéďäĎŤčěĚĹÍľĺÄÁÉžŽôöÓůÚýÖÜŠĽÝŘťáíóúňŇŮÔšřŕŔ¼§▴▾                           Ë   Ï                 ß         ë   ï ±  ®©  °   ™"

		with open("%s%s/%s/%s.json" % (self.PATH_PHASE_REMAKED, self.issue.number, "fonts", 0), "r") as f:
			#content = f.read()
			lines = f.readlines() # TODO
			content = ''.join(lines) # TODO

			self.fonts_0 = ObjDict(content)

		self.PATTERN_PATH_TEXT = "%s%s" % (self.PATH_DATA_REMAKED, "%03d/")

		self.PATTERN_FILE_TEXT_ASSET = "%s%d.png"
		self.PATTERN_FILE_TEXT_PLAIN = "%s%d.txt"



	def export_assets(self):
		print "Export assets begin"

		for text_index, text in tqdm(self.meta_decompiled.data.texts.iteritems(), total=len(self.meta_decompiled.data.texts), desc="data.texts", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			if self.source.version == 1 or text.content:
				if self.source.version > 1:
					text = text.content

				self.items_total += 1
				status = True

				text_variant = 0

				path_text = self.PATTERN_PATH_TEXT % int(text_index)

				if not os.path.exists(path_text):
					os.makedirs(path_text)

				data_text = u""

				if text.linetable:
					lines_width = 0
					lines_height = 0
					lines = []

					for linetable_index, linetable in text.linetable.iteritems():
						line_width = 0
						line_height = text.linetable_meta[linetable_index].content.height
						line_pieces = []

						flag_bold = False
						flag_italic = False
						flag_link = False

						font_id = 1

						if linetable.content.pieces:
							for piece_index, piece in linetable.content.pieces.iteritems():
								# konec radku
								if piece.raw == 0:
									data_text += "\n"
								# font
								elif piece.raw == 1:
									font_id = piece.data.mode
									continue
								# bold
								elif piece.raw == 2:
									flag_bold = not flag_bold
									continue
								# italic
								elif piece.raw == 4:
									flag_italic = not flag_italic
									continue
								# obrazek
								elif piece.raw == 8:
									image_content_unpacked = []

									for row_index, row in piece.data.rows.iteritems():
										content_byte_count = None

										with open(row.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
											row_content = f.read()

										for content_byte in row_content[:-1]:
											if content_byte_count:
												image_content_unpacked.extend([content_byte] * content_byte_count)
												content_byte_count = None
											else:
												if ord(content_byte) > 192:
													content_byte_count = ord(content_byte) - 192
												else:
													image_content_unpacked.append(content_byte)

									image_content_unpacked = "".join(image_content_unpacked)

									with open(text.palettetable[str(piece.data.table)].content.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
										piece_colormap = f.read()

									i_piece = Image.frombytes("P", (piece.data.width, piece.data.height), image_content_unpacked)
									i_piece.putpalette(piece_colormap)
									i_piece.convert("RGBA")
									line_width += piece.data.width
									line_pieces.append(i_piece)
									continue
								# odkaz
								elif piece.raw == 9:
									flag_link = not flag_link
									continue
								# mezera
								elif piece.raw == 32:
									data_text += " "

									i_piece = Image.new("RGBA", (piece.data.length, line_height), (0, 0, 0, 0))
									line_width += piece.data.length
									line_pieces.append(i_piece)
								# bezny znak
								else:
									if piece.raw < 128:
										data_text += chr(piece.raw)
									else:
										data_text += self.CHARTABLE[piece.raw - 128]

									if str(piece.raw) in self.fonts_0.fonts[str(font_id)].normal.characters:
										if flag_bold:
											font_variant = "bold"
										elif flag_italic:
											font_variant = "italic"
										else:
											font_variant = "normal"

										if flag_link:
											font_variant += "_link"

										i_piece = Image.open(self.fonts_0.fonts[str(font_id)][font_variant].characters[str(piece.raw)].asset.replace("remaked://", self.PATH_PHASE_REMAKED))
										i_piece_width, i_piece_height = i_piece.size
										line_width += i_piece_width
										line_pieces.append(i_piece)

						i_line = Image.new("RGBA", (line_width, line_height), (0, 0, 0, 0))
						line_offset_x = 0

						for line_piece in line_pieces:
							line_piece_width, line_piece_height = line_piece.size
							i_line.paste(line_piece, (line_offset_x, 0))
							line_offset_x += line_piece_width

						if line_width > lines_width:
							lines_width = line_width
						lines_height += line_height
						lines.append(i_line)

					i_lines_temp = Image.new("RGBA", (lines_width, lines_height), (0, 0, 0, 0))
					lines_offset_y = 0

					for line in lines:
						line_width, line_height = line.size
						i_lines_temp.paste(line, (0, lines_offset_y))
						lines_offset_y += line_height

					i_lines = Image.new("RGBA", (lines_width, lines_height), (0, 0, 0, 255))
					i_lines = Image.alpha_composite(i_lines, i_lines_temp)
					i_lines.convert("RGBA")
					i_lines.save(self.PATTERN_FILE_TEXT_ASSET % (path_text, text_variant))

				with open(self.PATTERN_FILE_TEXT_PLAIN % (path_text, text_variant), "w") as f:
					f.write(data_text.encode("utf8", "replace"))

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1



	def fill_meta(self):
		super(TextsRemaker, self).fill_meta()

		self.meta_remaked.texts = ObjDict()

		for text_index, text in self.meta_decompiled.data.texts.iteritems():
			if self.source.version == 1 or text.content:
				if self.source.version > 1:
					text = text.content

				path_text = self.PATTERN_PATH_TEXT % int(text_index)

				data_text = ObjDict()

				if self.source.version == 1:
					data_text.name = self.meta_decompiled.fat[str(text_index)].name
				else:
					data_text.name = self.meta_decompiled.fat.offsets[str(text_index)].name

				data_text.variants = ObjDict()

				text_variant = 0
				data_variant = ObjDict()

				data_variant.asset = (self.PATTERN_FILE_TEXT_ASSET % (path_text, text_variant)).replace(self.PATH_PHASE_REMAKED, "remaked://")
				data_variant.plain = (self.PATTERN_FILE_TEXT_PLAIN % (path_text, text_variant)).replace(self.PATH_PHASE_REMAKED, "remaked://")

				data_variant.links = ObjDict()

				for link_index, link in text.linktable_meta.iteritems():
					linktable = text.linktable[str(link_index)]

					data_link = ObjDict()
					data_link.area = ObjDict()
					data_link.actions = ObjDict()

					data_link.area.topleft_x = link.content.topleft_x
					data_link.area.topleft_y = link.content.topleft_y
					data_link.area.bottomright_x = link.content.bottomright_x
					data_link.area.bottomright_y = link.content.bottomright_y

					for action_index, action in linktable.content.pieces.iteritems():
						data_action = ObjDict()

						data_action.type = action.mode
						data_action.params = ObjDict()

						if data_action.type == 4:
							data_action.params.content = action.data.textfile
							data_action.params.area = ObjDict()
							data_action.params.slider = ObjDict()

							data_action.params.area.topleft_x = action.data.topleft_x
							data_action.params.area.topleft_y = action.data.topleft_y
							data_action.params.area.width = action.data.width
							data_action.params.area.height = action.data.height

							data_action.params.slider.topleft_x = action.data.slider_topleft_x
							data_action.params.slider.topleft_y = action.data.slider_topleft_y

						elif data_action.type == 6:
							#data_linktable_content_piece.data.foo = linktable_content_piece.data.foo # TODO
							data_action.params.foo = ""

						elif data_action.type == 9:
							#data_linktable_content_piece.data.foo = linktable_content_piece.data.foo # TODO
							data_action.params.foo = ""

						elif data_action.type == 11:
							data_action.params.foo = action.data.foo

						elif data_action.type == 12:
							data_action.params.id = action.data.id
							data_action.params.foo = action.data.foo

						elif data_action.type == 13:
							data_action.params.id = action.data.id
							data_action.params.content = action.data.textfile

						elif data_action.type == 14:
							data_action.params.id = action.data.id
							data_action.params.value = action.data.value

						elif data_action.type == 20:
							data_action.params.content = action.data.textfile
							data_action.params.foo = action.data.foo

						elif data_action.type == 65535:
							data_action.params.foo = action.data.foo

						else:
							print "Unknown action type: %s (text_index=%s, link_index=%s)" % (action.mode, text_index, link_index)
							sys.exit()

						data_link.actions[str(action_index)] = data_action

					data_variant.links[str(link_index)] = data_link

				data_text.variants[str(text_variant)] = data_variant

				self.meta_remaked.texts[str(text_index)] = data_text
