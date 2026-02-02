import streamlit as st
from PIL import Image
import io

st.set_page_config(
    page_title="Redimensionador de Imagens",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Redimensionador de Imagens")
st.markdown("Redimensione suas imagens por porcentagem mantendo a proporção original")

# Upload de imagem
uploaded_file = st.file_uploader(
    "Faça upload de uma imagem",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
    help="Formatos suportados: PNG, JPG, JPEG, GIF, BMP, WEBP"
)

if uploaded_file is not None:
    # Carregar imagem
    try:
        image = Image.open(uploaded_file)
        original_format = image.format or 'PNG'
        
        # Mostrar informações da imagem original
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Imagem Original")
            st.image(image, caption=f"Tamanho original: {image.width} x {image.height} pixels", use_container_width=True)
            st.info(f"**Formato:** {original_format}\n\n**Dimensões:** {image.width} x {image.height} pixels")
        
        # Controles de redimensionamento
        st.subheader("⚙️ Configurações de Redimensionamento")
        
        col_percent, col_size = st.columns(2)
        
        with col_percent:
            percent = st.slider(
                "Porcentagem de redimensionamento (%)",
                min_value=1,
                max_value=500,
                value=100,
                step=1,
                help="100% = tamanho original, 50% = metade do tamanho, 200% = dobro do tamanho"
            )
        
        with col_size:
            new_width = int(image.width * percent / 100)
            new_height = int(image.height * percent / 100)
            st.metric("Novo tamanho", f"{new_width} x {new_height} pixels")
        
        # Redimensionar imagem
        if percent != 100:
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            with col2:
                st.subheader("✨ Imagem Redimensionada")
                st.image(resized_image, caption=f"Tamanho redimensionado: {new_width} x {new_height} pixels", use_container_width=True)
                st.success(f"**Dimensões:** {new_width} x {new_height} pixels\n\n**Redimensionamento:** {percent}%")
            
            # Preparar imagem para download
            img_buffer = io.BytesIO()
            
            # Manter o formato original ou converter para PNG se necessário
            save_format = original_format
            if original_format == 'JPEG':
                save_format = 'JPEG'
            elif original_format == 'PNG':
                save_format = 'PNG'
            else:
                save_format = 'PNG'  # Padrão para outros formatos
            
            resized_image.save(img_buffer, format=save_format, quality=95)
            img_buffer.seek(0)
            
            # Botão de download
            st.subheader("💾 Download")
            st.download_button(
                label=f"⬇️ Baixar imagem redimensionada ({new_width}x{new_height})",
                data=img_buffer,
                file_name=f"redimensionada_{percent}porcento.{save_format.lower()}",
                mime=f"image/{save_format.lower()}",
                type="primary"
            )
        else:
            with col2:
                st.info("Ajuste a porcentagem para ver a imagem redimensionada")
    except Exception as e:
        st.error(f"Erro ao processar a imagem: {str(e)}")
        st.info("Por favor, verifique se o arquivo é uma imagem válida.")
else:
    st.info("👆 Faça upload de uma imagem para começar a redimensionar")
    
    # Exemplo de uso
    with st.expander("ℹ️ Como usar"):
        st.markdown("""
        1. **Faça upload** de uma imagem usando o botão acima
        2. **Ajuste a porcentagem** usando o slider (1% a 500%)
        3. **Visualize** a imagem redimensionada ao lado
        4. **Baixe** a imagem redimensionada usando o botão de download
        
        **Dicas:**
        - 50% = metade do tamanho original
        - 100% = tamanho original
        - 200% = dobro do tamanho original
        - A proporção da imagem é sempre mantida
        """)
