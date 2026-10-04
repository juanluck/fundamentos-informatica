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


def box(title, lines, progress, footer=""):
    global LAST_SCROLL_SCREEN

    wrapped = []
    for raw in lines:
        for line in str(raw).splitlines() or [""]:
            wrapped.extend(
                textwrap.wrap(
                    line,
                    WIDTH - 2,
                    replace_whitespace=False,
                    break_on_hyphens=False,
                )
                or [""]
            )

    columns, rows = shutil.get_terminal_size((80, 40))

    # En ventanas pequeñas no borrar ni repetir cada segundo el texto que
    # el alumno está leyendo con el desplazamiento de su terminal.
    extra = 8 if footer else 6
    if columns < WIDTH + 2 or rows < len(wrapped) + extra:
        screen = (title, tuple(wrapped), progress, footer, columns, rows)
        if screen != LAST_SCROLL_SCREEN:
            print(f"\n--- {title} · {int(progress * 100)} % ---")
            print("La ventana es pequeña. Puedes desplazarte para leer todas las instrucciones.")
            print("\n".join(wrapped))
            if footer:
                print(footer)
            sys.stdout.flush()
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

    if footer:
        print("╠" + "─" * WIDTH + "╣")
        print("║" + ("  " + footer)[:WIDTH].ljust(WIDTH) + "║")

    print("╚" + "═" * WIDTH + "╝")
    sys.stdout.flush()


def render_screen(content, detail=None, hint=None, previous=None):
    """Construye una pantalla sin imponer una plantilla didáctica fija."""
    lines = []

    if previous:
        lines += ["✓ " + previous, ""]

    lines += list(content)

    if detail:
        lines += ["", "⚠ " + detail]

    if hint:
        lines += ["", "Pista: " + hint]

    return lines


def wait_until(check, title, content, progress, hints=(), footer=""):
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

        box(
            title,
            render_screen(content, detail, hint, LAST_EVENT),
            progress,
            footer,
        )
        time.sleep(1)


def display_path(path):
    """Mostrar ~ sin cambiar la ruta real utilizada por los validadores."""
    try:
        return str(Path("~") / path.relative_to(HOME))
    except ValueError:
        return str(path)


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
        return False, "Aún no existe la carpeta FIE_RECOVERY en tu directorio personal."

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
        return False, "Revisa las mayúsculas: los nombres de las tres carpetas deben estar en minúsculas."

    if missing:
        return False, "Todavía faltan estas carpetas: " + ", ".join(missing) + "."

    return True, None


def copied_state():
    dst = REC / "sistema" / "estado_inicial.txt"

    if not dst.exists():
        return False, "Aún no aparece estado_inicial.txt en la carpeta sistema."

    if not same_file(FRAG / "estado.txt", dst):
        return False, "La copia existe, pero su contenido no coincide con estado.txt. Revisa el archivo que has copiado."

    return True, None


def docs_copied():
    expected = {p.name for p in FRAG.glob("*.txt")}
    d = REC / "documentos"
    present = {p.name for p in d.glob("*.txt")} if d.exists() else set()
    missing = expected - present

    if missing:
        return False, f"Se han encontrado {len(expected) - len(missing)} de los {len(expected)} documentos .txt que debes copiar."

    return True, None


def obsolete_removed():
    p = REC / "documentos" / "estado_old.txt"
    return (
        not p.exists(),
        "La copia estado_old.txt sigue en documentos. Aún debes eliminarla." if p.exists() else None,
    )


def system_files_ok():
    s = REC / "sistema"
    cpu = text(s / "cpu.txt")
    mem = text(s / "memoria.txt")
    ver = text(s / "version.txt")

    ok_cpu = "model name" in cpu or "Processor" in cpu
    ok_mem = "MemTotal:" in mem and "MemFree:" in mem
    ok_ver = "Linux version" in ver

    pending = []
    if not ok_cpu:
        pending.append("cpu.txt")
    if not ok_mem:
        pending.append("memoria.txt")
    if not ok_ver:
        pending.append("version.txt")

    if pending:
        return False, "Todavía faltan archivos válidos: " + ", ".join(pending) + "."

    return True, None


def unlock_odt():
    dst = REC / "documentos" / "Informe_Mantenimiento.odt"
    if not dst.exists() and (DOCS / "Informe_Mantenimiento.odt").exists():
        shutil.copy2(DOCS / "Informe_Mantenimiento.odt", dst)


