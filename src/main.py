"""
SQL List Formatter

Lê identificadores de um arquivo TXT, valida e padroniza os valores,
remove duplicidades e gera arquivos prontos para uso em cláusulas SQL IN.
"""

import argparse
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "data" / "entrada.txt"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "output"


def parse_arguments():
    """Configura os argumentos opcionais da linha de comando."""
    parser = argparse.ArgumentParser(
        description="Limpa, deduplica e formata listas de identificadores para SQL."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT,
        help="Caminho do arquivo TXT de entrada.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Diretório onde os arquivos gerados serão salvos.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=10,
        help="Quantidade de dígitos do identificador (padrão: 10).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Quantidade máxima de identificadores por arquivo (padrão: 500).",
    )
    return parser.parse_args()


def read_identifiers(input_path, width):
    """
    Lê e valida os identificadores.

    Linhas vazias são ignoradas. Apenas valores numéricos com tamanho
    menor ou igual à largura configurada são aceitos.
    """
    valid = []
    invalid = []
    total_non_empty = 0

    with input_path.open("r", encoding="utf-8-sig") as file:
        for line_number, raw_line in enumerate(file, start=1):
            value = raw_line.strip()

            if not value:
                continue

            total_non_empty += 1

            if not value.isdigit():
                invalid.append((line_number, value, "contém caracteres não numéricos"))
                continue

            if len(value) > width:
                invalid.append(
                    (line_number, value, f"ultrapassa a largura configurada ({width})")
                )
                continue

            valid.append(value.zfill(width))

    return valid, invalid, total_non_empty


def remove_duplicates(identifiers):
    """Remove duplicidades e preserva a primeira ocorrência."""
    unique = list(dict.fromkeys(identifiers))
    return unique, len(identifiers) - len(unique)


def write_output_files(identifiers, output_dir, chunk_size):
    """Gera arquivos numerados, com no máximo chunk_size linhas cada."""
    output_dir.mkdir(parents=True, exist_ok=True)

    if not identifiers:
        return []

    output_files = []

    for start in range(0, len(identifiers), chunk_size):
        chunk = identifiers[start:start + chunk_size]
        file_number = len(output_files) + 1
        output_path = output_dir / f"lista_formatada_{file_number:03d}.txt"

        # A última linha não recebe vírgula, facilitando o uso em SQL IN.
        formatted_lines = [
            f"'{identifier}'" + ("," if index < len(chunk) - 1 else "")
            for index, identifier in enumerate(chunk)
        ]

        output_path.write_text(
            "\n".join(formatted_lines) + "\n",
            encoding="utf-8",
        )
        output_files.append(output_path)

    return output_files


def main():
    args = parse_arguments()

    if args.width < 1:
        raise SystemExit("Erro: --width deve ser maior que zero.")

    if args.chunk_size < 1:
        raise SystemExit("Erro: --chunk-size deve ser maior que zero.")

    if not args.input.is_file():
        raise SystemExit(f"Erro: arquivo de entrada não encontrado: {args.input}")

    try:
        valid, invalid, total = read_identifiers(args.input, args.width)
    except UnicodeDecodeError:
        raise SystemExit("Erro: não foi possível ler o arquivo como UTF-8.")

    unique, duplicates_removed = remove_duplicates(valid)
    output_files = write_output_files(unique, args.output_dir, args.chunk_size)

    print("\nProcessamento concluído!")
    print(f"Linhas não vazias lidas: {total}")
    print(f"Identificadores válidos: {len(valid)}")
    print(f"Duplicidades removidas: {duplicates_removed}")
    print(f"Linhas inválidas: {len(invalid)}")
    print(f"Identificadores únicos gerados: {len(unique)}")
    print(f"Arquivos criados: {len(output_files)}")

    if output_files:
        print("\nArquivos de saída:")
        for path in output_files:
            print(f"  - {path}")

    if invalid:
        print("\nLinhas ignoradas:")
        for line_number, value, reason in invalid:
            print(f"  Linha {line_number}: {value!r} ({reason})")


if __name__ == "__main__":
    main()
