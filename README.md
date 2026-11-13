# SQL List Formatter

Ferramenta simples em Python para limpar, validar, padronizar e formatar listas de identificadores para utilização em consultas SQL, especialmente em cláusulas `IN`.

## Funcionalidades

- Lê identificadores de um arquivo `.txt`, um por linha.
- Ignora linhas vazias.
- Valida se os valores contêm somente números.
- Completa identificadores com zeros à esquerda.
- Remove duplicidades, preservando a primeira ocorrência.
- Divide os resultados em arquivos com limite configurável de registros.
- Gera uma lista entre aspas simples, separada por vírgulas e pronta para ser utilizada em SQL.
- Apresenta um resumo do processamento e informa as linhas inválidas.

## Estrutura do projeto

```text
sql-list-formatter/
├── src/
│   └── main.py
├── data/
│   └── entrada.txt
├── output/
├── README.md
├── .gitignore
└── requirements.txt
```

## Requisitos

- Python 3.9 ou superior.
- Não utiliza bibliotecas externas.

## Como utilizar

### 1. Preparar o arquivo de entrada

Adicione os identificadores ao arquivo `data/entrada.txt`, colocando um identificador por linha.

Exemplo:

```text
12345
67890
12345
24680
```

### 2. Executar o programa

Na pasta raiz do projeto, execute:

```bash
python src/main.py
```

O programa utilizará `data/entrada.txt` como entrada e salvará os arquivos gerados na pasta `output/`.

### 3. Informar outro arquivo de entrada

```bash
python src/main.py caminho/para/arquivo.txt
```

### 4. Personalizar a formatação

É possível alterar a quantidade de dígitos e o limite de registros por arquivo:

```bash
python src/main.py data/entrada.txt --width 10 --chunk-size 500
```

Também é possível escolher outro diretório de saída:

```bash
python src/main.py data/entrada.txt --output-dir resultados
```

## Exemplo de entrada

```text
12345
67890
12345
24680
13579
```

## Exemplo de saída

```sql
'0000012345',
'0000067890',
'0000024680',
'0000013579'
```

Os valores duplicados são removidos após a padronização. Por exemplo, `12345` e `0000012345` são tratados como o mesmo identificador.

## Validações

O programa ignora e informa:

- Valores que contenham letras ou caracteres especiais.
- Identificadores maiores que a largura configurada.

Linhas vazias são ignoradas automaticamente. Os valores inválidos não entram nos arquivos de saída.

## Observação sobre SQL

O conteúdo gerado pode ser utilizado em uma cláusula `IN`, por exemplo:

```sql
SELECT *
FROM tabela_exemplo
WHERE identificador IN (
    '0000012345',
    '0000067890',
    '0000024680'
);
```

A ferramenta apenas formata os valores. Ela não executa consultas nem se conecta a bancos de dados. Para aplicações que recebem dados externos, prefira consultas parametrizadas em vez de montar SQL por concatenação de texto.

## Tecnologias

- Python
- Biblioteca padrão: `argparse` e `pathlib`

## Licença

Este projeto pode ser distribuído sob a licença MIT. Caso escolha essa licença, adicione um arquivo `LICENSE` com o texto oficial correspondente.
