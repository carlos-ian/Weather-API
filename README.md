# 🌤️ Weather API

Um projeto pessoal simples que consiste em consultas meteorológicas que integra uma API de clima em tempo real com um sistema completo de gerenciamento de histórico e autenticação de usuários. O objetivo do projeto é treinar as operações CRUD, Autenticação e Autorização utilizando OpenWeather API.

---

## 📝 Sobre o Projeto

O projeto permite que usuários se cadastrem e realizem consultas de condições climáticas de qualquer cidade do mundo. O diferencial do projeto é a persistência de dados, onde as últimas 3 pesquisas de cada usuário são armazenadas em um banco de dados relacional, permitindo a atualização dos dados diretamente da API ou a exclusão do registro.

---

## 🚀 Funcionalidades

### 🔐 Autenticação e Segurança
* **Cadastro de Usuários:** Criação de conta com criptografia de senha (`bcrypt`).
* **Login JWT:** Autenticação baseada em tokens para proteger as rotas de busca.

### ☁️ Consulta e Clima
* **Busca em Tempo Real:** Integração com OpenWeather API para obter temperatura, sensação térmica e probabilidade de chuva.
* **Geocodificação:** Conversão automática de nomes de cidades em coordenadas (Lat/Lon).

### 📊 Gerenciamento de Histórico (CRUD)
* **Registro Automático:** Cada busca bem-sucedida é salva no histórico do usuário.
* **Visualização Limitada:** Exibição inteligente das últimas 3 pesquisas realizadas.
* **Update via API:** Botão para atualizar um registro antigo com os dados climáticos do momento atual.
* **Exclusão:** Remoção individual de itens do histórico.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python / FastAPI |
| **Banco de Dados** | PostgreSQL / SQLAlchemy (ORM) |
| **Frontend** | HTML5 / CSS3 / JavaScript |
| **Servidor** | Uvicorn |

---

## 📁 Estrutura de Pastas

```text
Weather-API/
├── frontend/          # Arquivos HTML (login.html, index.html)
├── src/               # Código fonte (main, routes, models, services)
├── venv/              # Ambiente Virtual Python
├── requirements.txt   # Dependências do sistema
└── README.md          # Documentação do projeto
