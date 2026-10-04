from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
import shutil
import subprocess
import textwrap
import os

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "escape-linux" / "package-src"
OUT = ROOT / "_site" / "escape-linux" / "download"
PKG = OUT / "escape_fie"


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_odt(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    mimetype = "application/vnd.oasis.opendocument.text"
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" office:version="1.2">
 <office:body><office:text>
  <text:h text:outline-level="1">FIE-LAB — Informe de mantenimiento</text:h>
  <text:p>Intervención: respaldo previo a mantenimiento</text:p>
  <text:p>Estado: recuperación pendiente</text:p>
  <text:p>Antes de la intervención se generaron varios informes cifrados. El informe que contiene las instrucciones finales no puede abrirse sin contraseña.</text:p>
  <text:p>Por seguridad, la contraseña no fue almacenada directamente en este documento.</text:p>
  <text:h text:outline-level="2">Referencia codificada</text:h>
  <text:p>OLQXA-ILH-2026</text:p>
  <text:p>Desplazamiento César: 3</text:p>
  <text:h text:outline-level="2">Herramienta de recuperación</text:h>
  <text:p>https://juanluck.github.io/fundamentos-informatica/escape-linux/cesar/</text:p>
  <text:p>Copia la referencia exactamente, introdúcela en la URL anterior y conserva la contraseña resultante. La necesitarás más adelante.</text:p>
 </office:text></office:body>
</office:document-content>'''
    manifest = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
 <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.text"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''
    with ZipFile(path, "w") as z:
        z.writestr("mimetype", mimetype, compress_type=ZIP_STORED)
        z.writestr("content.xml", content, compress_type=ZIP_DEFLATED)
        z.writestr("META-INF/manifest.xml", manifest, compress_type=ZIP_DEFLATED)


def encrypt(infile, outfile, password):
    subprocess.run([
        "openssl", "enc", "-aes-256-cbc", "-salt", "-pbkdf2",
        "-in", str(infile), "-out", str(outfile), "-pass", f"pass:{password}"
    ], check=True)


if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)
shutil.copytree(SRC, PKG)

# Material generado para evitar almacenar binarios en el repositorio fuente.
write(PKG / "README.txt", '''
FIE — OPERACIÓN RECUPERACIÓN
============================

No modifiques el contenido de este paquete salvo cuando la consola lo indique.

Organización recomendada durante la actividad:
  Terminal 1: ~/escape_fie        -> ./iniciar.py
  Terminal 2: ~/escape_fie        -> consultar el paquete original
  Terminal 3: ~                   -> reconstruir ~/FIE_RECOVERY

La consola de recuperación supervisa automáticamente ~/FIE_RECOVERY.
''')

write(PKG / "tutorial" / "registro.log", '''
INFO  Arranque de subsistema
INFO  Comprobación de red
ERROR Fallo temporal de lectura
INFO  Reintento automático
ERROR Copia incompleta
INFO  Servicio restaurado
ERROR Índice no encontrado
INFO  Fin del diagnóstico
''')

write(PKG / "registros" / "recovery_01.log", '''
2026-10-04 09:11 INFO recovery-start
2026-10-04 09:12 INFO filesystem-ok
2026-10-04 09:13 WARN legacy-copy-detected
''')
write(PKG / "registros" / "recovery_02.log", '''
2026-10-04 09:21 INFO cpu-snapshot-ready
2026-10-04 09:22 ERROR incomplete-index
2026-10-04 09:23 INFO memory-snapshot-ready
''')
write(PKG / "registros" / "recovery_03.log", '''
2026-10-04 09:31 INFO encrypted-reports-found
2026-10-04 09:32 INFO FINAL_REPORT=informe_01.enc
2026-10-04 09:33 INFO recovery-index-closed
''')
write(PKG / "registros" / "recovery_04.log", '''
2026-10-04 09:41 INFO audit-start
2026-10-04 09:42 WARN obsolete-reference
2026-10-04 09:43 INFO audit-end
''')

make_odt(PKG / "documentos" / "Informe_Mantenimiento.odt")

final_text = PKG / "informes" / "_final_plain.txt"
write(final_text, '''
INFORME FINAL DE RECUPERACIÓN
=============================

Integridad del procedimiento: COMPLETA
Estado del respaldo: LOCALIZADO

Si estás leyendo este archivo, has reconstruido correctamente el procedimiento de recuperación.

Queda una última operación.

El dispositivo de respaldo NO está conectado al ordenador.
Se encuentra en la cremallera lateral de la mochila del profesor.

No accedas a ella sin autorización.

1. Acércate al profesor.
2. Míralo y dile: «¿Puedo?»
3. Guiña un ojo.
4. Espera a que te dé permiso explícitamente.
5. Solo entonces, dirígete a su mochila y abre el bolsillo lateral indicado.
6. Recupera el objeto que encontrarás en su interior.
7. Comunica a la clase: «HE COMPLETADO EL RETO».

Fin de la operación.
''')

decoy2 = PKG / "informes" / "_decoy2.txt"
write(decoy2, "INFORME 02 — copia de comprobación. No contiene instrucciones finales.\n")
decoy3 = PKG / "informes" / "_decoy3.txt"
write(decoy3, "INFORME 03 — copia histórica. No contiene instrucciones finales.\n")
decoy4 = PKG / "informes" / "_decoy4.txt"
write(decoy4, "INFORME 04 — registro auxiliar. No contiene instrucciones finales.\n")

encrypt(final_text, PKG / "informes" / "informe_01.enc", "LINUX-FIE-2026")
encrypt(decoy2, PKG / "informes" / "informe_02.enc", "NO-ES-ESTA")
encrypt(decoy3, PKG / "informes" / "informe_03.enc", "TAMPOCO-ESTA")
encrypt(decoy4, PKG / "informes" / "informe_04.enc", "SIGUE-BUSCANDO")
for p in (final_text, decoy2, decoy3, decoy4):
    p.unlink()

# ZIP descargable. El directorio superior es escape_fie/.
zip_path = OUT / "escape_fie.zip"
with ZipFile(zip_path, "w", ZIP_DEFLATED) as z:
    for p in sorted(PKG.rglob("*")):
        if p.is_file():
            z.write(p, Path("escape_fie") / p.relative_to(PKG))

print(f"Generated {zip_path}")
