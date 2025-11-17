✋🔤 Sistema de Reconhecimento de Libras com Jogo da Forca

Projeto desenvolvido para detectar letras do alfabeto em Libras usando visão computacional e integrar isso a um jogo da Forca interativo.

📌 📷 Sobre o Projeto

Este projeto combina inteligência artificial, visão computacional e interfaces gráficas para criar um sistema capaz de:

Identificar letras do alfabeto em Libras usando a posição da mão.

Interpretar movimentos e rotações da mão.

Reconhecer letras com base em:

estados dos dedos,

coordenadas dos pontos (landmarks),

trajetória passada da mão,

orientação (frente, diagonal, trás).

E usar essas letras diretamente em um Jogo da Forca feito em PyQt5.

É um projeto educacional que explora IA, acessibilidade e interação homem-máquina.

🧠 Tecnologias Utilizadas
Linguagem principal

Python 3.10

Visão Computacional

MediaPipe Hands

Para detectar a mão, os dedos e gerar os pontos (landmarks).

TensorFlow Lite

Usado como backend otimizado.

OpenCV

Leitura da webcam e manipulação das imagens.

Interface Gráfica

PyQt5

Criação de janelas, botões, labels, e exibição das imagens da forca.

Outros recursos

deque (collections)

Para armazenar trajetórias da mão.

Classes individuais para cada letra

Cada letra tem sua própria lógica dentro de detectar_letras().

Arquitetura escalável

Fácil adicionar novas letras ou gestos futuramente.

🎮 Como o sistema funciona
🖐️ 1. Detecção de mão

O MediaPipe detecta:

Pontas dos dedos

Dobramento (levantado, parcial, abaixado)

Rotação da mão (comparando landmarks 5 e 17)

Trajetória (movimentação da mão no tempo)

🔎 2. Classificação da letra

Cada letra tem sua própria classe, exemplo:

class letra_P(LetraBase):
    def detectar_letras(...):
        return (
            estados['indicador'] and
            estados['polegar'] and
            estados['medio_parcial'] and
            ...
        )


Algumas letras analisam:

Coordenadas x / y / z

Diferença entre dedos

Movimento da trajetória (como o X)

Rotação da palma da mão

🎲 3. Integração com o Jogo da Forca

Quando uma letra é detectada corretamente:

Ela é enviada ao jogo

Atualiza o estado da palavra

Atualiza a imagem da forca (forca_0.png, forca_1.png …)

Se errar, incrementa o contador de erros

Tudo em tempo real.

🧩 Recursos implementados

✔ Reconhecimento de letras estáticas
✔ Reconhecimento de letras com movimento (ex: X)
✔ Detecção de rotação horizontal da mão
✔ Detecção de dedos parcial / levantado / abaixado
✔ Jogo da Forca completo em PyQt5
✔ Atualização dinâmica de imagens
✔ Lógica modular e organizada em classes
✔ Fácil expansão (basta criar nova classe para cada letra)

🚀 Como executar o projeto
1. Instale as dependências
pip install mediapipe opencv-python PyQt5 tensorflow

2. Execute o sistema
python jogo.py


O jogo abrirá automaticamente, juntamente com a câmera.

📁 Estrutura do Projeto
📦 Projeto-Libras-Forca
│
├── jogo.py                  # Interface gráfica + integração
├── detector.py              # Lógicas de detecção e estados dos dedos
├── letras/
│   ├── letra_A.py
│   ├── letra_B.py
│   ├── letra_P.py
│   └── ...
│
├── imagens/
│   ├── forca_0.png
│   ├── forca_1.png
│   └── ...
│
└── README.md

🧪 Melhorias futuras

✨ Adicionar mais letras
✨ Treinar modelo TFLite personalizado
✨ Suporte para frases completas
✨ Modo acessibilidade
✨ Banco de palavras do jogo mais extenso
