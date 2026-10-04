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


def wait_until(check, title, lines, progress, hints=()):
    started = time.time()
    while True:
        ok, detail = check()
        if ok:
            return detail
        age = time.time() - started
        extra = list(lines)
        if LAST_EVENT:
            extra = ["✓ " + LAST_EVENT, ""] + extra
        if detail:
            extra += ["", detail]
        if hints:
            idx = min(len(hints), int(age // 45))
            if idx:
                extra += ["", "PISTA:", hints[idx - 1]]
        box(title, extra, progress)
        time.sleep(1)


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
    wait_until(lambda: (REC.is_dir(), None), "CONSOLA DE RECUPERACIÓN", [
        "MISIÓN: reconstruir el sistema y localizar su respaldo físico.",
        "Deja esta consola abierta. Ejecuta comandos en otras terminales.",
        "",
        "ORIENTARSE: pwd muestra dónde estás; ls lista el contenido.",
        "~ representa tu directorio personal; / inicia una ruta absoluta.",
        "mkdir crea directorios. Ejemplo: mkdir ensayo",
        "crea ensayo dentro del directorio en el que estás trabajando.",
        "",
        "APRENDER CON EL MANUAL: prueba man mkdir en otra terminal.",
        "Flechas: mover; espacio: avanzar; /palabra: buscar; n: siguiente.",
        "Pulsa q para salir del manual y volver a la terminal.",
        "Para ampliar: man pwd, man ls. No escribas las comas.",
        "",
        "PRIMER OBJETIVO: crea el directorio de recuperación:",
        f"    {REC}",
        "La consola avanzará cuando detecte ese directorio."
    ], 0.0, ["Piensa qué comando crea un directorio nuevo."])
    completed("DIRECTORIO DE RECUPERACIÓN DETECTADO")

    wait_until(has_dirs, "FASE 1 · RECONSTRUCCIÓN", [
        "mkdir admite varios nombres: mkdir uno dos crea dos carpetas.",
        "cd cambia de directorio; pwd permite comprobar dónde estás.",
        "Una ruta relativa se interpreta desde ese directorio actual.",
        "Para ampliar: man mkdir; para cd, ejecuta help cd en Bash.",
        "",
        "Reconstruye dentro de FIE_RECOVERY los tres módulos originales:",
        "",
        "    documentos/",
        "    informes/",
        "    sistema/",
        "Comprueba con ls: deben aparecer las tres carpetas en el destino."
    ], 0.10, ["Puedes crear varios directorios con mkdir."])
    completed("ESTRUCTURA BÁSICA RESTAURADA")

    wait_until(copied_state, "FASE 1 · RECUPERAR ESTADO", [
        "cp copia archivos sin borrar el original.",
        "Ejemplo: cp notas.txt copia.txt",
        "Primer argumento: origen. Segundo: destino y su nuevo nombre.",
        "Linux distingue estado.txt de Estado.txt: revisa las mayúsculas.",
        "Para ampliar: man cp. Puedes leer un texto con cat: man cat.",
        "",
        f"Origen:  {FRAG / 'estado.txt'}",
        f"Destino: {REC / 'sistema' / 'estado_inicial.txt'}",
        "",
        "Recupéralo conservando exactamente su contenido.",
        "Comprueba con cat la copia: cambia su nombre, no la información."
    ], 0.18, ["Necesitas copiar un fichero y cambiar su nombre en el destino."])
    completed("ESTADO INICIAL VERIFICADO")

    wait_until(docs_copied, "FASE 1 · DOCUMENTACIÓN", [
        "Un comodín permite seleccionar varios nombres de archivo.",
        "* representa cualquier secuencia de caracteres; ? uno solo.",
        "Ejemplo: ls *.txt lista los nombres terminados en .txt.",
        "Aquí el shell expande el patrón antes de ejecutar el comando.",
        "Para ampliar: man bash, busca /Pathname Expansion; q para salir.",
        "",
        "Recupera TODOS los documentos de texto del directorio fragmentos/.",
        "",
        f"Origen:  {FRAG}",
        f"Destino: {REC / 'documentos'}",
        "",
        "Los documentos válidos tienen extensión .txt",
        "Con ls en el destino verás las copias; los originales se conservan."
    ], 0.26, ["Los comodines permiten seleccionar muchos ficheros: piensa en *.txt"])
    completed("DOCUMENTACIÓN RECUPERADA")

    wait_until(obsolete_removed, "FASE 1 · DEPURACIÓN", [
        "rm elimina un archivo: rm copia.txt elimina esa copia.",
        "No lo envía a la papelera. Comprueba antes el nombre con ls.",
        "Para ampliar: man rm.",
        "",
        "El manifiesto marca una copia obsoleta que no debe conservarse:",
        "",
        f"    {REC / 'documentos' / 'estado_old.txt'}",
        "",
        "Elimínala del sistema reconstruido.",
        "Comprueba con ls: desaparece esa copia; las demás deben seguir."
    ], 0.34, ["rm elimina ficheros. Comprueba bien la ruta antes de usarlo."])
    completed("FASE 1 COMPLETADA")

    wait_until(system_files_ok, "FASE 2 · IDENTIFICACIÓN", [
        "/proc es un directorio virtual: el kernel ofrece datos del sistema.",
        "cat /proc/meminfo los muestra; cp permite guardar una instantánea.",
        "cpuinfo describe la CPU; meminfo, la memoria; version, el kernel.",
        "Los datos de memoria cambian: tu copia conserva un momento concreto.",
        "Para ampliar: man proc, man cat y man cp.",
        "",
        "Crea estas copias dentro de FIE_RECOVERY/sistema/:",
        "",
        "  cpu.txt      ← /proc/cpuinfo",
        "  memoria.txt  ← /proc/meminfo",
        "  version.txt  ← /proc/version",
        "",
        "Lee las copias con cat: MemTotal indica la memoria total en kB.",
        "En cpu.txt, model name identifica el modelo del procesador.",
        "La consola verificará automáticamente su contenido."
    ], 0.42, ["Los ficheros de /proc pueden copiarse igual que cualquier fichero de texto."])
    completed("EQUIPO IDENTIFICADO")
    unlock_odt()

    wait_until(dossier_read, "FASE 3 · EXPEDIENTE RECUPERADO", [
        "En otra terminal, entra en la carpeta del documento:",
        "  cd ~/FIE_RECOVERY/documentos",
        "",
        "Abre el informe que hay en esa carpeta:",
        "  libreoffice --writer Informe_Mantenimiento.odt",
        "--writer selecciona el procesador de textos de LibreOffice.",
        "Para ampliar: libreoffice --help.",
        "Lee la referencia y visita la URL del informe para descodificarla.",
        "Conserva la contraseña obtenida: la necesitarás al final.",
        "",
        "Cierra Writer para volver a la terminal y confirma la lectura:",
        "  touch ~/FIE_RECOVERY/sistema/expediente_leido.txt",
        "",
        "touch crea un archivo vacío; si existe, actualiza sus fechas.",
        "Aquí confirma tu lectura. Para ampliar: man touch.",
        "Esta pantalla permanecerá hasta que crees ese archivo."
    ], 0.57)
    completed("LECTURA DEL EXPEDIENTE CONFIRMADA")

    wait_until(grep_tutorial_ok, "FASE 4 · TUTORIAL: grep", [
        "grep busca líneas que coinciden con un patrón, sin editar el archivo.",
        'Ejemplo: grep "ERROR" archivo.log',
        '"ERROR" es el patrón; archivo.log es el archivo que se lee.',
        "Verás las líneas completas que contienen ERROR, respetando su orden.",
        "Para ampliar: man grep. /palabra busca; n repite; q sale.",
        "",
        "GUARDAR LA SALIDA: > redirige lo que iría a la pantalla.",
        'Ejemplo: grep "AVISO" archivo.log > avisos.txt',
        "Crea avisos.txt o sobrescribe su contenido; >> añade al final.",
        "Para ampliar: man bash, busca /REDIRECTION.",
        "",
        "TU RETO: guarda las líneas ERROR en:",
        f"    {REC / 'sistema' / 'errores.txt'}",
        "con las líneas ERROR de:",
        f"    {TUTORIAL / 'registro.log'}",
        "Combina la selección de líneas y su guardado en un archivo.",
        "Con > no verás esas líneas en pantalla: lee el resultado con cat."
    ], 0.60, ["Una posible forma empieza por: grep \"ERROR\" ... > ..."])
    completed("grep DOMINADO")

    wait_until(find_tutorial_ok, "FASE 4 · TUTORIAL: find", [
        "find recorre un directorio y sus subdirectorios buscando nombres.",
        'Ejemplo: find . -name "*.txt"',
        ". indica dónde empieza; -name filtra por el nombre del archivo.",
        '"*.txt" selecciona nombres que terminan en .txt.',
        "Las comillas evitan que el shell expanda *: find recibe el patrón.",
        "El resultado es una lista de rutas, no el contenido de los archivos.",
        "Para ampliar: man find. Busca /-name; q vuelve a la terminal.",
        "",
        "TU RETO: guarda la lista de rutas en:",
        f"    {REC / 'informes' / 'cifrados.txt'}",
        "Busca TODOS los .enc dentro de:",
        f"    {REPORTS}",
        "",
        "Guarda el resultado mediante >.",
        "Lee cifrados.txt con cat: contiene rutas, no copias de los .enc."
    ], 0.68, ["Cambia el punto del ejemplo por el directorio que quieres explorar."])
    completed("find DOMINADO")

    wait_until(pipe_tutorial_ok, "FASE 4 · TUTORIAL: PIPELINE", [
        "Una tubería | conecta la salida de un programa con otro.",
        'Ejemplo: grep "ERROR" archivo.log | wc -l',
        "1. grep selecciona las líneas que contienen ERROR.",
        "2. | entrega esas líneas a wc, sin crear un archivo intermedio.",
        "3. wc -l cuenta las líneas recibidas (-l significa líneas).",
        "Verás un número: no cuenta palabras ni todos los errores repetidos",
        "dentro de una misma línea, sino las líneas seleccionadas.",
        "Para ampliar: man wc; man bash, busca /Pipelines.",
        "| y > son operadores del shell: se explican en man bash.",
        "",
        "TU RETO: guarda el número de líneas ERROR en:",
        f"    {REC / 'sistema' / 'numero_errores.txt'}",
        "Archivo que debes analizar:",
        f"    {TUTORIAL / 'registro.log'}",
        "",
        "Combina grep, |, wc -l y >.",
        "Al leer la salida con cat, verás un número en vez de las líneas."
    ], 0.75, ["La tubería cuenta; la redirección final guarda ese número."])
    completed("TUTORIAL AVANZADO COMPLETADO")

    wait_until(boss_index_ok, "BOSS DIGITAL · ÍNDICE DAÑADO", [
        "Ya puedes trabajar sobre los registros reales.",
        "",
        f"Directorio: {LOGS}",
        "",
        "Existe una única referencia que contiene la marca:",
        "    FINAL_REPORT",
        "",
        "Localízala y guarda esa línea en:",
        f"    {REC / 'informes' / 'indice.txt'}",
        "",
        "Esta vez decide tú cómo combinar las herramientas aprendidas.",
        "Lee indice.txt con cat: la marca revela qué informe debes abrir.",
        "Para repasar: man grep, man find, man wc y man bash."
    ], 0.82, ["grep puede buscar el mismo texto en varios *.log"])
    completed("INFORME FINAL IDENTIFICADO: informe_01.enc")

    wait_until(final_ok, "FASE 5 · DESCIFRADO FINAL", [
        "Descifrar recupera el texto original usando la contraseña correcta.",
        "OpenSSL ofrece herramientas de cifrado; enc procesa este archivo.",
        "AES-256-CBC es el cifrado usado; PBKDF2 deriva la clave a partir",
        "de la contraseña. Las opciones deben coincidir con las del cifrado.",
        "-d descifra; -in indica el origen; -out el archivo que se creará.",
        "Para ampliar: man openssl y man openssl-enc.",
        "TU RETO: completa ARCHIVO y DESTINO con sus rutas reales:",
        "",
        "  openssl enc -d -aes-256-cbc -pbkdf2 \\",
        "    -in ARCHIVO \\",
        "    -out DESTINO",
        "\\ al final continúa el mismo comando en la línea siguiente.",
        "OpenSSL pedirá la contraseña de César; no se verá al escribirla.",
        "Archivo: informe_01.enc (consulta informes/cifrados.txt).",
        "",
        f"El destino debe ser: {REC / 'informes' / 'informe_final.txt'}",
        "El .enc se conserva; la nueva copia .txt contendrá texto legible."
    ], 0.90, [f"El archivo cifrado está en {REPORTS / 'informe_01.enc'}"])

    while True:
        box("RECUPERACIÓN DIGITAL COMPLETADA", [
            "✓ Estructura reconstruida",
            "✓ Sistema identificado",
            "✓ Expediente recuperado",
            "✓ Herramientas avanzadas utilizadas",
            "✓ Informe final descifrado",
            "",
            "El sistema digital está restaurado al 100 %.",
            "",
            "La consola ya no puede ayudarte.",
            "Lee ahora:",
            f"    {REC / 'informes' / 'informe_final.txt'}",
            "",
            "La última operación ocurre fuera del ordenador."
        ], 1.0, "Fin de la supervisión automática.")
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Consola detenida. Puedes volver a ejecutar ./iniciar.py para continuar.")
