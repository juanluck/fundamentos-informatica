#!RUTA_PYTHON
# FIE · Operación Recuperación
# La primera línea debe ser completada por el alumnado con la salida de: which python3

from pathlib import Path
import hashlib
import os
import shutil
import sys
import time

PACKAGE = Path(__file__).resolve().parent
HOME = Path.home()
REC = HOME / "FIE_RECOVERY"
START = time.time()
WIDTH = 76

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
    for raw in lines:
        for line in str(raw).splitlines() or [""]:
            txt = ("  " + line)[:WIDTH]
            print("║" + txt.ljust(WIDTH) + "║")
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


def flash(msg, progress, seconds=2):
    end = time.time() + seconds
    while time.time() < end:
        box("CAMBIO DETECTADO", ["", "✓ " + msg, ""], progress, "Verificando siguiente etapa...")
        time.sleep(0.25)


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
    box("CONSOLA DE RECUPERACIÓN", [
        "Paquete de emergencia detectado.",
        "",
        "ESTADO",
        "  Estructura de trabajo ........ DAÑADA",
        "  Identificación del equipo .... DESCONOCIDA",
        "  Expediente de mantenimiento .. BLOQUEADO",
        "  Índice de informes ........... DAÑADO",
        "  Dispositivo de respaldo ...... NO LOCALIZADO",
        "",
        "OBJETIVO: recuperar el dispositivo físico de respaldo.",
        "",
        "Mantén esta consola abierta. Trabaja desde otras terminales."
    ], 0.0, "La supervisión automática comienza en 4 segundos...")
    time.sleep(4)

    wait_until(lambda: (REC.is_dir(), None if REC.is_dir() else f"Crea el directorio {REC}"),
               "FASE 1 · RECONSTRUCCIÓN", [
                   "El directorio principal del sistema de respaldo se ha perdido.",
                   "La ruta registrada era:",
                   f"    {REC}"
               ], 0.04, ["Piensa qué comando crea un directorio nuevo."])
    flash("DIRECTORIO DE RECUPERACIÓN DETECTADO", 0.08)

    wait_until(has_dirs, "FASE 1 · RECONSTRUCCIÓN", [
        "Reconstruye dentro de FIE_RECOVERY los tres módulos originales:",
        "",
        "    documentos/",
        "    informes/",
        "    sistema/"
    ], 0.10, ["Puedes crear varios directorios con mkdir."])
    flash("ESTRUCTURA BÁSICA RESTAURADA", 0.16)

    wait_until(copied_state, "FASE 1 · RECUPERAR ESTADO", [
        "En el paquete original se conserva el estado del equipo.",
        "",
        f"Origen:  {FRAG / 'estado.txt'}",
        f"Destino: {REC / 'sistema' / 'estado_inicial.txt'}",
        "",
        "Recupéralo conservando exactamente su contenido."
    ], 0.18, ["Necesitas copiar un fichero y cambiar su nombre en el destino."])
    flash("ESTADO INICIAL VERIFICADO", 0.24)

    wait_until(docs_copied, "FASE 1 · DOCUMENTACIÓN", [
        "Recupera TODOS los documentos de texto del directorio fragmentos/.",
        "",
        f"Origen:  {FRAG}",
        f"Destino: {REC / 'documentos'}",
        "",
        "Los documentos válidos tienen extensión .txt"
    ], 0.26, ["Los comodines permiten seleccionar muchos ficheros: piensa en *.txt"])
    flash("DOCUMENTACIÓN RECUPERADA", 0.32)

    wait_until(obsolete_removed, "FASE 1 · DEPURACIÓN", [
        "El manifiesto marca una copia obsoleta que no debe conservarse:",
        "",
        f"    {REC / 'documentos' / 'estado_old.txt'}",
        "",
        "Elimínala del sistema reconstruido."
    ], 0.34, ["rm elimina ficheros. Comprueba bien la ruta antes de usarlo."])
    flash("FASE 1 COMPLETADA", 0.40)

    wait_until(system_files_ok, "FASE 2 · IDENTIFICACIÓN", [
        "Antes de confiar en los informes hay que documentar el sistema real.",
        "Crea estas copias dentro de FIE_RECOVERY/sistema/:",
        "",
        "  cpu.txt      ← /proc/cpuinfo",
        "  memoria.txt  ← /proc/meminfo",
        "  version.txt  ← /proc/version",
        "",
        "La consola verificará automáticamente su contenido."
    ], 0.42, ["Los ficheros de /proc pueden copiarse igual que cualquier fichero de texto."])
    flash("EQUIPO IDENTIFICADO", 0.52)
    unlock_odt()

    box("FASE 3 · EXPEDIENTE RECUPERADO", [
        "Se ha desbloqueado un documento asociado al procedimiento:",
        "",
        f"    {REC / 'documentos' / 'Informe_Mantenimiento.odt'}",
        "",
        "Ábrelo con LibreOffice Writer.",
        "El informe contiene una referencia codificada y una URL exacta.",
        "Usa esa página para obtener la contraseña de recuperación.",
        "",
        "No tendrás que escribir la contraseña en esta consola: consérvala."
    ], 0.57, "La siguiente fase se activará automáticamente en 10 segundos...")
    time.sleep(10)

    wait_until(grep_tutorial_ok, "FASE 4 · TUTORIAL: grep", [
        "Los registros son demasiado grandes para leerlos línea a línea.",
        "grep selecciona las líneas que contienen un texto.",
        "",
        "Ejemplo:",
        "    grep \"ERROR\" archivo.log",
        "",
        "Ahora genera:",
        f"    {REC / 'sistema' / 'errores.txt'}",
        "con las líneas ERROR de:",
        f"    {TUTORIAL / 'registro.log'}",
        "",
        "Para guardar la salida de un comando en un fichero puedes usar >"
    ], 0.60, ["Una posible forma empieza por: grep \"ERROR\" ... > ..."])
    flash("grep DOMINADO", 0.66)

    wait_until(find_tutorial_ok, "FASE 4 · TUTORIAL: find", [
        "find localiza ficheros por criterios.",
        "",
        "Ejemplo:",
        "    find . -name \"*.txt\"",
        "",
        "Genera informes/cifrados.txt con las rutas de TODOS los .enc que hay en:",
        f"    {REPORTS}",
        "",
        "Guarda el resultado mediante >"
    ], 0.68, ["Cambia el punto del ejemplo por el directorio que quieres explorar."])
    flash("find DOMINADO", 0.73)

    wait_until(pipe_tutorial_ok, "FASE 4 · TUTORIAL: PIPELINE", [
        "El símbolo | conecta programas:",
        "la salida del primero pasa a ser la entrada del segundo.",
        "",
        "Ejemplo:",
        "    grep \"ERROR\" archivo.log | wc -l",
        "",
        "Genera sistema/numero_errores.txt con el número de líneas ERROR de:",
        f"    {TUTORIAL / 'registro.log'}",
        "",
        "Combina grep, |, wc -l y >"
    ], 0.75, ["La tubería cuenta; la redirección final guarda ese número."])
    flash("TUTORIAL AVANZADO COMPLETADO", 0.80)

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
        "Esta vez decide tú cómo combinar las herramientas aprendidas."
    ], 0.82, ["grep puede buscar el mismo texto en varios *.log"])
    flash("INFORME FINAL IDENTIFICADO: informe_01.enc", 0.88)

    wait_until(final_ok, "FASE 5 · DESCIFRADO FINAL", [
        "Dispones de las dos piezas necesarias:",
        "",
        "  Archivo:    informe_01.enc",
        "  Contraseña: la obtenida con el decodificador César",
        "",
        "El informe usa AES-256-CBC con PBKDF2.",
        "Patrón del comando:",
        "",
        "  openssl enc -d -aes-256-cbc -pbkdf2 \\",
        "    -in ARCHIVO \\",
        "    -out DESTINO \\",
        "    -pass pass:CONTRASEÑA",
        "",
        f"El destino debe ser: {REC / 'informes' / 'informe_final.txt'}"
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
