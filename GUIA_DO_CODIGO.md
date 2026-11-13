# Guia didático — entendendo o SQL List Formatter

Este documento explica o funcionamento do projeto **SQL List Formatter** para quem está começando a aprender Python.

A ideia não é apenas executar o programa: é entender o que cada parte faz, por que ela existe e como as informações percorrem o código.

---

## 1. O que o programa faz?

Imagine que você recebeu um arquivo de texto com vários identificadores numéricos. Alguns podem estar repetidos, outros podem estar escritos com menos dígitos do que o formato desejado.

O programa:

1. Lê os identificadores de um arquivo TXT.
2. Ignora linhas vazias.
3. Verifica se cada valor contém somente números.
4. Verifica se o identificador cabe na quantidade de dígitos configurada.
5. Completa os valores com zeros à esquerda.
6. Remove duplicidades, mantendo a primeira ocorrência.
7. Divide o resultado em arquivos menores.
8. Salva os arquivos formatados e apresenta um resumo.

**Exemplo**

Entrada:

```text
12345
67890
12345
24680
```

Saída:

```text
'0000012345',
'0000067890',
'0000024680'
```

O número `12345` aparece duas vezes na entrada, mas somente uma vez na saída.

---

## 2. Conhecendo a estrutura do projeto

```text
sql-list-formatter/
├── src/
│   └── main.py
├── data/
│   └── entrada.txt
├── output/
├── README.md
├── GUIA_DO_CODIGO.md
├── .gitignore
└── requirements.txt
```

O que cada item representa?

| Arquivo ou pasta | Responsabilidade |
|---|---|
| `src/` | Guarda o código-fonte do programa. |
| `main.py` | Contém as instruções que executam o processamento. |
| `data/` | Guarda os arquivos de entrada. |
| `entrada.txt` | Contém os identificadores que serão processados. |
| `output/` | Recebe os arquivos gerados pelo programa. |
| `README.md` | Apresenta o projeto e ensina como executá-lo. |
| `GUIA_DO_CODIGO.md` | Explica o código com foco em aprendizagem. |
| `.gitignore` | Informa ao Git quais arquivos não devem ser versionados. |
| `requirements.txt` | Lista dependências externas, se houver. |

O projeto utiliza apenas recursos que já fazem parte da biblioteca padrão do Python. Portanto, não é necessário instalar pacotes externos.

---

## 3. Importações: ferramentas que o programa utiliza

No início do arquivo `main.py`, encontramos:

```python
import argparse
from pathlib import Path
```

### `import argparse`

O módulo `argparse` permite receber opções e argumentos pelo terminal.

Por exemplo:

```bash
python src/main.py data/entrada.txt --width 10 --chunk-size 500
```

Nesse comando, o programa recebe:

- O caminho do arquivo de entrada.
- A largura desejada para os identificadores.
- A quantidade máxima de registros por arquivo de saída.

Sem `argparse`, seria necessário construir manualmente uma lógica para interpretar essas opções.

### `from pathlib import Path`

O `Path` facilita o trabalho com caminhos de arquivos e pastas.

Exemplo:

```python
from pathlib import Path

arquivo = Path("data/entrada.txt")

print(arquivo.name)
print(arquivo.suffix)
```

Resultado:

```text
entrada.txt
.txt
```

É uma alternativa mais organizada e multiplataforma do que manipular caminhos somente como textos.

---

## 4. Definindo os caminhos do projeto

```python
PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "data" / "entrada.txt"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "output"
```

Vamos entender cada parte.

### `__file__`

É uma variável especial do Python que representa o caminho do arquivo Python que está sendo executado.

Neste projeto, ela aponta para algo semelhante a:

```text
sql-list-formatter/src/main.py
```

### `.resolve()`

Transforma o caminho em um caminho absoluto, resolvendo referências relativas.

### `.parent`

Retorna a pasta que contém o arquivo.

Como `main.py` está dentro de `src`, o primeiro `.parent` representa a pasta `src`.

O segundo `.parent` representa a raiz do projeto.

### O operador `/` com `Path`

Quando usamos:

```python
PROJECT_DIR / "data" / "entrada.txt"
```

o `Path` combina os componentes do caminho de forma apropriada para o sistema operacional.

**Em resumo:** essas três variáveis definem onde o programa procura a entrada e onde salva os resultados.

---

