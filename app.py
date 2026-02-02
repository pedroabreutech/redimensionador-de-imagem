import streamlit as st
from PIL import Image
import io

st.set_page_config(
    page_title="Redimensionador de Imagens",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Redimensionador de Imagens")
st.markdown("Redimensione suas imagens por porcentagem ou definindo dimensões personalizadas")

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
        
        # Seleção do modo de redimensionamento
        resize_mode = st.radio(
            "Escolha o modo de redimensionamento:",
            ["Por Porcentagem", "Dimensões Manuais"],
            horizontal=True,
            help="Por Porcentagem: mantém a proporção. Dimensões Manuais: defina largura e altura específicas."
        )
        
        new_width = image.width
        new_height = image.height
        percent = 100
        
        if resize_mode == "Por Porcentagem":
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
        else:
            # Modo manual
            col_manual1, col_manual2, col_manual3 = st.columns(3)
            
            with col_manual1:
                st.write("**Dimensões Originais:**")
                st.info(f"Largura: {image.width}px\n\nAltura: {image.height}px")
            
            with col_manual2:
                maintain_ratio = st.checkbox(
                    "Manter proporção",
                    value=True,
                    help="Se marcado, ao alterar uma dimensão, a outra será ajustada automaticamente"
                )
            
            with col_manual3:
                st.write("**Novas Dimensões:**")
            
            col_width, col_height = st.columns(2)
            
            with col_width:
                manual_width = st.number_input(
                    "Largura (pixels)",
                    min_value=1,
                    max_value=10000,
                    value=image.width,
                    step=1,
                    help="Digite a largura desejada em pixels"
                )
            
            with col_height:
                if maintain_ratio:
                    # Calcular altura proporcional
                    ratio = image.height / image.width
                    calculated_height = int(manual_width * ratio)
                    st.write("**Altura (pixels):**")
                    st.info(f"{calculated_height}px\n\n*Calculada automaticamente para manter a proporção*")
                    manual_height = calculated_height
                else:
                    manual_height = st.number_input(
                        "Altura (pixels)",
                        min_value=1,
                        max_value=10000,
                        value=image.height,
                        step=1,
                        help="Digite a altura desejada em pixels"
                    )
            
            new_width = int(manual_width)
            new_height = int(manual_height)
            
            # Calcular porcentagem equivalente para exibição
            if new_width != image.width:
                percent = int((new_width / image.width) * 100)
            elif new_height != image.height:
                percent = int((new_height / image.height) * 100)
            else:
                percent = 100
        
        # Redimensionar imagem
        if new_width != image.width or new_height != image.height:
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
            if resize_mode == "Por Porcentagem":
                file_name = f"redimensionada_{percent}porcento.{save_format.lower()}"
            else:
                file_name = f"redimensionada_{new_width}x{new_height}.{save_format.lower()}"
            
            st.download_button(
                label=f"⬇️ Baixar imagem redimensionada ({new_width}x{new_height})",
                data=img_buffer,
                file_name=file_name,
                mime=f"image/{save_format.lower()}",
                type="primary"
            )
        else:
            with col2:
                if resize_mode == "Por Porcentagem":
                    st.info("Ajuste a porcentagem para ver a imagem redimensionada")
                else:
                    st.info("Ajuste as dimensões para ver a imagem redimensionada")
    except Exception as e:
        st.error(f"Erro ao processar a imagem: {str(e)}")
        st.info("Por favor, verifique se o arquivo é uma imagem válida.")
else:
    st.info("👆 Faça upload de uma imagem para começar a redimensionar")
    
    # Exemplo de uso
    with st.expander("ℹ️ Como usar"):
        st.markdown("""
        ### Modo Por Porcentagem:
        1. **Faça upload** de uma imagem usando o botão acima
        2. Selecione **"Por Porcentagem"**
        3. **Ajuste a porcentagem** usando o slider (1% a 500%)
        4. **Visualize** a imagem redimensionada ao lado
        5. **Baixe** a imagem redimensionada
        
        ### Modo Dimensões Manuais:
        1. **Faça upload** de uma imagem usando o botão acima
        2. Selecione **"Dimensões Manuais"**
        3. **Digite** a largura e altura desejadas em pixels
        4. Marque **"Manter proporção"** para ajuste automático
        5. **Visualize** e **baixe** a imagem redimensionada
        
        **Dicas:**
        - **Por Porcentagem**: 50% = metade, 100% = original, 200% = dobro
        - **Dimensões Manuais**: Controle total sobre largura e altura
        - A proporção pode ser mantida ou alterada conforme sua escolha
        """)
