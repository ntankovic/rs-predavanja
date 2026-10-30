-- Explicit, stable lecture.definition numbers shared by chapter and slides.
local label = 'Definition'

local function metadata(meta)
  if pandoc.utils.stringify(meta.lang or ''):match('^hr') then label = 'Definicija' end
  local headers = meta['header-includes'] or pandoc.MetaList({})
  if FORMAT:match('latex') then
    headers:insert(pandoc.MetaBlocks({pandoc.RawBlock('latex',
      '\\definecolor{definitionRed}{RGB}{166,32,44}\n\\definecolor{definitionBackground}{RGB}{255,245,245}\n\\newsavebox{\\courseDefinitionBox}')}))
  elseif FORMAT:match('html') or FORMAT:match('revealjs') then
    headers:insert(pandoc.MetaBlocks({pandoc.RawBlock('html', [[
<style>
.definition { border: 2px solid #a6202c; border-left-width: 10px;
  background: #fff5f5; padding: 0.7em 0.9em; margin: 1em 0;
  border-radius: 5px; color: inherit; text-align: left; }
.definition > .definition-heading { color: #a6202c; font-weight: 700; margin: 0 0 0.5em; }
.definition > :last-child { margin-bottom: 0; }
</style>]] )}))
  end
  meta['header-includes'] = headers
  return meta
end

local function definition(div)
  if not div.classes:includes('definition') then return nil end
  local number = div.attributes.number
  if not number or not number:match('^%d+%.%d+$') then
    error('Definition blocks require number="lecture.definition", for example number="1.1".')
  end
  local heading = label .. ' ' .. number
  if FORMAT:match('latex') then
    local blocks = pandoc.List({pandoc.RawBlock('latex', [[
\par\medskip\noindent\begingroup
\setlength{\fboxsep}{10pt}\setlength{\fboxrule}{1pt}
\sbox{\courseDefinitionBox}{\fcolorbox{definitionRed}{definitionBackground}{%
\begin{minipage}{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}
]])})
    blocks:insert(pandoc.RawBlock('latex', '{\\color{definitionRed}\\bfseries ' .. heading .. '}\\par\\smallskip'))
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock('latex', '\\end{minipage}}}\\usebox{\\courseDefinitionBox}\\kern-\\wd\\courseDefinitionBox\\rlap{\\color{definitionRed}\\rule[-\\dp\\courseDefinitionBox]{5pt}{\\dimexpr\\ht\\courseDefinitionBox+\\dp\\courseDefinitionBox\\relax}}\\kern\\wd\\courseDefinitionBox\\endgroup\\par\\medskip'))
    return blocks
  end
  div.content:insert(1, pandoc.Div({pandoc.Para({pandoc.Str(heading)})},
                                  pandoc.Attr('', {'definition-heading'})))
  return div
end

return {{Meta = metadata}, {Div = definition}}
