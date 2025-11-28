"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    from pathlib import Path
    import re
    import pandas as pd

    path = (
        Path(__file__)
        .resolve()
        .parents[1]
        .joinpath("files", "input", "clusters_report.txt")
    )

    with path.open(encoding="utf-8") as f:
        lines = [l.rstrip() for l in f]

    # Find the separator line and start after it
    sep_idx = next(i for i, l in enumerate(lines) if re.match(r"-{5,}", l))
    i = sep_idx + 1

    data = []
    current = None
    kw_buffer = []

    cluster_re = re.compile(r"^\s*(\d+)\s+(\d+)\s+(\d+,\d+)\s*%\s*(.*)$")

    def finalize_row():
        """Close the current block and stash the cleaned keywords."""

        if current is None:
            return

        kw = re.sub(r"\s+", " ", " ".join(kw_buffer).strip()).rstrip(".")
        keywords = ", ".join(k.strip() for k in kw.split(",") if k.strip())
        current["principales_palabras_clave"] = keywords
        data.append(current)

    while i < len(lines):
        line = lines[i]
        if not line.strip():  # blank line => end of block
            finalize_row()
            current, kw_buffer = None, []
            i += 1
            continue

        m = cluster_re.match(line)
        if m:
            # start a new cluster row
            finalize_row()  # just in case
            current = {
                "cluster": int(m.group(1)),
                "cantidad_de_palabras_clave": int(m.group(2)),
                "porcentaje_de_palabras_clave": float(m.group(3).replace(",", ".")),
            }
            first_kw = m.group(4).strip()
            if first_kw:
                kw_buffer = [first_kw]
            else:
                kw_buffer = []
        else:
            # continuation of keywords
            kw_buffer.append(line.strip())
        i += 1

    # finalize last row if file ended without blank line
    finalize_row()

    df = pd.DataFrame(data)
    return df