def dossier_read():
    # Confirmación de lectura desde otra terminal; no se intenta detectar
    # la apertura de Writer ni se solicita una respuesta dentro de Python.
    marker = REC / "sistema" / "expediente_leido.txt"
    return (
        marker.is_file(),
        "Puedes leer el documento sin prisa. Cuando termines, crea expediente_leido.txt para continuar.",
    )


def grep_tutorial_ok():
    src_lines = [
        l for l in text(TUTORIAL / "registro.log").splitlines()
        if "ERROR" in l
    ]
    out = REC / "sistema" / "errores.txt"
    got = text(out).splitlines()

    if got == src_lines:
        return True, None

    return False, "errores.txt aún no contiene exactamente las líneas con ERROR de registro.log."


def _normalize_find_output(line):
    raw = line.strip()
    if not raw:
        return None

    p = Path(raw).expanduser()

    # Acepta tanto rutas absolutas como salidas del tipo ./informes/fichero.enc
    # cuando la búsqueda se hace desde ~/escape_fie.
    if not p.is_absolute():
        raw = raw[2:] if raw.startswith("./") else raw
        p = PACKAGE / raw

    try:
        return p.resolve()
    except OSError:
        return p.absolute()


def find_tutorial_ok():
    out = REC / "informes" / "cifrados.txt"

    got = {
        p for p in (
            _normalize_find_output(line)
            for line in text(out).splitlines()
        )
        if p is not None
    }

    expected = {p.resolve() for p in PACKAGE.rglob("*.enc")}

    if got == expected and expected:
        return True, None

    return False, (
        f"La lista todavía no contiene correctamente los {len(expected)} archivos .enc "
        "localizados dentro de ~/escape_fie."
    )


def pipe_tutorial_ok():
    expected = sum(
        1 for l in text(TUTORIAL / "registro.log").splitlines()
        if "ERROR" in l
    )

    try:
        got = int(text(REC / "sistema" / "numero_errores.txt").strip())
    except ValueError:
        got = -1

    if got == expected:
        return True, None

    return False, "El recuento aún no es correcto o no está guardado en numero_errores.txt."


def boss_index_ok():
    target = "FINAL_REPORT=informe_01.enc"
    lines = [
        l.strip()
        for l in text(REC / "informes" / "indice.txt").splitlines()
        if l.strip()
    ]

    if lines == [target] or any(target in l for l in lines):
        return True, target

    return False, "La referencia al informe todavía no aparece en indice.txt."


def final_ok():
    p = REC / "informes" / "informe_final.txt"
    t = text(p)

    if "HE COMPLETADO EL RETO" in t and "mochila del profesor" in t:
        return True, None

    if p.exists():
        return False, "El archivo existe, pero no contiene el informe esperado. Revisa la contraseña y el archivo de origen."

    return False, "Todavía no se ha creado informe_final.txt en la carpeta informes."


