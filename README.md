# 🖼️ Redimensionador de Imagens

Uma aplicação web simples e intuitiva para redimensionar imagens por porcentagem, desenvolvida com Streamlit.

## 🚀 Funcionalidades

- ✅ Upload de imagens em múltiplos formatos (PNG, JPG, JPEG, GIF, BMP, WEBP)
- ✅ **Presets de Redes Sociais** - Dimensões otimizadas para Instagram, Facebook, Twitter, LinkedIn, TikTok, YouTube, Pinterest e WhatsApp
- ✅ Redimensionamento por porcentagem (1% a 500%)
- ✅ Redimensionamento manual com dimensões personalizadas
- ✅ **Métodos de redimensionamento inteligentes:**
  - **Distorcer**: Estica/achata a imagem para preencher o espaço
  - **Cortar (Crop)**: Mantém proporção cortando partes da imagem
  - **Adicionar barras (Padding)**: Mantém proporção adicionando barras transparentes
- ✅ Preview da imagem original e redimensionada
- ✅ Download da imagem redimensionada
- ✅ Interface gráfica moderna e intuitiva

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/pedroabreutech/redimensionador-de-imagem.git
cd redimensionador-de-imagem
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🎯 Como usar

1. Execute a aplicação:
```bash
streamlit run app.py
```

2. A aplicação abrirá automaticamente no navegador (geralmente em `http://localhost:8501`)
3. Faça upload de uma imagem
4. Escolha o modo de redimensionamento:
   - **Presets de Redes Sociais**: Selecione a rede social e tipo de conteúdo
   - **Por Porcentagem**: Use o slider para ajustar o tamanho
   - **Dimensões Manuais**: Digite largura e altura em pixels
5. Se as proporções forem diferentes, escolha o método:
   - **Distorcer**: Para preencher todo o espaço (pode distorcer)
   - **Cortar (Crop)**: Para manter proporção cortando partes
   - **Adicionar barras (Padding)**: Para manter proporção com barras
6. Visualize o resultado
7. Baixe a imagem redimensionada

## 📋 Requisitos

- Python 3.7+
- Streamlit
- Pillow (PIL)

## 💡 Exemplos de uso

### Presets de Redes Sociais:
- **Instagram Stories**: 1080 x 1920 pixels
- **Facebook Post**: 1200 x 630 pixels
- **Twitter Header**: 1500 x 500 pixels
- E muitas outras opções para cada rede social!

### Por Porcentagem:
- **50%**: Reduz a imagem para metade do tamanho original
- **100%**: Mantém o tamanho original
- **200%**: Dobra o tamanho da imagem

### Métodos de Redimensionamento:
- Use **Distorcer** quando quiser preencher todo o espaço
- Use **Cortar** quando quiser manter a proporção (partes podem ser cortadas)
- Use **Padding** quando quiser manter a proporção sem perder conteúdo (barras serão adicionadas)
