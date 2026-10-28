<p align="center">
  <img src="assets/header.png" alt="Team Sprint Demo — Mediação de conflitos" width="100%">
</p>

<h1 align="center">Conflict Simulation</h1>

<p align="center">
  Um jogo interativo em que <strong>você é o mediador</strong> de um conflito no ambiente de trabalho.
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README_fr.md">Français</a> · <strong href="README_pt-BR.md">Português</strong> 
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="Streamlit" src="https://img.shields.io/badge/built%20with-Streamlit-FF4B4B">
</p>

---

## Sumário

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Como jogar](#como-jogar)
- [Primeiros passos](#primeiros-passos)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Criando seu próprio cenário](#criando-seu-próprio-cenário)
- [Como contribuir](#como-contribuir)
- [Licença](#licença)
- [Autor](#autor)

## Sobre

O **Conflict Simulation** é um pequeno jogo de interpretação que roda no navegador, desenvolvido com [Streamlit](https://streamlit.io/). Ele coloca você no meio de uma discussão tensa entre dois colegas de equipe e pede que você acalme a situação — uma mensagem de cada vez.

O cenário incluído, **"Demo Deadline Conflict"** (conflito sobre o prazo da demonstração), se passa no dia de uma apresentação para os stakeholders:

- **Alex** prometeu a demonstração do dashboard para hoje e se sente pego de surpresa.
- **Sam** se recusa a entregar algo com defeito depois que os requisitos mudaram três vezes.

Sua missão é conduzir os dois a um plano comum e realista, sem tomar partido. É uma forma leve de praticar habilidades de mediação e comunicação: escuta ativa, reformulação, alinhamento de escopo e definição de acordos de trabalho claros.

> **Observação:** a interface e os diálogos do jogo estão atualmente em inglês.

## Funcionalidades

- 🎭 **Escolhas de mediação ramificadas** — três respostas possíveis a cada rodada, cada uma com um impacto diferente.
- 📊 **Indicadores em tempo real** — acompanhe como a tensão e a confiança de cada pessoa em você mudam após cada decisão.
- 💬 **Transcrição em estilo de chat** — toda a conversa é exibida com avatares para Alex, Sam e você.
- 🏁 **Condições de vitória e derrota** — desarme o conflito ou veja tudo desmoronar.
- 🔄 **Botões de Reiniciar e Encerrar** — jogue de novo para testar outras estratégias.
- 🧩 **Cenário orientado a dados** — diálogos, pontuação e regras ficam em um único dicionário Python, então você pode criar seu próprio cenário sem mexer na lógica do jogo.

## Como jogar

1. Leia o que Alex e Sam dizem na rodada atual.
2. Escolha uma das três mensagens de mediação (**A**, **B** ou **C**).
3. Sua escolha atualiza os indicadores e a próxima rodada começa.

O jogo tem **8 rodadas** no total. Cada escolha é avaliada nos bastidores:

| Qualidade da escolha | Tensão | Confiança (Alex) | Confiança (Sam) |
|----------------------|:------:|:----------------:|:---------------:|
| Melhor               | −15    | +10              | +10             |
| Média                | −5     | +3               | +3              |
| Ruim                 | +10    | −5               | −5              |

Você começa com **Tensão 50** e **Confiança 55** com cada pessoa. Todos os valores ficam entre 0 e 100.

O estado do jogo é verificado após cada escolha:

- ✅ **Você vence** quando a tensão está em **20 ou menos** e a confiança de **ambos**, Alex e Sam, está em **70 ou mais**.
- ❌ **Você perde** quando a tensão chega a **85 ou mais**, ou quando a confiança de **qualquer um** dos dois cai para **20 ou menos**.
- Se nenhuma das duas situações acontecer, o jogo termina após a última rodada e mostra suas estatísticas finais.

> **Dica:** boas respostas de mediação costumam ser neutras, esclarecem o que cada pessoa realmente precisa e transformam a discussão em acordos concretos e compartilhados.

## Primeiros passos

### Pré-requisitos

- [Python](https://www.python.org/downloads/) 3.9 ou mais recente
- `pip`

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/eduardodacostasoares/conflict_simulation.git
cd conflict_simulation

# 2. (Opcional) Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # No Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### Executando o app

```bash
streamlit run app.py
```

O Streamlit abrirá o jogo no seu navegador, normalmente em <http://localhost:8501>.

> **Observação:** execute o comando a partir da pasta raiz do projeto — o app carrega as imagens da pasta `assets/` usando caminhos relativos.
>
> Se aparecer um erro mencionando `chat_message` ou `use_container_width`, sua versão do Streamlit está desatualizada. Atualize com `pip install --upgrade streamlit`.

## Estrutura do projeto

```
conflict_simulation/
├── app.py              # App Streamlit: dados do cenário, lógica do jogo e interface
├── requirements.txt    # Dependências Python
└── assets/             # Imagens usadas pelo app
    ├── header.png      # Banner exibido no topo da página
    ├── alex.png        # Avatar de Alex
    ├── sam.png         # Avatar de Sam
    ├── mediator.png    # Seu avatar (o mediador)
    └── good.png
```

## Criando seu próprio cenário

Todo o conteúdo do jogo é definido no dicionário `SCENARIO`, no início do arquivo `app.py`:

| Chave            | O que controla                                                           |
|------------------|--------------------------------------------------------------------------|
| `title`          | Título da página, exibido no navegador e no topo do app                  |
| `initial_state`  | Valores iniciais de tensão e confiança                                   |
| `scoring`        | Quanto cada nível (`best`, `medium`, `bad`) altera os indicadores        |
| `end_conditions` | Limites para vitória e derrota                                           |
| `turns`          | A lista de rodadas: o que Alex e Sam dizem e as três opções de escolha   |

Cada rodada segue este formato:

```python
{
    "alex": "O que Alex diz nesta rodada.",
    "sam": "O que Sam diz nesta rodada.",
    "choices": [
        {"id": "A", "text": "Uma mensagem de mediação.", "grade": "best"},
        {"id": "B", "text": "Outra opção.",              "grade": "medium"},
        {"id": "C", "text": "Uma opção ruim.",           "grade": "bad"},
    ],
},
```

Edite os diálogos, adicione ou remova rodadas, ou ajuste a pontuação e os limites para criar um novo desafio. Para trocar a aparência dos personagens, substitua as imagens da pasta `assets/`.

## Como contribuir

Contribuições, ideias e novos cenários são muito bem-vindos!

1. Faça um fork do repositório.
2. Crie uma branch para sua alteração: `git checkout -b meu-novo-cenario`
3. Faça o commit das alterações: `git commit -m "Adiciona um novo cenário"`
4. Envie a branch: `git push origin meu-novo-cenario`
5. Abra um pull request.

Encontrou um bug ou tem uma sugestão? [Abra uma issue](https://github.com/eduardodacostasoares/conflict_simulation/issues).

## Licença

Este projeto ainda não tem uma licença definida. Até que uma seja adicionada, todos os direitos são reservados ao autor. Entre em contato com o autor antes de reutilizar o código.

## Autor

**Eduardo da Costa Soares** — [@eduardodacostasoares](https://github.com/eduardodacostasoares)

Se você gostou do projeto, considere deixar uma ⭐ no GitHub!
