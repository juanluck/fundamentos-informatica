local labels = {
  ["concepto-clave"] = "Concepto clave",
  ["importante"] = "Importante",
  ["ejemplo"] = "Ejemplo",
  ["para-saber-mas"] = "Para saber más",
  ["autoevaluacion"] = "Autoevaluación",
  ["video"] = "Vídeo",
  ["recurso"] = "Recurso externo",
  ["objetivos"] = "Objetivos",
  ["resumen"] = "Resumen",
  ["solucion"] = "Solución"
}

local difficulty = {
  ["1"] = "● Básico",
  ["2"] = "●● Intermedio",
  ["3"] = "●●● Avanzado"
}

local function has_class(div, class_name)
  for _, c in ipairs(div.classes) do
    if c == class_name then return true end
  end
  return false
end

local function prepend_label(div, text)
  local kicker = pandoc.Span({pandoc.Str(text)}, pandoc.Attr("", {"component-kicker"}))
  table.insert(div.content, 1, pandoc.Para({kicker}))
end

local function exercise_header(div, kind)
  local number = div.attributes["numero"] or ""
  local title = div.attributes["titulo"] or ""
  local level = div.attributes["dificultad"] or ""

  local label = kind
  if number ~= "" then label = label .. " " .. number end

  local meta = pandoc.Div({}, pandoc.Attr("", {"exercise-meta"}))
  table.insert(meta.content, pandoc.Para({
    pandoc.Span({pandoc.Str(label)}, pandoc.Attr("", {"exercise-label"})),
    pandoc.Space(),
    pandoc.Span({pandoc.Str(difficulty[level] or "")}, pandoc.Attr("", {"difficulty-badge"}))
  }))

  table.insert(div.content, 1, meta)
  if title ~= "" then
    table.insert(div.content, 2, pandoc.Div({pandoc.Para({pandoc.Str(title)})}, pandoc.Attr("", {"exercise-title"})))
  end

  div.attributes["numero"] = nil
  div.attributes["titulo"] = nil
  div.attributes["dificultad"] = nil
end

function Div(div)
  if has_class(div, "ejercicio") then
    exercise_header(div, "Ejercicio")
    return div
  end

  if has_class(div, "tarea") then
    exercise_header(div, "Tarea")
    return div
  end

  for class_name, label in pairs(labels) do
    if has_class(div, class_name) then
      prepend_label(div, label)
      return div
    end
  end

  return div
end
