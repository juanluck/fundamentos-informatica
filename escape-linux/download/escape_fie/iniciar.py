#!RUTA_PYTHON
# FIE · Operación Recuperación
# La primera línea debe ser completada por el alumnado con la salida de: which python3

from pathlib import Path
import hashlib
import os
import shutil
import sys
import time
import textwrap

PACKAGE = Path(__file__).resolve().parent
HOME = Path.home()
REC = HOME / "FIE_RECOVERY"
START = time.time()
WIDTH = 76
LAST_EVENT = ""
LAST_SCROLL_SCREEN = None

FRAG = PACKAGE / "fragmentos"
LOGS = PACKAGE / "registros"
TUTORIAL = PACKAGE / "tutorial"
REPORTS = PACKAGE / "informes"
DOCS = PACKAGE / "documentos"


def clear():
    print("\033[2J\033[H", end="")


def elapsed():
    s = int(time.time() - START)
    return f"{s // 60:02d}:{s % 60:02d}"


def bar(progress):
    n = 38
    k = max(0, min(n, round(progress * n)))
    return "█" * k + "░" * (n - k)


def box(title, lines, progress, footer="Esperando cambios en el sistema..."):
    global LAST_SCROLL_SCREEN
    wrapped = []
    for raw in lines:
        for line in str(raw).splitlines() or [""]:
            wrapped.extend(textwrap.wrap(line, WIDTH - 2, replace_whitespace=False,
                                         break_on_hyphens=False) or [""])
    columns, rows = shutil.get_terminal_size((80, 40))
    # En ventanas pequeñas no borrar ni repetir cada segundo el texto que
    # el alumno está leyendo con el desplazamiento de su terminal.
    if columns < WIDTH + 2 or rows < len(wrapped) + 9:
        screen = (title, tuple(wrapped), progress, footer, columns, rows)
        if screen != LAST_SCROLL_SCREEN:
            print(f"\n--- {title} · {int(progress * 100)} % ---")
            print("Ventana pequeña: desplázate para leer; las instrucciones se conservan.")
            print("\n".join(wrapped))
            print(footer, flush=True)
            LAST_SCROLL_SCREEN = screen
        return
    LAST_SCROLL_SCREEN = None
    clear()
    print("╔" + "═" * WIDTH + "╗")
    header = f" FIE-LAB // {title}"
    timer = f"{elapsed()} "
    print("║" + header.ljust(WIDTH - len(timer)) + timer + "║")
    print("╠" + "═" * WIDTH + "╣")
    pct = int(progress * 100)
    p = f"  PROGRESO  {bar(progress)}  {pct:3d}%"
    print("║" + p.ljust(WIDTH) + "║")
    print("║" + "".ljust(WIDTH) + "║")
    for part in wrapped:
        print("║" + ("  " + part).ljust(WIDTH) + "║")
    print("║" + "".ljust(WIDTH) + "║")
    print("╠" + "─" * WIDTH + "╣")
    print("║" + ("  " + footer)[:WIDTH].ljust(WIDTH) + "║")
    print("╚" + "═" * WIDTH + "╝")
    sys.stdout.flush()


