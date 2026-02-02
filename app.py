import streamlit as st
from PIL import Image
import io

st.set_page_config(
    page_title="Redimensionador de Imagens",
    page_icon="🖼️",
    layout="wide"
)

# Dicionário com dimensões das redes sociais
SOCIAL_MEDIA_PRESETS = {
    "Instagram": {
        "Feed (Post Quadrado)": (1080, 1080),
        "Feed (Post Retrato)": (1080, 1350),
        "Feed (Post Paisagem)": (1080, 566),
        "Stories": (1080, 1920),
        "Reels": (1080, 1920),
        "IGTV/Cover": (1080, 1920),
        "Perfil": (320, 320)
    },
    "Facebook": {
        "Post no Feed": (1200, 630),
        "Post Quadrado": (1200, 1200),
        "Capa": (1640, 859),
        "Perfil": (400, 400),
        "Stories": (1080, 1920),
        "Evento": (1920, 1080)
    },
    "Twitter/X": {
        "Post com Imagem": (1200, 675),
        "Post Quadrado": (1200, 1200),
        "Header": (1500, 500),
        "Perfil": (400, 400)
    },
    "LinkedIn": {
        "Post no Feed": (1200, 627),
        "Post Quadrado": (1200, 1200),
        "Capa": (1584, 396),
        "Perfil": (400, 400),
        "Banner de Empresa": (1128, 191)
    },
    "TikTok": {
        "Vídeo/Post": (1080, 1920),
        "Perfil": (200, 200)
    },
    "YouTube": {
        "Thumbnail": (1280, 720),
        "Banner": (2560, 1440),
        "Perfil": (800, 800)
    },
    "Pinterest": {
        "Pin Padrão": (1000, 1500),
        "Pin Quadrado": (1000, 1000),
        "Pin Longo": (1000, 2100)
    },
    "WhatsApp": {
        "Status": (1080, 1920),
        "Perfil": (640, 640)
    }
}

