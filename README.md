# Sistema Almoxarifado - Entrada de Notas Fiscais

Este projeto é uma aplicação web simples desenvolvida com Flask para facilitar a entrada de notas fiscais de materiais em um sistema de almoxarifado. Os dados inseridos através do formulário são enviados diretamente para uma planilha do Google Sheets, proporcionando uma forma eficiente de registrar e gerenciar o estoque.

## Funcionalidades

-   **Formulário Web Intuitivo**: Interface amigável para inserção de dados de notas fiscais.
-   **Adição Dinâmica de Itens**: Capacidade de adicionar múltiplos itens de material a uma única nota fiscal.
-   **Integração com Google Sheets**: Envio automático dos dados do formulário para uma planilha Google Sheets configurada via Google Apps Script.
-   **Visualização em Tempo Real**: Link direto para a planilha do Google Sheets para acompanhamento em tempo real.
-   **Validação Básica**: Campos obrigatórios para garantir a integridade dos dados.

## Tecnologias Utilizadas

-   **Backend**: Python 3, Flask
-   **Frontend**: HTML5, CSS3, JavaScript
-   **Integração**: `requests` (Python), Google Apps Script (para a planilha)

  ## Estrutura do Projeto

```
.
├── app.py                  # Lógica principal da aplicação Flask
├── templates/
│   └── index.html          # Frontend da aplicação (formulário)
└── README.md               # Este arquivo
```

##Projeto desenvolvido para a Fleximedical/Kure
