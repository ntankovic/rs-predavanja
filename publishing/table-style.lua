-- Shared table typography and alternating body rows in PDF output.
function Meta(meta)
  if FORMAT:match('latex') then
    local headers = meta['header-includes'] or pandoc.MetaList({})
    headers:insert(pandoc.MetaBlocks({pandoc.RawBlock('latex',
      '\\usepackage{colortbl}\n\\definecolor{courseRowGray}{gray}{0.95}')}))
    meta['header-includes'] = headers
  end
  return meta
end

function Table(tbl)
  for _, row in ipairs(tbl.head.rows) do
    for _, cell in ipairs(row.cells) do
      cell.contents = cell.contents:walk({
        Plain = function(b) return pandoc.Plain({pandoc.Strong(b.content)}) end,
        Para = function(b) return pandoc.Para({pandoc.Strong(b.content)}) end
      })
    end
  end
  if FORMAT:match('latex') then
    local index = 0
    for _, body in ipairs(tbl.bodies) do
      for _, row in ipairs(body.body) do
        index = index + 1
        if index % 2 == 0 then
          for _, cell in ipairs(row.cells) do
            local first = cell.contents[1]
            if first and (first.t == 'Plain' or first.t == 'Para') then
              first.content:insert(1, pandoc.RawInline('latex', '\\cellcolor{courseRowGray}'))
            end
          end
        end
      end
    end
  end
  if FORMAT:match('latex') then
    -- Struts add breathing room above and below each cell's text, including
    -- wrapped paragraphs inside Pandoc's minipages.
    local function pad_rows(rows)
      for _, row in ipairs(rows) do
        for _, cell in ipairs(row.cells) do
          local first, last = cell.contents[1], cell.contents[#cell.contents]
          if first and (first.t == 'Plain' or first.t == 'Para') then
            first.content:insert(1, pandoc.RawInline('latex', '\\rule{0pt}{1.35em}'))
          end
          if last and (last.t == 'Plain' or last.t == 'Para') then
            last.content:insert(pandoc.RawInline('latex', '\\rule[-0.55em]{0pt}{0.55em}'))
          end
        end
      end
    end
    pad_rows(tbl.head.rows)
    for _, body in ipairs(tbl.bodies) do
      pad_rows(body.head)
      pad_rows(body.body)
    end
    pad_rows(tbl.foot.rows)
    return {
      pandoc.RawBlock('latex', '\\begingroup\\small\\setlength{\\tabcolsep}{8pt}'),
      tbl,
      pandoc.RawBlock('latex', '\\endgroup')
    }
  end
  return tbl
end
