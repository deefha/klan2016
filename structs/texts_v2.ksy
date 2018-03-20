meta:
  id: klan_texts_v2
  file-extension: lib
  title: KLAN texts library v2
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/texty.html

seq:
  - id: header
    type: t_header
  - id: fat
    type: t_fat
  - id: data
    type: t_data

types:
  t_fat:
    seq:
      - id: count
        type: u2
      - id: offsets
        type: t_fat_offset
        repeat: expr
        repeat-expr: 200

  t_fat_offset:
    seq:
      - id: name
        size: 9
      - id: offset_1
        type: u4
      - id: offset_2
        type: u4
      - id: offset_3
        type: u4
      - id: offset_4
        type: u4

  t_data:
    instances:
      texts:
        type: t_text(_parent.fat.offsets[_index].offset_1, _parent.fat.offsets[_index].offset_2 - _parent.fat.offsets[_index].offset_1)
        repeat: expr
        repeat-expr: 200

  t_text:
    params:
      - id: param_offset
        type: u4
      - id: param_length
        type: u4
    instances:
      content:
        type: t_text_content
        pos: param_offset
        size: param_length
        if: param_offset != 0

  t_text_content:
    instances:
      offset_linktable:
        pos: _io.size - 4
        type: u4
      count_linktable:
        pos: _io.size - 8
        type: u4
      offset_linktable_meta:
        value: _io.size - 8 - (20 * count_linktable)
      linktable_meta:
        type: t_linktable_meta(offset_linktable_meta + 20 * _index)
        repeat: expr
        repeat-expr: count_linktable
        if: count_linktable != 0
      linktable:
        type:
          switch-on: _index
          cases:
            (count_linktable - 1): t_linktable(linktable_meta[_index].content.offset, offset_linktable_meta - linktable_meta[_index].content.offset)
            _: t_linktable(linktable_meta[_index].content.offset, linktable_meta[_index + 1].content.offset - linktable_meta[_index].content.offset)
        repeat: expr
        repeat-expr: count_linktable
        if: count_linktable != 0
      count_linetable_meta:
        pos: offset_linktable - 52
        type: u4
      offset_linetable_meta:
        value: offset_linktable - 52 - (count_linetable_meta * 17) - 17
      linetable_meta:
        type: t_linetable_meta(offset_linetable_meta + 17 * _index)
        repeat: expr
        repeat-expr: count_linetable_meta
        if: count_linetable_meta != 0
      count_palettetable:
        pos: offset_linetable_meta - 1
        type: u1
      offset_palettetable:
        value: offset_linetable_meta - 1 - (count_palettetable * 768)
      palettetable:
        type: t_palettetable(offset_palettetable + 768 * _index)
        repeat: expr
        repeat-expr: count_palettetable
        if: count_palettetable != 0
      linetable:
        type:
          switch-on: _index
          cases:
            (count_linetable_meta - 1): t_linetable(linetable_meta[_index].content.offset, offset_palettetable - linetable_meta[_index].content.offset)
            _: t_linetable(linetable_meta[_index].content.offset, linetable_meta[_index + 1].content.offset - linetable_meta[_index].content.offset)
        repeat: expr
        repeat-expr: count_linetable_meta
        if: count_linetable_meta != 0

  t_linktable_meta:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_linktable_meta_content
        pos: param_offset

  t_linktable_meta_content:
    seq:
      - id: topleft_x
        type: u4
      - id: topleft_y
        type: u4
      - id: bottomright_x
        type: u4
      - id: bottomright_y
        type: u4
      - id: offset
        type: u4

  t_linktable:
    params:
      - id: param_offset
        type: u4
      - id: param_length
        type: u4
    instances:
      content:
        pos: param_offset
        size: param_length

  t_linetable_meta:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_linetable_meta_content
        pos: param_offset

  t_linetable_meta_content:
    seq:
      - id: offset
        type: u4
      - id: height
        type: u1
      - id: top
        type: u2
      - id: foo
        size: 10

  t_palettetable:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        size: 768
        pos: param_offset

  t_linetable:
    params:
      - id: param_offset
        type: u4
      - id: param_length
        type: u4
    instances:
      content:
        pos: param_offset
        size: param_length