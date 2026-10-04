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


def box(title, lines, progress, footer="Trabaja en otra terminal; esta consola comprobará tus cambios."):
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
            print("La ventana es pequeña. Puedes desplazarte para leer todas las instrucciones.")
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
        "", "ESTADO", detail or "El objetivo está pendiente. La consola avanzará cuando lo completes.",
    ]
    if previous:
        lines += ["✓ " + previous]
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
        return False, f"Se han encontrado {len(expected)-len(missing)} de los {len(expected)} documentos .txt que debes copiar."
    return True, None


def obsolete_removed():
    p = REC / "documentos" / "estado_old.txt"
    return (not p.exists(), "La copia estado_old.txt sigue en documentos. Aún debes eliminarla." if p.exists() else None)


def system_files_ok():
    s = REC / "sistema"
    cpu = text(s / "cpu.txt")
    mem = text(s / "memoria.txt")
    ver = text(s / "version.txt")
    ok_cpu = "model name" in cpu or "Processor" in cpu
    ok_mem = "MemTotal:" in mem and "MemFree:" in mem
    ok_ver = "Linux version" in ver
    pending = []
    if not ok_cpu: pending.append("cpu.txt")
    if not ok_mem: pending.append("memoria.txt")
    if not ok_ver: pending.append("version.txt")
    if pending:
        return False, "Faltan copias válidas de estos archivos: " + ", ".join(pending) + "."
    return True, None


def unlock_odt():
    dst = REC / "documentos" / "Informe_Mantenimiento.odt"
    if not dst.exists() and (DOCS / "Informe_Mantenimiento.odt").exists():
        shutil.copy2(DOCS / "Informe_Mantenimiento.odt", dst)


def dossier_read():
    # Confirmación de lectura desde otra terminal; no se intenta detectar
    # la apertura de Writer ni se solicita una respuesta dentro de Python.
    return ((REC / "sistema" / "expediente_leido.txt").is_file(),
            "Puedes leer sin prisa. Falta crear el archivo que confirma la lectura.")


def grep_tutorial_ok():
    src_lines = [l for l in text(TUTORIAL / "registro.log").splitlines() if "ERROR" in l]
    out = REC / "sistema" / "errores.txt"
    got = text(out).splitlines()
    if got == src_lines:
        return True, None
    return False, "errores.txt aún no contiene las líneas esperadas. Revisa la búsqueda y la ruta de destino."


def find_tutorial_ok():
    out = REC / "informes" / "cifrados.txt"
    got = {Path(l.strip()).name for l in text(out).splitlines() if l.strip()}
    expected = {p.name for p in REPORTS.glob("*.enc")}
    if got == expected and expected:
        return True, None
    return False, f"La lista todavía no incluye correctamente los {len(expected)} archivos .enc. Revisa la búsqueda."


def pipe_tutorial_ok():
    expected = sum(1 for l in text(TUTORIAL / "registro.log").splitlines() if "ERROR" in l)
    try:
        got = int(text(REC / "sistema" / "numero_errores.txt").strip())
    except ValueError:
        got = -1
    if got == expected:
        return True, None
    return False, "El recuento aún no es correcto o no está guardado en numero_errores.txt."


def boss_index_ok():
    target = "FINAL_REPORT=informe_01.enc"
    lines = [l.strip() for l in text(REC / "informes" / "indice.txt").splitlines() if l.strip()]
    if lines == [target] or any(target in l for l in lines):
        return True, target
    return False, "La referencia al informe todavía no aparece en indice.txt. Revisa la búsqueda y dónde guardas el resultado."


def final_ok():
    p = REC / "informes" / "informe_final.txt"
    t = text(p)
    if "HE COMPLETADO EL RETO" in t and "mochila del profesor" in t:
        return True, None
    if p.exists():
        return False, "El archivo de destino existe, pero no contiene el informe esperado. Revisa la contraseña y el archivo de origen."
    return False, "Todavía no se ha creado informe_final.txt en la carpeta informes."