st.title("🖼️ Redimensionador de Imagens")
st.markdown("Redimensione suas imagens usando presets de redes sociais, por porcentagem ou definindo dimensões personalizadas")

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
            ["Presets de Redes Sociais", "Por Porcentagem", "Dimensões Manuais"],
            horizontal=True,
            help="Presets: dimensões prontas para redes sociais. Por Porcentagem: mantém a proporção. Dimensões Manuais: defina largura e altura específicas."
        )
        
        new_width = image.width
        new_height = image.height
        percent = 100
        selected_social = None
        selected_preset = None
        
        if resize_mode == "Presets de Redes Sociais":
            # Seleção de rede social
            col_social1, col_social2 = st.columns(2)
            
            with col_social1:
                selected_social = st.selectbox(
                    "🌐 Escolha a rede social:",
                    options=list(SOCIAL_MEDIA_PRESETS.keys()),
                    help="Selecione a rede social para ver as dimensões disponíveis"
                )
            
            if selected_social:
                # Seleção do tipo de conteúdo
                with col_social2:
                    preset_options = list(SOCIAL_MEDIA_PRESETS[selected_social].keys())
                    selected_preset = st.selectbox(
                        "📐 Escolha o tipo de conteúdo:",
                        options=preset_options,
                        help="Selecione o tipo de conteúdo para aplicar as dimensões recomendadas"
                    )
                
                if selected_preset:
                    # Aplicar dimensões do preset
                    preset_width, preset_height = SOCIAL_MEDIA_PRESETS[selected_social][selected_preset]
                    new_width = preset_width
                    new_height = preset_height
                    
                    # Calcular porcentagem equivalente
                    if new_width != image.width:
                        percent = int((new_width / image.width) * 100)
                    elif new_height != image.height:
                        percent = int((new_height / image.height) * 100)
                    else:
                        percent = 100
                    
                    # Mostrar informações do preset
                    st.info(f"📏 **Dimensões para {selected_social} - {selected_preset}:** {preset_width} x {preset_height} pixels")
                    
                    # Opção para ajustar manualmente se necessário
                    adjust_manual = st.checkbox(
                        "Ajustar dimensões manualmente",
                        help="Marque para ajustar as dimensões do preset manualmente"
                    )
                    
                    if adjust_manual:
                        col_adj_width, col_adj_height = st.columns(2)
                        with col_adj_width:
                            new_width = st.number_input(
                                "Largura (pixels)",
                                min_value=1,
                                max_value=10000,
                                value=preset_width,
                                step=1
                            )
                        with col_adj_height:
                            new_height = st.number_input(
                                "Altura (pixels)",
                                min_value=1,
                                max_value=10000,
                                value=preset_height,
                                step=1
                            )
        
        elif resize_mode == "Por Porcentagem":
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
        
        # Método de redimensionamento (apenas se as dimensões forem diferentes)
        resize_method = "Distorcer"  # Padrão
        resized_image = None
        
        if new_width != image.width or new_height != image.height:
            # Calcular proporções
            original_ratio = image.width / image.height
            target_ratio = new_width / new_height
            
            # Se as proporções forem diferentes, oferecer opções
            if abs(original_ratio - target_ratio) > 0.01:  # Tolerância para diferenças pequenas
                resize_method = st.radio(
                    "⚠️ As proporções são diferentes. Como deseja redimensionar?",
                    ["Distorcer", "Cortar (Crop)", "Adicionar barras (Padding)"],
                    horizontal=True,
                    help="Distorcer: estica a imagem. Cortar: mantém proporção cortando partes. Padding: adiciona barras para manter proporção."
                )
            else:
                # Proporções iguais, apenas redimensionar normalmente
                resize_method = "Distorcer"
            
            # Aplicar método de redimensionamento
            if resize_method == "Distorcer":
                resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            elif resize_method == "Cortar (Crop)":
                # Calcular escala para manter proporção e preencher o tamanho alvo
                scale = max(new_width / image.width, new_height / image.height)
                scaled_width = int(image.width * scale)
                scaled_height = int(image.height * scale)
                
                # Redimensionar mantendo proporção
                temp_image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
                
                # Calcular posição para centralizar o crop
                left = (scaled_width - new_width) // 2
                top = (scaled_height - new_height) // 2
                right = left + new_width
                bottom = top + new_height
                
                # Cortar a imagem
                resized_image = temp_image.crop((left, top, right, bottom))
            else:  # Padding
                # Calcular escala para manter proporção e caber no tamanho alvo
                scale = min(new_width / image.width, new_height / image.height)
                scaled_width = int(image.width * scale)
                scaled_height = int(image.height * scale)
                
                # Redimensionar mantendo proporção
                temp_image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
                
                # Converter para RGBA se necessário para suportar transparência
                if temp_image.mode != 'RGBA':
                    temp_image = temp_image.convert('RGBA')
                
                # Criar imagem com fundo transparente
                resized_image = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
                
                # Centralizar a imagem redimensionada
                paste_x = (new_width - scaled_width) // 2
                paste_y = (new_height - scaled_height) // 2
                
                # Colar a imagem mantendo transparência
                resized_image.paste(temp_image, (paste_x, paste_y), temp_image)
            
            # Mostrar resultado
            with col2:
                st.subheader("✨ Imagem Redimensionada")
                st.image(resized_image, caption=f"Tamanho redimensionado: {new_width} x {new_height} pixels", use_container_width=True)
                
                # Mensagem com método usado
                method_text = ""
                if resize_method == "Cortar (Crop)":
                    method_text = "\n\n**Método:** Cortar (mantém proporção)"
                elif resize_method == "Adicionar barras (Padding)":
                    method_text = "\n\n**Método:** Padding (mantém proporção com barras)"
                else:
                    method_text = "\n\n**Método:** Redimensionar (pode distorcer)"
                
                st.success(f"**Dimensões:** {new_width} x {new_height} pixels\n\n**Redimensionamento:** {percent}%{method_text}")
            
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
            if resize_mode == "Presets de Redes Sociais" and selected_social and selected_preset:
                safe_social = selected_social.lower().replace("/", "_").replace(" ", "_")
                safe_preset = selected_preset.lower().replace("/", "_").replace(" ", "_")
                file_name = f"{safe_social}_{safe_preset}_{new_width}x{new_height}.{save_format.lower()}"
            elif resize_mode == "Por Porcentagem":
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
                if resize_mode == "Presets de Redes Sociais":
                    st.info("Selecione uma rede social e tipo de conteúdo para ver a imagem redimensionada")
                elif resize_mode == "Por Porcentagem":
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
        ### Modo Presets de Redes Sociais:
        1. **Faça upload** de uma imagem usando o botão acima
        2. Selecione **"Presets de Redes Sociais"**
        3. **Escolha a rede social** (Instagram, Facebook, Twitter, etc.)
        4. **Escolha o tipo de conteúdo** (Feed, Stories, Perfil, etc.)
        5. As dimensões serão aplicadas automaticamente
        6. **Visualize** e **baixe** a imagem redimensionada
        
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
        - **Presets**: Dimensões otimizadas para cada rede social
        - **Por Porcentagem**: 50% = metade, 100% = original, 200% = dobro
        - **Dimensões Manuais**: Controle total sobre largura e altura
        - A proporção pode ser mantida ou alterada conforme sua escolha
        """)