## 5. Recebendo opções pelo terminal: `parse_arguments()`

```python
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Limpa, deduplica e formata listas de identificadores para SQL."
    )
```

### O que é uma função?

Uma função é um bloco de código que recebe informações, executa uma tarefa e pode devolver um resultado.

A palavra `def` é utilizada para definir uma função.

Neste caso, `parse_arguments()` configura como o programa receberá informações pelo terminal.

Em seguida, temos:

```python
parser.add_argument(
    "input",
    nargs="?",
    type=Path,
    default=DEFAULT_INPUT,
    help="Caminho do arquivo TXT de entrada.",
)
```

Esse argumento permite informar o arquivo de entrada.

Vamos analisar:

- `"input"`: nome do argumento.
- `nargs="?"`: argumento opcional.
- `type=Path`: converte o valor recebido em um objeto `Path`.
- `default=DEFAULT_INPUT`: utiliza o arquivo padrão quando nenhum caminho é informado.
- `help`: texto de ajuda exibido pelo terminal.

O mesmo princípio é utilizado nas opções `--output-dir`, `--width` e `--chunk-size`.

No final da função:

```python
return parser.parse_args()
```

O método `parse_args()` interpreta os argumentos recebidos e devolve um objeto com as opções configuradas.

### Teste prático

Execute:

```bash
python src/main.py --help
```

O terminal apresentará as opções disponíveis.

---

## 6. Lendo e validando os identificadores: `read_identifiers()`

Essa é uma das partes mais importantes do projeto.

```python
def read_identifiers(input_path, width):
    valid = []
    invalid = []
    total_non_empty = 0
```

A função recebe dois parâmetros:

- `input_path`: caminho do arquivo que será lido.
- `width`: quantidade máxima de dígitos permitida.

Depois cria três variáveis:

| Variável | Para que serve |
|---|---|
| `valid` | Armazena identificadores válidos. |
| `invalid` | Armazena informações sobre linhas inválidas. |
| `total_non_empty` | Conta as linhas que não estão vazias. |

### Abrindo o arquivo

```python
with input_path.open("r", encoding="utf-8-sig") as file:
```

Aqui utilizamos `with` para abrir o arquivo.

- `open("r")`: abre o arquivo no modo de leitura (*read*).
- `encoding="utf-8-sig"`: permite ler arquivos UTF-8 e também lidar com um possível marcador BOM no início do arquivo.
- `as file`: atribui o arquivo aberto à variável `file`.

Uma vantagem de `with` é que o arquivo é fechado automaticamente ao sair do bloco, inclusive se ocorrer uma exceção.

### Percorrendo as linhas

```python
for line_number, raw_line in enumerate(file, start=1):
    value = raw_line.strip()
```

O `for` percorre cada linha do arquivo.

O `enumerate()` permite obter duas informações ao mesmo tempo:

1. O número da linha.
2. O conteúdo daquela linha.

O `start=1` faz a contagem começar em 1, como normalmente numeramos linhas em um arquivo.

O `.strip()` remove espaços e quebras de linha das extremidades do texto.

Exemplo:

```python
raw_line = "  12345\n"
value = raw_line.strip()

print(value)
```

Resultado:

```text
12345
```

### Ignorando linhas vazias

```python
if not value:
    continue
```

O `if` verifica uma condição.

Se `value` estiver vazio, o `continue` pula para a próxima repetição do `for`.

Assim, linhas vazias não são consideradas identificadores.

### Validando os números

```python
if not value.isdigit():
    invalid.append((line_number, value, "contém caracteres não numéricos"))
    continue
```

O método `.isdigit()` verifica se todos os caracteres do texto são dígitos.

Exemplos:

```python
"12345".isdigit()   # True
"12A45".isdigit()   # False
"12-45".isdigit()   # False
```

Quando o valor não é numérico, adicionamos uma informação à lista `invalid`.

O método `.append()` adiciona um elemento ao final de uma lista.

Nesse caso, adicionamos uma tupla contendo:

- Número da linha.
- Valor encontrado.
- Motivo da rejeição.

### Verificando o tamanho

```python
if len(value) > width:
    invalid.append(
        (line_number, value, f"ultrapassa a largura configurada ({width})")
    )
    continue
```

O `len()` retorna a quantidade de caracteres.

Se o identificador tiver mais dígitos do que a largura permitida, ele será considerado inválido.

