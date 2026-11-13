# Guia: como transformar Markdown em PDF pelo VS Code

Este guia mostra como converter um arquivo Markdown (`.md`) em PDF mantendo sua organização visual: títulos, subtítulos, textos em negrito, listas, tabelas e blocos de código.

O procedimento utiliza o Visual Studio Code e a extensão **Markdown PDF**, publicada por **yzane**.

## 1. O que é Markdown?

Markdown é uma linguagem simples de marcação usada para estruturar documentos de texto.

Por exemplo, este trecho:

```markdown
# Título principal

## Subtítulo

Este é um texto com **negrito**.

- Primeiro item
- Segundo item

| Linguagem | Uso |
|---|---|
| Python | Automação |
| SQL | Consultas |
```

é interpretado por ferramentas compatíveis como um documento formatado, com título, subtítulo, negrito, lista e tabela.

Ao exportar para PDF, a intenção é preservar essa apresentação, em vez de imprimir o arquivo como texto puro.

## 2. Instalar a extensão Markdown PDF

1. Abra o Visual Studio Code.
2. Abra a área de extensões pelo ícone de quadradinhos na barra lateral ou pressione `Ctrl + Shift + X`.
3. Pesquise por `Markdown PDF`.
4. Localize a extensão publicada por **yzane**.
5. Clique em **Install**.

<text>
Após a instalação, o VS Code terá comandos para exportar arquivos Markdown para PDF.
</text>

## 3. Abrir o arquivo Markdown

Abra no VS Code o arquivo que deseja converter, por exemplo:

```text
GUIA_DO_CODIGO.md
```

Você pode conferir a aparência formatada usando a visualização Markdown:

- Pressione `Ctrl + Shift + V` para abrir a pré-visualização.
- Ou use `Ctrl + K` e depois `V` para abrir a pré-visualização ao lado do código-fonte.

A pré-visualização ajuda a conferir títulos, tabelas, listas e demais elementos antes da exportação.

## 4. Exportar para PDF

Com o arquivo `.md` aberto:

1. Pressione `Ctrl + Shift + P` para abrir a Paleta de Comandos.
2. Digite `Markdown PDF`.
3. Selecione **Markdown PDF: Export (pdf)**.
4. Aguarde a geração do documento.

Por padrão, o PDF é salvo na mesma pasta do arquivo Markdown.

Exemplo:

```text
projeto/
├── GUIA_DO_CODIGO.md
└── GUIA_DO_CODIGO.pdf
```

O arquivo `.md` continua sendo a versão editável do documento. O PDF é uma versão prática para leitura, compartilhamento e impressão.

## 5. Imprimir o PDF

Se quiser imprimir o documento:

1. Abra o PDF gerado.
2. Pressione `Ctrl + P`.
3. Confira as opções antes de imprimir.

Configurações iniciais sugeridas:

| Opção | Configuração sugerida |
|---|---|
| Tamanho do papel | A4 |
| Orientação | Retrato |
| Margens | Padrão |
| Escala | Ajustar à página |
| Gráficos de segundo plano | Ativado, quando disponível |

A aparência final pode variar conforme o leitor de PDF, a impressora e o conteúdo do documento. Antes de imprimir muitas páginas, confira a prévia de impressão.

## 6. Dicas para melhorar o resultado

### Organize bem os títulos

Use níveis de título em ordem lógica:

```markdown
# Título do documento

## Seção

### Subseção
```

Evite pular níveis sem necessidade, como sair diretamente de `#` para `####`.

### Prefira tabelas simples

Tabelas muito largas podem ultrapassar a área imprimível da página. Quando possível, use nomes de colunas curtos e evite muitas colunas.

### Revise blocos de código

Blocos de código longos também podem ultrapassar a largura da página. Considere dividir exemplos extensos em partes menores.

### Confira imagens e links

Verifique se as imagens aparecem corretamente e se os links estão escritos de forma válida antes de exportar.

### Faça uma prévia antes de imprimir

Abra o PDF e confira:
- Se os títulos estão legíveis.
- Se as tabelas não foram cortadas.
- Se os blocos de código cabem na página.
- Se não há páginas em branco ou quebras inesperadas.

## 7. Personalização visual com CSS

A extensão permite personalizar a aparência da exportação por meio de CSS, quando configurada para utilizar uma folha de estilos.

Com CSS, é possível ajustar elementos como:

- Fonte e tamanho dos textos.
- Espaçamento entre seções.
- Aparência de tabelas.
- Cores de títulos.
- Blocos de código.
- Margens e quebras de página.

Exemplo ilustrativo de CSS:

```css
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
}

h1, h2, h3 {
    page-break-after: avoid;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    border: 1px solid #cccccc;
    padding: 6px;
}

pre, code {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}
```

A configuração exata para carregar o CSS depende das opções disponíveis na extensão e da versão instalada. Consulte as configurações da extensão no VS Code para indicar uma folha de estilos personalizada.

## 8. Resumo rápido

Depois de instalar a extensão, o fluxo habitual é:

1. Abrir o arquivo `.md`.
2. Conferir a pré-visualização com `Ctrl + Shift + V`.
3. Abrir a Paleta de Comandos com `Ctrl + Shift + P`.
4. Executar `Markdown PDF: Export (pdf)`.
5. Abrir o PDF gerado e revisar o resultado.

## 9. Markdown ou PDF: qual utilizar?

| Formato | Melhor utilização |
|---|---|
| Markdown (`.md`) | Editar, manter documentação no GitHub e acompanhar alterações. |
| PDF (`.pdf`) | Ler, compartilhar, arquivar e imprimir o documento com layout preservado. |

**Boa prática:** mantenha o arquivo Markdown como documento-fonte do projeto e gere o PDF quando precisar de uma versão pronta para leitura ou impressão. Assim, você pode atualizar o conteúdo no `.md` e exportar novamente o PDF quando necessário.