def main():
    wait_until(lambda: (REC.is_dir(), "Aún no existe la carpeta FIE_RECOVERY."),
               "CONSOLA DE RECUPERACIÓN", lesson(
        [("UBICACIÓN QUE DEBES CREAR", REC)],
        ["Crea en tu directorio personal la carpeta FIE_RECOVERY. Allí irás reconstruyendo los archivos del proyecto."],
        ["Deja esta consola abierta y trabaja en otra terminal. El comando mkdir crea una carpeta; por ejemplo:",
         "  mkdir ensayo",
         "La carpeta se crea donde estés situado. Puedes comprobar esa ubicación con pwd y cambiarla con cd. El símbolo ~ representa tu directorio personal."],
        ["Utiliza ls para comprobar que FIE_RECOVERY aparece dentro de tu directorio personal."],
        "Consulta man mkdir. Usa las flechas para leer, /palabra para buscar y q para salir."
    ), 0.0, ["Puedes volver a tu directorio personal con cd ~ antes de crear la carpeta."])
    completed("La carpeta de recuperación ya está creada.")

    wait_until(has_dirs, "FASE 1 · RECONSTRUCCIÓN", lesson(
        [("UBICACIÓN DONDE DEBES CREAR LAS CARPETAS", REC)],
        ["Crea tres carpetas dentro de FIE_RECOVERY: documentos, informes y sistema."],
        ["Entra con cd en FIE_RECOVERY y utiliza mkdir para crear las tres carpetas. Puedes hacerlo en una sola orden, indicando sus nombres separados por espacios.",
         "Escribe los nombres en minúsculas: para Linux, sistema y Sistema son carpetas distintas."],
        ["Ejecuta ls dentro de FIE_RECOVERY. Deben aparecer las tres carpetas, cada una con su nombre correcto."],
        "Consulta man mkdir. Para saber más sobre cd, utiliza help cd."
    ), 0.10, ["Por ejemplo, mkdir fotos videos crea dos carpetas en la ubicación actual."])
    completed("Las tres carpetas del proyecto están preparadas.")

    wait_until(copied_state, "FASE 1 · RECUPERAR ESTADO", lesson(
        [("ORIGEN · de dónde partimos", FRAG / "estado.txt"),
         ("DESTINO · dónde debe quedar", REC / "sistema" / "estado_inicial.txt")],
        ["Copia estado.txt en la carpeta sistema y guarda la copia con el nombre estado_inicial.txt."],
        ["El comando cp necesita dos rutas: la del archivo original y la de la copia que quieres crear. Por ejemplo:",
         "  cp notas.txt copia.txt",
         "Este comando crea copia.txt con el mismo contenido y conserva notas.txt. Adapta el ejemplo a las rutas indicadas arriba."],
        ["Lee la copia con cat seguido de su ruta. Debe contener el mismo texto que estado.txt, aunque tenga otro nombre."],
        "Consulta man cp y man cat para conocer sus opciones."
    ), 0.18, ["En la segunda ruta debes incluir el nuevo nombre del archivo."])
    completed("La copia del estado inicial tiene el contenido correcto.")

    wait_until(docs_copied, "FASE 1 · DOCUMENTACIÓN", lesson(
        [("ORIGEN · de dónde partimos", FRAG),
         ("DESTINO · dónde debe quedar", REC / "documentos")],
        ["Copia todos los archivos terminados en .txt de fragmentos a documentos. Conserva sus nombres."],
        ["Puedes seleccionar varios archivos con un comodín. El asterisco * representa cualquier secuencia de caracteres; por eso, *.txt selecciona los nombres que terminan en .txt.",
         "Prueba ls con ese patrón para ver qué archivos selecciona. Después utiliza cp con el mismo patrón y la carpeta de destino."],
        ["Consulta con ls la carpeta documentos: deben aparecer las copias de todos los .txt. Los archivos originales deben seguir en fragmentos."],
        "Consulta man cp. El manual man bash también explica los comodines."
    ), 0.26, ["Cuando copias varios archivos, el destino debe ser una carpeta que ya exista."])
    completed("Los documentos de texto ya se han recuperado.")

    wait_until(obsolete_removed, "FASE 1 · DEPURACIÓN", lesson(
        [("ARCHIVO QUE DEBES ELIMINAR", REC / "documentos" / "estado_old.txt")],
        ["Elimina estado_old.txt de la carpeta documentos: es una versión antigua que ya no necesitamos."],
        ["El comando rm elimina el archivo cuya ruta le indiques. Por ejemplo, rm copia.txt borra ese archivo de la carpeta actual.",
         "Revisa bien el nombre antes de ejecutarlo: rm no envía los archivos a la papelera."],
        ["Vuelve a listar documentos con ls. estado_old.txt debe haber desaparecido y los demás archivos deben seguir allí."],
        "Consulta man rm para conocer las opciones de borrado."
    ), 0.34, ["Borra la copia de documentos, no el archivo original de fragmentos."])
    completed("La copia antigua se ha eliminado.")

    wait_until(system_files_ok, "FASE 2 · IDENTIFICACIÓN", lesson(
        [("ORIGEN · de dónde partimos", Path("/proc")),
         ("DESTINO · dónde debe quedar", REC / "sistema")],
        ["Guarda información sobre el equipo copiando estos tres archivos con los nombres indicados:",
         "  cpuinfo → cpu.txt    meminfo → memoria.txt    version → version.txt"],
        ["Linux ofrece información sobre el equipo en /proc. Sus archivos describen, entre otras cosas, el procesador, la memoria y la versión del sistema.",
         "Utiliza cp para guardar una copia de cada uno en sistema. Así conservarás los datos disponibles en ese momento."],
        ["Lee las copias con cat. En memoria.txt, MemTotal indica la memoria total en kB; en cpu.txt, busca el modelo del procesador."],
        "Consulta man proc para saber más sobre estos archivos."
    ), 0.42, ["Cada copia necesita su propia orden cp, con el archivo de origen y el nuevo nombre en el destino."])
    completed("Las copias de la información del equipo están preparadas.")
    unlock_odt()

    wait_until(dossier_read, "FASE 3 · EXPEDIENTE RECUPERADO", lesson(
        [("DOCUMENTO QUE DEBES ABRIR", REC / "documentos" / "Informe_Mantenimiento.odt"),
         ("CONFIRMACIÓN DE LECTURA", REC / "sistema" / "expediente_leido.txt")],
        ["Abre el informe recuperado y sigue sus instrucciones para obtener la contraseña. Guárdala: la necesitarás más adelante."],
        ["En otra terminal, entra en documentos y abre el informe con Writer, el procesador de textos de LibreOffice:",
         "  cd ~/FIE_RECOVERY/documentos",
         "  libreoffice --writer Informe_Mantenimiento.odt"],
        ["Cuando hayas obtenido la contraseña, cierra Writer y ejecuta:",
         "  touch ~/FIE_RECOVERY/sistema/expediente_leido.txt",
         "touch crea un archivo vacío que confirma que has terminado. Esta pantalla te esperará hasta que lo crees."],
        "Consulta libreoffice --help y man touch si necesitas más información."
    ), 0.57)
    completed("Has confirmado la lectura del informe.")

    wait_until(grep_tutorial_ok, "FASE 4 · BUSCAR CON grep", lesson(
        [("ORIGEN · de dónde partimos", TUTORIAL / "registro.log"),
         ("DESTINO · dónde debe quedar", REC / "sistema" / "errores.txt")],
        ["Guarda en errores.txt las líneas de registro.log que contienen la palabra ERROR."],
        ["grep busca un texto dentro de un archivo y muestra las líneas en las que aparece. Puedes guardar esas líneas usando >, como en este ejemplo:",
         '  grep "ERROR" archivo.log > seleccion.txt',
         "Aquí se buscan las líneas con ERROR en archivo.log y se guardan en seleccion.txt. Si el destino ya existe, > sustituye su contenido."],
        ["Lee errores.txt con cat. Debe contener las líneas completas con ERROR, en el mismo orden que en el registro."],
        "Consulta man grep. En man bash encontrarás la explicación de >."
    ), 0.60, ["Sustituye los dos nombres del ejemplo por las rutas de ORIGEN y DESTINO."])
    completed("Las líneas de error se han guardado correctamente.")

    wait_until(find_tutorial_ok, "FASE 4 · LOCALIZAR CON find", lesson(
        [("ORIGEN · directorio que debes explorar", REPORTS),
         ("DESTINO · dónde debe quedar la lista", REC / "informes" / "cifrados.txt")],
        ["Localiza los archivos terminados en .enc y guarda sus rutas en cifrados.txt."],
        ["find busca archivos en una carpeta y sus subcarpetas. Por ejemplo:",
         '  find . -name "*.txt"',
         "El punto indica la carpeta actual y -name permite buscar por nombre. Las comillas hacen que find reciba el patrón *.txt sin que la terminal lo sustituya antes por una lista de archivos.",
         "Busca los .enc en la carpeta de ORIGEN y guarda la lista con >."],
        ["Al abrir cifrados.txt con cat, debes ver una ruta por línea."],
        "Consulta man find para explorar otras formas de buscar archivos."
    ), 0.68, ["Cambia el punto por la carpeta de ORIGEN y el patrón por el de los archivos que buscas."])
    completed("La lista de archivos cifrados está preparada.")

    wait_until(pipe_tutorial_ok, "FASE 4 · CONECTAR COMANDOS", lesson(
        [("ORIGEN · de dónde partimos", TUTORIAL / "registro.log"),
         ("DESTINO · dónde debe quedar", REC / "sistema" / "numero_errores.txt")],
        ["Cuenta cuántas líneas contienen ERROR y guarda el resultado en numero_errores.txt."],
        ["El símbolo |, llamado tubería, envía la salida de un comando al siguiente. En este ejemplo, grep selecciona las líneas y wc -l las cuenta:",
         '  grep "ERROR" archivo.log | wc -l',
         "La opción -l indica que queremos contar líneas. Adapta el archivo de origen y añade > al final para guardar el número en el destino."],
        ["Lee el resultado con cat: debe aparecer un único número. Cada línea se cuenta una vez, aunque contenga la palabra ERROR varias veces."],
        "Consulta man wc. El manual man bash explica cómo funcionan las tuberías."
    ), 0.75, ["La tubería conecta los dos comandos; > guarda el resultado del último."])
    completed("El recuento de líneas de error es correcto.")

    wait_until(boss_index_ok, "RETO FINAL · BUSCAR EL INFORME", lesson(
        [("ORIGEN · registros que debes investigar", LOGS),
         ("DESTINO · dónde debe quedar", REC / "informes" / "indice.txt")],
        ["Busca en los registros la línea que contiene FINAL_REPORT y guárdala en indice.txt. Esa pista identifica el informe que necesitas."],
        ["Ahora aplicarás lo aprendido a los registros del proyecto. La pista está en uno de los archivos .log; utiliza grep para buscarla.",
         "Puedes buscar en varios archivos a la vez y guardar la línea encontrada con >."],
        ["Lee indice.txt con cat. Junto a FINAL_REPORT debe aparecer el nombre de un archivo cifrado."],
        "Repasa man grep si necesitas ayuda para buscar en varios archivos."
    ), 0.82, ["El patrón *.log permite seleccionar todos los registros de la carpeta."])
    completed("El informe que debes descifrar ya está identificado.")

    wait_until(final_ok, "FASE 5 · DESCIFRAR EL INFORME", lesson(
        [("ORIGEN · archivo cifrado", REPORTS / "informe_01.enc"),
         ("DESTINO · archivo descifrado", REC / "informes" / "informe_final.txt")],
        ["Descifra el informe con la contraseña que obtuviste al leer el documento de mantenimiento."],
        ["OpenSSL permite recuperar el texto de un archivo cifrado. Sustituye ARCHIVO y DESTINO por las rutas indicadas arriba:",
         "  openssl enc -d -aes-256-cbc -pbkdf2 \\",
         "    -in ARCHIVO -out DESTINO",
         "La opción -d pide descifrar; -in indica qué archivo leer y -out dónde guardar el resultado. El resto selecciona el cifrado y cómo obtener la clave a partir de la contraseña.",
         "La barra \\ permite continuar la orden en otra línea. OpenSSL te pedirá la contraseña; no se verá mientras la escribes."],
        ["El nuevo informe_final.txt debe contener texto legible. El archivo cifrado original se conserva."],
        "Consulta man openssl-enc para conocer las opciones del comando."
    ), 0.90, ["Escribe la contraseña de César con sus mayúsculas y guiones."])

    while True:
        box("RECUPERACIÓN DIGITAL COMPLETADA", render_lesson(lesson(
            [("DOCUMENTO QUE DEBES LEER", REC / "informes" / "informe_final.txt")],
            ["Lee el informe final y sigue sus instrucciones para encontrar el dispositivo. La última parte del reto ocurre fuera del ordenador."],
            ["Utiliza cat seguido de la ruta del informe para mostrar su contenido en la terminal. Lee las instrucciones completas antes de actuar."],
            ["El documento explica qué debes hacer a continuación. Pide autorización al profesor antes de recuperar el objeto."],
            "Puedes consultar man cat si necesitas recordar cómo leer un archivo."
        ), detail="✓ Has completado todos los pasos de recuperación en el ordenador."),
            1.0, "Lee el informe final para continuar el reto.")
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Consola detenida. Puedes volver a ejecutar ./iniciar.py para continuar.")