O `f` antes das aspas indica uma *f-string*, que permite inserir variáveis dentro de um texto.

### Completando com zeros

```python
valid.append(value.zfill(width))
```

O método `.zfill()` completa uma string com zeros à esquerda até atingir o tamanho solicitado.

Exemplo:

```python
codigo = "12345"

print(codigo.zfill(10))
```

Resultado:

```text
0000012345
```

Observe que o identificador é tratado como texto (`str`), e não como número inteiro (`int`).

Isso é importante porque zeros à esquerda fazem parte do formato desejado. Se convertermos `"0000012345"` para inteiro, os zeros iniciais desaparecem.

### Retornando os resultados

```python
return valid, invalid, total_non_empty
```

A função devolve três resultados.

No Python, podemos retornar vários valores separados por vírgula. Quem chama a função poderá receber esses resultados em três variáveis.

---

## 7. Removendo duplicidades: `remove_duplicates()`

```python
def remove_duplicates(identifiers):
    unique = list(dict.fromkeys(identifiers))
    return unique, len(identifiers) - len(unique)
```

Essa função recebe uma lista de identificadores.

O objetivo é remover valores repetidos sem alterar a ordem da primeira ocorrência.

Vamos dividir a expressão:

### `dict.fromkeys()`

Cria um dicionário usando os elementos da lista como chaves.

As chaves de um dicionário não se repetem.

Exemplo:

```python
codigos = ["111", "222", "111", "333"]

resultado = dict.fromkeys(codigos)

print(resultado)
```

Resultado conceitual:

```text
{"111": None, "222": None, "333": None}
```

### `list()`

Transforma o resultado em uma lista novamente:

```python
unique = list(dict.fromkeys(identifiers))
```

Resultado:

```python
["111", "222", "333"]
```

O Python preserva a ordem de inserção dos dicionários modernos.

### Calculando duplicidades removidas

```python
len(identifiers) - len(unique)
```

Se tínhamos 100 identificadores e, depois da remoção, restaram 80:

```text
100 - 80 = 20 duplicidades removidas
```

A função retorna a lista sem duplicidades e a quantidade removida.

**Atenção:** a deduplicação acontece depois da padronização. Assim, `12345` e `0000012345` passam a representar o mesmo identificador.

---

## 8. Gerando os arquivos: `write_output_files()`

```python
def write_output_files(identifiers, output_dir, chunk_size):
```

Essa função recebe:

- `identifiers`: identificadores únicos.
- `output_dir`: pasta de destino.
- `chunk_size`: quantidade máxima de registros em cada arquivo.

### Criando a pasta de saída

```python
output_dir.mkdir(parents=True, exist_ok=True)
```

O método `mkdir()` cria um diretório.

- `parents=True`: cria também as pastas superiores necessárias.
- `exist_ok=True`: não gera erro se a pasta já existir.

### Verificando se existe conteúdo

```python
if not identifiers:
    return []
```

Se a lista estiver vazia, a função retorna uma lista vazia, pois não há nada para gravar.

### Dividindo a lista em blocos

```python
for start in range(0, len(identifiers), chunk_size):
    chunk = identifiers[start:start + chunk_size]
```

Essa parte utiliza duas ferramentas importantes: `range()` e *slicing*.

Imagine que existam 1.850 identificadores e que cada arquivo possa conter no máximo 500.

O `range()` produzirá os pontos iniciais:

```text
0, 500, 1000, 1500
```

O *slicing* seleciona um trecho da lista:

```python
chunk = identifiers[start:start + chunk_size]
```

Assim, os registros são divididos em blocos de até 500 elementos.

Resultado:

| Arquivo | Quantidade |
|---|---:|
| 001 | 500 |
| 002 | 500 |
| 003 | 500 |
| 004 | 350 |
| **Total** | **1.850** |

### Criando o nome do arquivo

```python
file_number = len(output_files) + 1
output_path = output_dir / f"lista_formatada_{file_number:03d}.txt"
```

O `file_number` controla a numeração dos arquivos.

A expressão `:03d` formata um número inteiro com três posições, preenchendo com zeros à esquerda.

Exemplos:

```text
1   -> 001
2   -> 002
10  -> 010
```

### Formatando os identificadores

```python
formatted_lines = [
    f"'{identifier}'" + ("," if index < len(chunk) - 1 else "")
    for index, identifier in enumerate(chunk)
]
```

