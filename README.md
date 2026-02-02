# 🖼️ Redimensionador de Imagens

Uma aplicação web simples e intuitiva para redimensionar imagens por porcentagem, desenvolvida com Streamlit.

## 🚀 Funcionalidades

- ✅ Upload de imagens em múltiplos formatos (PNG, JPG, JPEG, GIF, BMP, WEBP)
- ✅ Redimensionamento por porcentagem (1% a 500%)
- ✅ Manutenção automática da proporção original
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
4. Ajuste a porcentagem de redimensionamento usando o slider
5. Visualize o resultado
6. Baixe a imagem redimensionada

## 📋 Requisitos

- Python 3.7+
- Streamlit
- Pillow (PIL)

## 💡 Exemplos de uso

- **50%**: Reduz a imagem para metade do tamanho original
- **100%**: Mantém o tamanho original
- **200%**: Dobra o tamanho da imagem