def main():
    wait_until(
        lambda: (REC.is_dir(), "Aún no existe la carpeta FIE_RECOVERY en tu directorio personal."),
        "CONSOLA DE RECUPERACIÓN",
        [
            "Vamos a reconstruir un sistema dañado utilizando la terminal de Linux.",
            "",
            "Deja esta consola abierta y trabaja en otra terminal. Aquí iremos comprobando "
            "automáticamente lo que haces y avanzaremos cuando completes cada paso.",
            "",
            "Primero necesitamos un lugar donde trabajar.",
            "",
            "Crea en tu directorio personal una carpeta llamada:",
            f"  {display_path(REC)}",
            "",
            "Para crear una carpeta puedes utilizar mkdir.",
            "",
            "Si no recuerdas dónde estás, pwd muestra tu ubicación actual. "
            "~ representa tu directorio personal.",
        ],
        0.00,
        ["Puedes volver a tu directorio personal con cd ~."],
        "Trabaja en otra terminal; esta consola avanzará automáticamente.",
    )
    completed("La carpeta de recuperación ya está creada.")

    wait_until(
        has_dirs,
        "FASE 1 · RECONSTRUCCIÓN",
        [
            "Ya tenemos el espacio de trabajo.",
            "",
            f"Dentro de {display_path(REC)} crea estas tres carpetas:",
            "  documentos",
            "  informes",
            "  sistema",
            "",
            "Puedes crear varias carpetas con una sola orden mkdir, escribiendo sus nombres "
            "separados por espacios.",
            "",
            "Recuerda que Linux distingue entre mayúsculas y minúsculas.",
        ],
        0.10,
        ["Por ejemplo: mkdir fotos videos"],
    )
    completed("Las tres carpetas del proyecto están preparadas.")

    wait_until(
        copied_state,
        "FASE 1 · RECUPERAR ESTADO",
        [
            "Ahora vamos a recuperar el primer archivo.",
            "",
            "Copia:",
            f"  {display_path(FRAG / 'estado.txt')}",
            "",
            "en:",
            f"  {display_path(REC / 'sistema' / 'estado_inicial.txt')}",
            "",
            "Hasta ahora has trabajado con carpetas. Para copiar archivos utilizaremos cp.",
            "",
            "Su forma básica es:",
            "  cp ORIGEN DESTINO",
            "",
            "El archivo original se conserva y se crea una copia en el destino.",
            "En este caso, además, queremos que la copia tenga un nombre diferente.",
        ],
        0.18,
        ["En DESTINO debes escribir también el nuevo nombre: estado_inicial.txt"],
    )
    completed("La copia del estado inicial tiene el contenido correcto.")

    wait_until(
        docs_copied,
        "FASE 1 · DOCUMENTACIÓN",
        [
            "Necesitamos recuperar ahora todos los documentos de texto.",
            "",
            "Copia desde:",
            f"  {display_path(FRAG)}",
            "",
            "hasta:",
            f"  {display_path(REC / 'documentos')}",
            "",
            "todos los archivos cuyo nombre termine en .txt.",
            "",
            "No hace falta escribir sus nombres uno por uno.",
            "",
            "En la terminal, * funciona como comodín. Por ejemplo:",
            "  *.txt",
            "",
            "representa todos los nombres que terminan en .txt.",
            "",
            "Puedes probar primero el patrón con ls para ver qué archivos selecciona. "
            "Después utilízalo con cp.",
        ],
        0.26,
        ["Cuando cp recibe varios archivos, el último argumento debe ser una carpeta de destino."],
    )
    completed("Los documentos de texto ya se han recuperado.")

    wait_until(
        obsolete_removed,
        "FASE 1 · DEPURACIÓN",
        [
            "Entre los documentos recuperados hay una copia antigua que ya no necesitamos:",
            f"  {display_path(REC / 'documentos' / 'estado_old.txt')}",
            "",
            "Elimínala.",
            "",
            "Para borrar un archivo puedes utilizar:",
            "  rm ARCHIVO",
            "",
            "Ten cuidado: rm elimina el archivo directamente, no lo envía a la papelera.",
        ],
        0.34,
        ["Elimina la copia que está en documentos, no el archivo original de fragmentos."],
    )
    completed("La copia antigua se ha eliminado.")

    wait_until(
        system_files_ok,
        "FASE 2 · IDENTIFICACIÓN",
        [
            "Ahora necesitamos obtener información sobre el equipo en el que estamos trabajando.",
            "",
            "Linux mantiene información sobre el sistema dentro de /proc. Vamos a explorar parte de ella.",
            "",
            "Empieza mostrando la información del procesador:",
            "  cat /proc/cpuinfo",
            "",
            "cat muestra en la terminal el contenido de un archivo. En este caso aparecerá "
            "información sobre la CPU.",
            "",
            "También podemos consultar la memoria:",
            "  cat /proc/meminfo",
            "",
            "y la versión del sistema:",
            "  cat /proc/version",
            "",
            "Hasta ahora la información aparece en pantalla. Pero también podemos guardar "
            "la salida de un comando en un archivo utilizando >.",
            "",
            "Por ejemplo:",
            f"  cat /proc/cpuinfo > {display_path(REC / 'sistema' / 'cpu.txt')}",
            "",
            "En vez de mostrarse en pantalla, la información queda guardada en cpu.txt.",
            "",
            "Haz lo mismo para conservar:",
            "  información de la CPU      → cpu.txt",
            "  información de la memoria  → memoria.txt",
            "  versión del sistema        → version.txt",
            "",
            "dentro de:",
            f"  {display_path(REC / 'sistema')}",
            "",
            "También podríamos haber utilizado:",
            f"  cp /proc/cpuinfo {display_path(REC / 'sistema' / 'cpu.txt')}",
            "",
            "y obtendríamos el mismo contenido. Pero el mecanismo es diferente:",
            "",
            "  cp              copia un archivo.",
            "  cat ... > ...   guarda en un archivo la salida que un comando produciría en pantalla.",
            "",
            "Esta segunda idea nos será útil más adelante con otros comandos.",
        ],
        0.42,
        ["Sigue el mismo patrón: cat ORIGEN > DESTINO"],
    )
    completed("La información del equipo ya está guardada.")
    unlock_odt()

    wait_until(
        dossier_read,
        "FASE 3 · EXPEDIENTE RECUPERADO",
        [
            "Hemos recuperado un documento de mantenimiento:",
            f"  {display_path(REC / 'documentos' / 'Informe_Mantenimiento.odt')}",
            "",
            "Ábrelo y léelo con atención. Contiene información que necesitarás más adelante.",
            "",
            "Desde la terminal puedes abrirlo con LibreOffice:",
            f"  libreoffice --writer {display_path(REC / 'documentos' / 'Informe_Mantenimiento.odt')}",
            "",
            "El documento contiene una contraseña cifrada. Sigue las instrucciones que aparecen "
            "en él para recuperarla y guárdala.",
            "",
            "Cuando hayas terminado de leerlo, indica a la consola que puede continuar creando:",
            f"  {display_path(REC / 'sistema' / 'expediente_leido.txt')}",
            "",
            "Puedes crear un archivo vacío con:",
            "  touch ARCHIVO",
        ],
        0.57,
    )
    completed("Has confirmado la lectura del informe.")

    wait_until(
        grep_tutorial_ok,
        "FASE 4 · BUSCAR CON grep",
        [
            "Tenemos un registro:",
            f"  {display_path(TUTORIAL / 'registro.log')}",
            "",
            "y queremos extraer únicamente las líneas que contienen ERROR.",
            "",
            "grep es parecido a cat, pero permite buscar línea por línea y mostrar únicamente "
            "las líneas que contienen el texto que nos interesa.",
            "",
            "Por ejemplo:",
            '  grep "ERROR" archivo.log',
            "",
            "muestra las líneas de archivo.log que contienen ERROR.",
            "",
            "Pruébalo con registro.log.",
            "",
            "Cuando tengas el resultado correcto, guárdalo en:",
            f"  {display_path(REC / 'sistema' / 'errores.txt')}",
            "",
            "Ya sabes utilizar > para guardar en un archivo la salida de un comando.",
        ],
        0.60,
        [
            "Primero haz que grep muestre las líneas correctas. "
            "Después utiliza > para guardar esa salida."
        ],
    )
    completed("Las líneas de error se han guardado correctamente.")

    wait_until(
        find_tutorial_ok,
        "FASE 4 · LOCALIZAR CON find",
        [
            "Antes buscábamos texto dentro de un archivo.",
            "",
            "Ahora el problema es distinto: queremos localizar archivos sin tener que recorrer "
            "las carpetas una a una.",
            "",
            "find permite buscar archivos recorriendo un directorio y todos sus subdirectorios.",
            "",
            "Por ejemplo:",
            f'  find {display_path(PACKAGE)} -name "*.txt"',
            "",
            "significa:",
            f"  {display_path(PACKAGE)}   empieza a buscar aquí",
            "  -name            busca por nombre",
            '  "*.txt"          nombres terminados en .txt',
            "",
            "A diferencia de ls, que muestra el contenido de una carpeta concreta, find puede "
            "explorar toda la estructura que cuelga del directorio que le indiquemos.",
            "",
            "Busca dentro de:",
            f"  {display_path(PACKAGE)}",
            "",
            "todos los archivos terminados en .enc y guarda las rutas encontradas en:",
            f"  {display_path(REC / 'informes' / 'cifrados.txt')}",
            "",
            "Ya sabes utilizar > para guardar la salida de un comando.",
        ],
        0.68,
        [
            f'Parte de {display_path(PACKAGE)} y cambia el patrón "*.txt" por el tipo de archivo que buscas.'
        ],
    )
    completed("La lista de archivos cifrados está preparada.")

    wait_until(
        pipe_tutorial_ok,
        "FASE 4 · CONECTAR COMANDOS",
        [
            "Sabemos buscar las líneas que contienen ERROR.",
            "",
            "Ahora queremos saber cuántas son.",
            "",
            "Podríamos guardar primero las líneas en un archivo y contarlas después, pero Linux "
            "permite conectar directamente dos comandos.",
            "",
            "El símbolo | se llama tubería.",
            "",
            "Envía la salida del comando de la izquierda directamente al comando de la derecha.",
            "",
            "Ya conocemos la primera parte:",
            '  grep "ERROR" archivo.log',
            "",
            "Para contar líneas podemos utilizar:",
            "  wc -l",
            "",
            "Por tanto:",
            '  grep "ERROR" archivo.log | wc -l',
            "",
            "busca las líneas con ERROR y envía el resultado directamente a wc, que las cuenta.",
            "",
            "Hazlo con:",
            f"  {display_path(TUTORIAL / 'registro.log')}",
            "",
            "y guarda el número obtenido en:",
            f"  {display_path(REC / 'sistema' / 'numero_errores.txt')}",
            "",
            "Ya sabes cómo guardar la salida final.",
        ],
        0.75,
        ["Primero conecta grep con wc -l. Después utiliza > para guardar el resultado."],
    )
    completed("El recuento de líneas de error es correcto.")

    wait_until(
        boss_index_ok,
        "RETO FINAL · BUSCAR EL INFORME",
        [
            "Hasta ahora has aprendido a:",
            "  buscar texto con grep;",
            "  seleccionar varios archivos con *;",
            "  guardar resultados con >.",
            "",
            "Ahora tendrás que combinarlo sin una orden de ejemplo completa.",
            "",
            "En los registros de:",
            f"  {display_path(LOGS)}",
            "",
            "hay varios archivos .log.",
            "",
            "Busca entre ellos la línea que contiene:",
            "  FINAL_REPORT",
            "",
            "y guárdala en:",
            f"  {display_path(REC / 'informes' / 'indice.txt')}",
            "",
            "Esa línea te indicará cuál es el informe que necesitas.",
        ],
        0.82,
        ["*.log permite seleccionar todos los archivos de registro."],
    )
    completed("El informe que debes descifrar ya está identificado.")

    wait_until(
        final_ok,
        "FASE 5 · DESCIFRAR EL INFORME",
        [
            "La pista anterior identifica el archivo cifrado:",
            f"  {display_path(REPORTS / 'informe_01.enc')}",
            "",
            "Ahora debes descifrarlo utilizando la contraseña que recuperaste del documento "
            "de mantenimiento.",
            "",
            "Para ello vamos a utilizar openssl.",
            "",
            "La orden es:",
            "  openssl enc -d -aes-256-cbc -pbkdf2 \\",
            "    -in ARCHIVO_CIFRADO \\",
            "    -out ARCHIVO_DESCIFRADO",
            "",
            "En esta ocasión no necesitas aprender todas las opciones de OpenSSL.",
            "",
            "Solo debes saber que:",
            "  -d      descifra",
            "  -in     indica el archivo de entrada",
            "  -out    indica dónde guardar el resultado",
            "",
            "Utiliza como destino:",
            f"  {display_path(REC / 'informes' / 'informe_final.txt')}",
            "",
            "OpenSSL te pedirá la contraseña. Mientras la escribes no aparecerán caracteres "
            "en pantalla; es normal.",
        ],
        0.90,
        ["Introduce exactamente la contraseña que obtuviste en el documento de mantenimiento."],
    )

    final_content = [
        "Has terminado la recuperación en el ordenador.",
        "",
        "El informe final está en:",
        f"  {display_path(REC / 'informes' / 'informe_final.txt')}",
        "",
        "Ya sabes cómo mostrar el contenido de un archivo desde la terminal.",
        "",
        "Léelo.",
        "",
        "La última parte del reto ocurre fuera del ordenador.",
        "",
        "Antes de recuperar el objeto, pide autorización al profesor.",
    ]

    while True:
        box(
            "RECUPERACIÓN DIGITAL COMPLETADA",
            render_screen(
                final_content,
                previous="Has completado todos los pasos de recuperación en el ordenador.",
            ),
            1.0,
            "Lee el informe final para continuar el reto.",
        )
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Consola detenida. Puedes volver a ejecutar ./iniciar.py para continuar.")