Aqui temos uma *list comprehension*, uma maneira compacta de construir uma lista.

Para cada identificador:

1. Colocamos aspas simples ao redor do valor.
2. Adicionamos uma vírgula se não for o último elemento do bloco.
3. Não adicionamos vírgula ao último elemento.

Exemplo:

```text
'0000012345',
'0000067890',
'0000024680'
```

Isso facilita copiar o conteúdo para uma cláusula SQL `IN`, sem deixar uma vírgula sobrando no final.

### Gravando o arquivo

```python
output_path.write_text(
    "\n".join(formatted_lines) + "\n",
    encoding="utf-8",
)
```

Vamos entender:

- `"\n"` representa uma quebra de linha.
- `.join()` une os elementos da lista usando essa quebra.
- `.write_text()` grava o texto no arquivo.
- `encoding="utf-8"` define a codificação do arquivo.

No final, o caminho do arquivo é adicionado à lista `output_files`.

A função retorna todos os arquivos criados.

---

## 9. Coordenando o programa: `main()`

A função `main()` organiza a execução. Ela chama as outras funções na ordem correta.

```python
def main():
    args = parse_arguments()
```

Primeiro, recebemos os argumentos do terminal.

```python
if args.width < 1:
    raise SystemExit("Erro: --width deve ser maior que zero.")
```

Validamos se a largura é maior que zero.

O `raise SystemExit()` encerra o programa e apresenta uma mensagem.

O mesmo tipo de validação é feito para `chunk_size`.

### Verificando o arquivo de entrada

```python
if not args.input.is_file():
    raise SystemExit(f"Erro: arquivo de entrada não encontrado: {args.input}")
```

O método `.is_file()` verifica se o caminho corresponde a um arquivo existente.

Se não existir, o programa encerra com uma mensagem de erro.

### Tratando erros de leitura

```python
try:
    valid, invalid, total = read_identifiers(args.input, args.width)
except UnicodeDecodeError:
    raise SystemExit("Erro: não foi possível ler o arquivo como UTF-8.")
```

O bloco `try` tenta executar uma operação.

Se ocorrer um erro de decodificação de texto, o `except` captura especificamente `UnicodeDecodeError` e apresenta uma mensagem mais compreensível.

Isso é chamado de tratamento de exceções.

### Executando o processamento

```python
unique, duplicates_removed = remove_duplicates(valid)
output_files = write_output_files(unique, args.output_dir, args.chunk_size)
```

Aqui acontece a sequência principal:

1. Remove as duplicidades.
2. Gera os arquivos formatados.

### Apresentando o resumo

```python
print("\nProcessamento concluído!")
print(f"Linhas não vazias lidas: {total}")
print(f"Identificadores válidos: {len(valid)}")
print(f"Duplicidades removidas: {duplicates_removed}")
print(f"Linhas inválidas: {len(invalid)}")
print(f"Identificadores únicos gerados: {len(unique)}")
print(f"Arquivos criados: {len(output_files)}")
```

O `print()` apresenta informações no terminal.

As expressões com `f` são *f-strings*, que permitem combinar texto e valores de variáveis.

No final, o programa também lista os arquivos gerados e informa quais linhas foram rejeitadas.

---

## 10. O ponto de entrada: `if __name__ == "__main__"`

No final do arquivo encontramos:

```python
if __name__ == "__main__":
    main()
```

Essa estrutura é muito comum em projetos Python.

A variável especial `__name__` indica como o arquivo está sendo utilizado.

Quando executamos diretamente:

```bash
python src/main.py
```

O Python define `__name__` como `"__main__"`.

Assim, a função `main()` é executada.

Essa estrutura também permite importar funções de `main.py` em outro arquivo sem executar automaticamente todo o programa.

---

## 11. Fluxo completo do programa

Veja a sequência de processamento:

```text
Início
  |
  v
Receber argumentos do terminal
  |
  v
Verificar arquivo de entrada
  |
  v
Ler arquivo TXT
  |
  v
Ignorar linhas vazias
  |
  v
Validar os identificadores
  |
  v
Padronizar com zeros à esquerda
  |
  v
Remover duplicidades
  |
  v
Dividir em blocos
  |
  v
Formatar com aspas e vírgulas
  |
  v
Gravar arquivos TXT
  |
  v
Exibir relatório
  |
  v
Fim
```

