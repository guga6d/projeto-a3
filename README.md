# Descubra sua viagem dos sonhos

Aplicação desktop em Python com interface gráfica (CustomTkinter) para votação de destinos de viagem. Os participantes respondem a um questionário, escolhem entre destinos sugeridos e os votos são registrados em sessões salvas em arquivos CSV.

## Requisitos

| Requisito | Versão |
|-----------|--------|
| **Python** | **3.10 ou superior** (recomendado: 3.11+) |

Para verificar sua versão instalada:

```bash
python --version
```

## Instalação

### 1. Clone ou baixe o projeto

```bash
git clone <url-do-repositorio>
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Dependências instaladas:

- `customtkinter==5.2.2` — interface gráfica
- `Pillow==12.2.0` — carregamento e redimensionamento de imagens

## Como executar

Na raiz do projeto (onde está o arquivo `main.py`):

```bash
python main.py
```

A janela **"Descubra sua viagem dos sonhos"** será aberta.

## Fluxo da aplicação

1. **Boas-vindas** — informe o nome da sessão de votação.
2. **Perguntas** — responda duas perguntas sobre estilo de viagem e companhia.
3. **Destinos** — escolha o destino preferido entre as opções sugeridas.
4. **Resultados parciais** — veja o ranking atual, adicione outro voto ou use o botão destacado de finalizar votação.
5. **Vencedor** — exibe o destino mais votado ao final da sessão ou, em caso de empate, apenas os destinos empatados.

## Comportamentos da interface

- O botão **"Finalizar votação"** usa uma cor diferente dos botões de navegação para evitar confusão com a ação de **"Próximo"**.
- Na tela de resultados parciais, o cabeçalho mantém título e ícone alinhados, os cards aparecem sem barra lateral de scroll, e os CTAs **"Adicionar voto"** e **"Finalizar votação"** ficam centralizados e empilhados com mais respiro vertical, seguindo a paleta azul/laranja e o raio padrão de botões definidos no tema.
- Ao tentar encerrar a sessão de votação, a aplicação usa o diálogo nativo de confirmação do sistema antes de concluir a ação.

## Estrutura do projeto

```
projeto-a3/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências Python
├── app/
│   ├── config/             # Configurações e tema da interface
│   ├── controllers/        # Orquestração entre views e serviços
│   ├── data/               # Perguntas e destinos
│   ├── gui/                # Janela principal e navegação
│   ├── models/             # Modelos de sessão e voto
│   ├── repositories/       # Persistência em CSV
│   ├── services/           # Regras de negócio
│   └── views/              # Telas e componentes visuais
├── assets/images/          # Ícones e imagens dos destinos
└── storage/sessions/       # Arquivos CSV gerados pelas sessões
```

## Dados e persistência

- Os votos de cada sessão são salvos em `storage/sessions/<nome_da_sessao>.csv`.
- As imagens ficam em `assets/images/` e são referenciadas pelos dados em `app/data/votes_data.py`.