def wait_until(check, title, content, progress, hints=()):
    started = time.time()
    while True:
        ok, detail = check()
        if ok:
            return detail
        age = time.time() - started
        hint = None
        if hints:
            idx = min(len(hints), int(age // 45))
            if idx:
                hint = hints[idx - 1]
        lines = render_lesson(content, detail, hint, LAST_EVENT)
        box(title, lines, progress)
        time.sleep(1)


def display_path(path):
    """Mostrar ~ sin cambiar la ruta real utilizada por los validadores."""
    try:
        return str(Path("~") / path.relative_to(HOME))
    except ValueError:
        return str(path)


def lesson(locations, task, explanation, verification, manuals):
    """Contenido de una pantalla, separado de su estado y presentación."""
    return dict(locations=locations, task=task, explanation=explanation,
                verification=verification, manuals=manuals)


def render_lesson(content, detail=None, hint=None, previous=None):
    """Objetivo primero; pistas en la ayuda y avisos automáticos en ESTADO."""
    lines = ["OBJETIVO", *content["task"], ""]
    for label, path in content["locations"]:
        lines += [label, "  " + display_path(path)]
    lines += ["", "CÓMO HACERLO", *content["explanation"]]
    if hint:
        lines += ["PISTA: " + hint]
    lines += [
        "", "COMPRUEBA", *content["verification"],
        "", "ESTADO", detail or "Esperando a que completes el objetivo.",
    ]
    if previous:
        lines += ["✓ Último avance: " + previous]
    return lines + ["", "PARA AMPLIAR", content["manuals"]]


def same_file(a, b):
    try:
        return hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest()
    except OSError:
        return False


def text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def completed(msg):
    # El aviso permanece en el siguiente objetivo, sin pantallas temporizadas.
    global LAST_EVENT
    LAST_EVENT = msg


def has_dirs():
    if not REC.exists():
        return False, f"No existe todavía: {REC}"
    needed = ["documentos", "informes", "sistema"]
    missing = [n for n in needed if not (REC / n).is_dir()]
    wrong_case = []
    try:
        names = {p.name for p in REC.iterdir() if p.is_dir()}
        for n in needed:
            if n not in names and any(x.lower() == n for x in names):
                wrong_case.append(n)
    except OSError:
        pass
    if wrong_case:
        return False, "Hay un nombre con mayúsculas/minúsculas incorrectas. Linux las distingue."
    if missing:
        return False, "Faltan: " + ", ".join(missing)
    return True, None


def copied_state():
    dst = REC / "sistema" / "estado_inicial.txt"
    if not dst.exists():
        return False, "Aún no se ha detectado estado_inicial.txt"
    if not same_file(FRAG / "estado.txt", dst):
        return False, "estado_inicial.txt existe, pero su contenido no coincide con estado.txt"
    return True, None


def docs_copied():
    expected = {p.name for p in FRAG.glob("*.txt")}
    d = REC / "documentos"
    present = {p.name for p in d.glob("*.txt")} if d.exists() else set()
    missing = expected - present
    if missing:
        return False, f"Documentos .txt recuperados: {len(expected)-len(missing)}/{len(expected)}"
    return True, None


def obsolete_removed():
    p = REC / "documentos" / "estado_old.txt"
    return (not p.exists(), "estado_old.txt continúa en documentos/" if p.exists() else None)


def system_files_ok():
    s = REC / "sistema"
    cpu = text(s / "cpu.txt")
    mem = text(s / "memoria.txt")
    ver = text(s / "version.txt")
    ok_cpu = "model name" in cpu or "Processor" in cpu
    ok_mem = "MemTotal:" in mem and "MemFree:" in mem
    ok_ver = "Linux version" in ver
    pending = []
    if not ok_cpu: pending.append("cpu.txt ← /proc/cpuinfo")
    if not ok_mem: pending.append("memoria.txt ← /proc/meminfo")
    if not ok_ver: pending.append("version.txt ← /proc/version")
    if pending:
        return False, "Pendiente: " + " | ".join(pending)
    return True, None


def unlock_odt():
    dst = REC / "documentos" / "Informe_Mantenimiento.odt"
    if not dst.exists() and (DOCS / "Informe_Mantenimiento.odt").exists():
        shutil.copy2(DOCS / "Informe_Mantenimiento.odt", dst)


def dossier_read():
    # Confirmación de lectura desde otra terminal; no se intenta detectar
    # la apertura de Writer ni se solicita una respuesta dentro de Python.
    return (REC / "sistema" / "expediente_leido.txt").is_file(), None


def grep_tutorial_ok():
    src_lines = [l for l in text(TUTORIAL / "registro.log").splitlines() if "ERROR" in l]
    out = REC / "sistema" / "errores.txt"
    got = text(out).splitlines()
    if got == src_lines:
        return True, None
    return False, "Genera sistema/errores.txt con las líneas que contienen ERROR."


def find_tutorial_ok():
    out = REC / "informes" / "cifrados.txt"
    got = {Path(l.strip()).name for l in text(out).splitlines() if l.strip()}
    expected = {p.name for p in REPORTS.glob("*.enc")}
    if got == expected and expected:
        return True, None
    return False, f"cifrados.txt debe listar los {len(expected)} ficheros .enc del paquete."


def pipe_tutorial_ok():
    expected = sum(1 for l in text(TUTORIAL / "registro.log").splitlines() if "ERROR" in l)
    try:
        got = int(text(REC / "sistema" / "numero_errores.txt").strip())
    except ValueError:
        got = -1
    if got == expected:
        return True, None
    return False, "numero_errores.txt debe contener únicamente el número de líneas ERROR."


def boss_index_ok():
    target = "FINAL_REPORT=informe_01.enc"
    lines = [l.strip() for l in text(REC / "informes" / "indice.txt").splitlines() if l.strip()]
    if lines == [target] or any(target in l for l in lines):
        return True, target
    return False, "Busca FINAL_REPORT en los registros y guarda el resultado en informes/indice.txt."


def final_ok():
    p = REC / "informes" / "informe_final.txt"
    t = text(p)
    if "HE COMPLETADO EL RETO" in t and "mochila del profesor" in t:
        return True, None
    if p.exists():
        return False, "informe_final.txt existe, pero no parece haberse descifrado correctamente."
    return False, "Esperando informe_final.txt..."


def main():
    wait_until(lambda: (REC.is_dir(), None), "CONSOLA DE RECUPERACIÓN", lesson(
        [("UBICACIÓN QUE DEBES CREAR", REC)],
        ["Reconstruye el sistema para localizar el respaldo físico.",
         "Primero crea el directorio indicado. Trabaja en otra terminal."],
        ["mkdir ensayo crea una carpeta llamada ensayo en el directorio actual.",
         "pwd muestra dónde estás; ls lista el contenido; ~ es tu HOME.",
         "Consulta man mkdir: flechas/espacio para avanzar, /palabra para buscar,",
         "n para la siguiente coincidencia y q para salir del manual."],
        ["Debe aparecer FIE_RECOVERY en tu HOME. La consola lo detectará."],
        "man mkdir, man pwd y man ls. Ejecuta cada consulta por separado."
    ), 0.0, ["Piensa qué comando crea un directorio nuevo."])
    completed("DIRECTORIO DE RECUPERACIÓN DETECTADO")

    wait_until(has_dirs, "FASE 1 · RECONSTRUCCIÓN", lesson(
        [("UBICACIÓN DONDE DEBES CREAR LAS CARPETAS", REC)],
        ["Crea dentro de esa ubicación: documentos/, informes/ y sistema/."],
        ["mkdir uno dos crea dos carpetas; cd cambia el directorio de trabajo.",
         "Una ruta relativa se interpreta desde el directorio actual.",
         "Linux distingue mayúsculas y minúsculas: sistema no es Sistema."],
        ["Usa pwd para orientarte y ls para comprobar que están las tres."],
        "man mkdir; para cd, utiliza help cd en Bash."
    ), 0.10, ["Puedes crear varios directorios con mkdir."])
    completed("ESTRUCTURA BÁSICA RESTAURADA")

    wait_until(copied_state, "FASE 1 · RECUPERAR ESTADO", lesson(
        [("ORIGEN · de dónde partimos", FRAG / "estado.txt"),
         ("DESTINO · dónde debe quedar", REC / "sistema" / "estado_inicial.txt")],
        ["Copia el archivo del origen al destino con el nuevo nombre."],
        ["cp notas.txt copia.txt conserva el original y crea una copia.",
         "Primer argumento: origen. Segundo: destino y su nuevo nombre.",
         "Revisa las mayúsculas: estado.txt no es Estado.txt."],
        ["Lee la copia con cat: cambia su nombre, no la información."],
        "man cp y man cat."
    ), 0.18, ["Necesitas copiar un fichero y cambiar su nombre en el destino."])
    completed("ESTADO INICIAL VERIFICADO")

    wait_until(docs_copied, "FASE 1 · DOCUMENTACIÓN", lesson(
        [("ORIGEN · de dónde partimos", FRAG),
         ("DESTINO · dónde debe quedar", REC / "documentos")],
        ["Copia TODOS los archivos .txt del origen al directorio de destino."],
        ["* representa cualquier secuencia de caracteres; ? uno solo.",
         "Ejemplo: ls *.txt lista los nombres terminados en .txt.",
         "El shell expande el patrón antes de ejecutar el comando."],
        ["Con ls en el destino verás las copias; los originales se conservan."],
        "man cp; man bash, busca /Pathname Expansion."
    ), 0.26, ["Los comodines permiten seleccionar muchos ficheros: piensa en *.txt"])
    completed("DOCUMENTACIÓN RECUPERADA")

    wait_until(obsolete_removed, "FASE 1 · DEPURACIÓN", lesson(
        [("ARCHIVO QUE DEBES ELIMINAR", REC / "documentos" / "estado_old.txt")],
        ["Elimina esta copia obsoleta del sistema reconstruido."],
        ["rm copia.txt elimina ese archivo; no lo envía a la papelera.",
         "Comprueba el nombre con ls antes de eliminarlo."],
        ["Con ls verás que desaparece solo esa copia; las demás deben seguir."],
        "man rm."
    ), 0.34, ["rm elimina ficheros. Comprueba bien la ruta antes de usarlo."])
    completed("FASE 1 COMPLETADA")

    wait_until(system_files_ok, "FASE 2 · IDENTIFICACIÓN", lesson(
        [("ORIGEN · de dónde partimos", Path("/proc")),
         ("DESTINO · dónde debe quedar", REC / "sistema")],
        ["Copia estos archivos, conservando la correspondencia de nombres:",
         "cpuinfo → cpu.txt; meminfo → memoria.txt; version → version.txt."],
        ["/proc es virtual: el kernel ofrece datos sobre el sistema.",
         "cat muestra esos datos; cp guarda una instantánea.",
         "La CPU, la memoria y la versión del kernel documentan el equipo."],
        ["Lee las copias con cat: MemTotal da la memoria total en kB;",
         "model name identifica la CPU. La memoria varía con el tiempo."],
        "man proc, man cat y man cp."
    ), 0.42, ["Los ficheros de /proc pueden copiarse igual que cualquier fichero de texto."])
    completed("EQUIPO IDENTIFICADO")
    unlock_odt()

    wait_until(dossier_read, "FASE 3 · EXPEDIENTE RECUPERADO", lesson(
        [("DOCUMENTO QUE DEBES ABRIR", REC / "documentos" / "Informe_Mantenimiento.odt"),
         ("CONFIRMACIÓN DE LECTURA", REC / "sistema" / "expediente_leido.txt")],
        ["Lee el documento y usa su URL para descodificar la referencia.",
         "Conserva la contraseña obtenida para el descifrado final."],
        ["En otra terminal, entra en la carpeta y abre Writer:",
         "  cd ~/FIE_RECOVERY/documentos",
         "  libreoffice --writer Informe_Mantenimiento.odt",
         "--writer selecciona el procesador de textos de LibreOffice."],
        ["Cuando tengas la contraseña, cierra Writer y confirma la lectura:",
         "  touch ~/FIE_RECOVERY/sistema/expediente_leido.txt",
         "touch crea el archivo vacío; si existe, actualiza sus fechas.",
         "La pantalla permanece hasta que exista esa confirmación."],
        "libreoffice --help y man touch."
    ), 0.57)
    completed("LECTURA DEL EXPEDIENTE CONFIRMADA")

    wait_until(grep_tutorial_ok, "FASE 4 · TUTORIAL: grep", lesson(
        [("ORIGEN · de dónde partimos", TUTORIAL / "registro.log"),
         ("DESTINO · dónde debe quedar", REC / "sistema" / "errores.txt")],
        ["Selecciona las líneas ERROR del origen y guárdalas en el destino."],
        ['grep "ERROR" archivo.log busca el patrón ERROR en archivo.log.',
         "Muestra las líneas completas coincidentes, en su orden original.",
         'grep "AVISO" archivo.log > avisos.txt guarda la salida en un archivo.',
         "> crea o sobrescribe el destino; >> añade al final. No edita el origen."],
        ["Con > la salida ya no aparece en pantalla: lee el destino con cat.",
         "Debe contener las líneas ERROR, no un recuento de ellas."],
        "man grep; man bash, busca /REDIRECTION. q sale del manual."
    ), 0.60, ['Una posible forma empieza por: grep "ERROR" ... > ...'])
    completed("grep DOMINADO")

    wait_until(find_tutorial_ok, "FASE 4 · TUTORIAL: find", lesson(
        [("ORIGEN · directorio que debes explorar", REPORTS),
         ("DESTINO · dónde debe quedar la lista", REC / "informes" / "cifrados.txt")],
        ["Busca TODOS los .enc dentro del origen y guarda sus rutas en el destino."],
        ['find . -name "*.txt" recorre el directorio actual y sus subdirectorios.',
         ". indica dónde empieza; -name filtra por nombre; *.txt es el patrón.",
         "Las comillas evitan que el shell expanda *: find recibe el patrón.",
         "El resultado es una lista de rutas. Guárdala mediante >."],
        ["Lee cifrados.txt con cat: contiene rutas, no copias de los .enc."],
        "man find. Busca /-name; q vuelve a la terminal."
    ), 0.68, ["Cambia el punto del ejemplo por el directorio que quieres explorar."])
    completed("find DOMINADO")

    wait_until(pipe_tutorial_ok, "FASE 4 · TUTORIAL: PIPELINE", lesson(
        [("ORIGEN · de dónde partimos", TUTORIAL / "registro.log"),
         ("DESTINO · dónde debe quedar", REC / "sistema" / "numero_errores.txt")],
        ["Cuenta las líneas ERROR del origen y guarda el número en el destino."],
        ['Ejemplo: grep "ERROR" archivo.log | wc -l',
         "1. grep selecciona las líneas que contienen ERROR.",
         "2. | entrega esas líneas a wc, sin crear un archivo intermedio.",
         "3. wc -l cuenta las líneas recibidas; añade > para guardar el número.",
         "| y > son operadores del shell; -l indica que se cuentan líneas."],
        ["cat debe mostrar un número, no las líneas ni el número de palabras.",
         "Si ERROR aparece dos veces en una línea, esa línea se cuenta una vez."],
        "man wc; man bash, busca /Pipelines."
    ), 0.75, ["La tubería cuenta; la redirección final guarda ese número."])
    completed("TUTORIAL AVANZADO COMPLETADO")

    wait_until(boss_index_ok, "BOSS DIGITAL · ÍNDICE DAÑADO", lesson(
        [("ORIGEN · registros que debes investigar", LOGS),
         ("DESTINO · dónde debe quedar", REC / "informes" / "indice.txt")],
        ["Localiza la única línea con FINAL_REPORT y guárdala en el destino."],
        ["Ya puedes trabajar sobre los registros reales.",
         "Decide cómo combinar las herramientas aprendidas para extraer la línea."],
        ["Lee indice.txt con cat: la marca revela qué informe debes descifrar."],
        "man grep, man find, man wc y man bash."
    ), 0.82, ["grep puede buscar el mismo texto en varios *.log"])
    completed("INFORME FINAL IDENTIFICADO: informe_01.enc")

    wait_until(final_ok, "FASE 5 · DESCIFRADO FINAL", lesson(
        [("ORIGEN · archivo cifrado", REPORTS / "informe_01.enc"),
         ("DESTINO · archivo descifrado", REC / "informes" / "informe_final.txt")],
        ["Descifra el origen usando la contraseña obtenida con César."],
        ["OpenSSL enc procesa el archivo; -d descifra; -in es el origen;",
         "-out es el destino. AES-256-CBC cifra y PBKDF2 deriva la clave.",
         "Completa ARCHIVO y DESTINO con las rutas indicadas arriba:",
         "  openssl enc -d -aes-256-cbc -pbkdf2 \\",
         "    -in ARCHIVO \\",
         "    -out DESTINO",
         "\\ al final continúa el comando. La contraseña no se verá al teclearla."],
        ["El .enc se conserva y el nuevo .txt contiene texto legible."],
        "man openssl y man openssl-enc."
    ), 0.90, ["Utiliza la ruta de ORIGEN para -in y la de DESTINO para -out."])

    while True:
        box("RECUPERACIÓN DIGITAL COMPLETADA", render_lesson(lesson(
            [("DOCUMENTO QUE DEBES LEER", REC / "informes" / "informe_final.txt")],
            ["Lee el informe: la última operación ocurre fuera del ordenador."],
            ["cat muestra el contenido de un archivo de texto en la terminal.",
             "El sistema está restaurado: estructura, equipo, expediente e informe."],
            ["Sigue las instrucciones del documento para localizar el respaldo.",
             "Solicita autorización al profesor antes de recuperar el objeto."],
            "man cat."
        ), detail="✓ Recuperación digital completada. Continúa con el profesor."),
            1.0, "Fin de la supervisión automática.")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Consola detenida. Puedes volver a ejecutar ./iniciar.py para continuar.")