---

## 12. Como executar o projeto

Abra o terminal na pasta raiz do projeto.

### Execução padrão

```bash
python src/main.py
```

Utiliza o arquivo `data/entrada.txt`, largura de 10 dígitos e blocos de até 500 registros.

### Informando outro arquivo

```bash
python src/main.py caminho/arquivo.txt
```

### Alterando a largura

```bash
python src/main.py data/entrada.txt --width 12
```

### Alterando o limite de registros

```bash
python src/main.py data/entrada.txt --chunk-size 100
```

### Combinando opções

```bash
python src/main.py data/entrada.txt --width 10 --chunk-size 500 --output-dir output
```

---

## 13. Conceitos de Python praticados

| Conceito | Onde aparece | O que você aprende |
|---|---|---|
| Variáveis | `PROJECT_DIR`, `valid` | Armazenar informações. |
| Tipos de dados | `str`, `int`, listas | Trabalhar com diferentes valores. |
| Funções | `def main()` | Organizar e reutilizar código. |
| Parâmetros | `read_identifiers(input_path, width)` | Enviar informações às funções. |
| Condicionais | `if` | Tomar decisões. |
| Laços de repetição | `for` | Percorrer coleções. |
| Listas | `valid`, `invalid` | Armazenar vários elementos. |
| Tuplas | `invalid.append((...))` | Agrupar informações. |
| Dicionários | `dict.fromkeys()` | Trabalhar com chaves únicas. |
| Tratamento de exceções | `try` e `except` | Tratar erros. |
| Manipulação de arquivos | `Path`, `open`, `write_text` | Ler e gravar arquivos. |
| Argumentos CLI | `argparse` | Criar programas configuráveis pelo terminal. |
| List comprehension | `formatted_lines` | Construir listas de forma concisa. |
| F-strings | `f"..."` | Montar textos dinâmicos. |

---

## 14. Exercícios para praticar

Tente resolver os exercícios antes de consultar uma solução.

### Exercício 1 — Alterar a largura

Execute o programa com largura de 8 dígitos.

Perguntas:

- O que acontece com um identificador de 5 dígitos?
- O que acontece com um identificador de 9 dígitos?
- Qual função realiza essa validação?

### Exercício 2 — Alterar o tamanho dos blocos

Execute o programa com:

```bash
python src/main.py --chunk-size 100
```

Se existirem 1.850 identificadores únicos, quantos arquivos serão gerados?

### Exercício 3 — Criar uma nova validação

Modifique o programa para rejeitar identificadores com menos de 4 dígitos antes da padronização.

Dica: utilize `len(value)`.

### Exercício 4 — Criar um relatório

Adicione ao resumo final a porcentagem de duplicidades removidas em relação aos identificadores válidos.

Dica: você pode calcular:

```python
percentage = (duplicates_removed / len(valid)) * 100
```

Lembre-se de tratar o caso em que `valid` está vazio para evitar divisão por zero.

### Exercício 5 — Separar responsabilidades

Imagine que o projeto cresça.

Como você poderia separar a leitura, a validação e a formatação em módulos Python diferentes?

---

## 15. Boas práticas e limitações importantes

- Identificadores são tratados como texto para preservar zeros à esquerda.
- A deduplicação preserva a primeira ocorrência.
- O programa não executa comandos SQL nem se conecta a bancos de dados.
- A validação atual considera apenas dígitos numéricos e tamanho máximo.
- O programa não valida se um identificador realmente existe em algum sistema externo.
- Os arquivos com nomes iguais na pasta de saída podem ser sobrescritos em uma nova execução.
- Para aplicações que recebem dados externos, prefira consultas SQL parametrizadas em vez de construir comandos por concatenação de texto.

**Importante:** os valores gerados são uma representação textual para facilitar o uso. Em sistemas reais, a forma mais segura de consultar muitos identificadores depende do banco de dados e da biblioteca utilizada.

---

## Conclusão

O SQL List Formatter é um exercício prático de automação com Python. Mesmo sendo pequeno, ele reúne conceitos importantes: funções, validação, estruturas de dados, manipulação de arquivos, argumentos de terminal e tratamento de erros.

Uma boa forma de aprender é modificar uma parte por vez, executar novamente, observar o resultado e entender por que ele mudou.
