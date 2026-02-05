import streamlit as st
from PIL import Image
import io
import json
import numpy as np
from streamlit_drawable_canvas import st_canvas

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

# Menu lateral
st.sidebar.title("⚙️ Configurações")

# Upload de imagem (menu lateral)
uploaded_file = st.sidebar.file_uploader(
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
        
        # Controles de redimensionamento (menu lateral)
        st.sidebar.subheader("⚙️ Configurações de Redimensionamento")
        
        # Seleção do modo de redimensionamento (menu lateral)
        resize_mode = st.sidebar.radio(
            "Escolha o modo de redimensionamento:",
            ["Presets de Redes Sociais", "Por Porcentagem", "Dimensões Manuais"],
            help="Presets: dimensões prontas para redes sociais. Por Porcentagem: mantém a proporção. Dimensões Manuais: defina largura e altura específicas."
        )
        
        new_width = image.width
        new_height = image.height
        percent = 100
        selected_social = None
        selected_preset = None
        
        # Todas as opções de configuração ficam no menu lateral
        if resize_mode == "Presets de Redes Sociais":
            # Seleção de rede social (lateral)
            selected_social = st.sidebar.selectbox(
                "🌐 Escolha a rede social:",
                options=list(SOCIAL_MEDIA_PRESETS.keys()),
                help="Selecione a rede social para ver as dimensões disponíveis"
            )
            
            if selected_social:
                # Seleção do tipo de conteúdo (lateral)
                preset_options = list(SOCIAL_MEDIA_PRESETS[selected_social].keys())
                selected_preset = st.sidebar.selectbox(
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
                    
                    # Mostrar informações do preset (lateral)
                    st.sidebar.info(f"📏 **Dimensões para {selected_social} - {selected_preset}:** {preset_width} x {preset_height} pixels")
                    
                    # Opção para ajustar manualmente se necessário (lateral)
                    adjust_manual = st.sidebar.checkbox(
                        "Ajustar dimensões manualmente",
                        help="Marque para ajustar as dimensões do preset manualmente"
                    )
                    
                    if adjust_manual:
                        new_width = st.sidebar.number_input(
                            "Largura (pixels)",
                            min_value=1,
                            max_value=10000,
                            value=preset_width,
                            step=1
                        )
                        new_height = st.sidebar.number_input(
                            "Altura (pixels)",
                            min_value=1,
                            max_value=10000,
                            value=preset_height,
                            step=1
                        )
        
        elif resize_mode == "Por Porcentagem":
            # Slider de porcentagem no menu lateral
            percent = st.sidebar.slider(
                "Porcentagem de redimensionamento (%)",
                min_value=1,
                max_value=500,
                value=100,
                step=1,
                help="100% = tamanho original, 50% = metade do tamanho, 200% = dobro do tamanho"
            )
            
            # Cálculo do novo tamanho exibido ao lado da imagem
            new_width = int(image.width * percent / 100)
            new_height = int(image.height * percent / 100)
            st.metric("Novo tamanho", f"{new_width} x {new_height} pixels")
        else:
            # Modo manual (menu lateral)
            st.sidebar.markdown("**Dimensões Originais:**")
            st.sidebar.info(f"Largura: {image.width}px\n\nAltura: {image.height}px")
            
            maintain_ratio = st.sidebar.checkbox(
                "Manter proporção",
                value=True,
                help="Se marcado, ao alterar uma dimensão, a outra será ajustada automaticamente"
            )
            
            manual_width = st.sidebar.number_input(
                "Largura (pixels)",
                min_value=1,
                max_value=10000,
                value=image.width,
                step=1,
                help="Digite a largura desejada em pixels"
            )
            
            if maintain_ratio:
                # Calcular altura proporcional
                ratio = image.height / image.width
                calculated_height = int(manual_width * ratio)
                st.sidebar.markdown("**Altura (pixels):**")
                st.sidebar.info(f"{calculated_height}px\n\n*Calculada automaticamente para manter a proporção*")
                manual_height = calculated_height
            else:
                manual_height = st.sidebar.number_input(
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
                st.markdown("**✂️ Selecione a área de corte diretamente na imagem:**")
                st.info("💡 **Como usar:** Clique e arraste na imagem abaixo para selecionar a área que deseja cortar. A área selecionada será redimensionada para as dimensões desejadas.")
                
                # Calcular escala para manter proporção e preencher o tamanho alvo
                scale = max(new_width / image.width, new_height / image.height)
                scaled_width = int(image.width * scale)
                scaled_height = int(image.height * scale)
                
                # Redimensionar mantendo proporção
                temp_image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
                
                # Calcular dimensões do canvas (limitar a 800px de largura para melhor UX)
                canvas_width = min(800, scaled_width)
                canvas_height = int(canvas_width * scaled_height / scaled_width)
                
                # Redimensionar a imagem para o tamanho do canvas para exibição
                display_image = temp_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                
                # Converter para RGB se necessário (st_canvas funciona melhor com RGB)
                if display_image.mode != 'RGB':
                    display_image = display_image.convert('RGB')
                
                # Criar uma cópia nova da imagem para evitar problemas de referência
                canvas_bg_image = Image.new('RGB', (canvas_width, canvas_height))
                canvas_bg_image.paste(display_image, (0, 0))
                
                # Canvas para seleção - usar apenas o canvas, sem fallback
                canvas_result = st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",
                    stroke_width=2,
                    stroke_color="#FF6600",
                    background_image=canvas_bg_image,
                    update_streamlit=True,
                    width=canvas_width,
                    height=canvas_height,
                    drawing_mode="rect",
                    point_display_radius=0,
                    key=f"crop_canvas_{new_width}_{new_height}",
                )
                
                # Processar seleção do canvas
                if canvas_result.json_data is not None:
                    objects = json.loads(canvas_result.json_data)
                    
                    # Procurar por retângulos desenhados
                    crop_rect = None
                    if "objects" in objects:
                        for obj in objects["objects"]:
                            if obj.get("type") == "rect":
                                crop_rect = obj
                                break
                    
                    if crop_rect:
                        # Obter coordenadas do retângulo no canvas
                        canvas_x = crop_rect.get("left", 0)
                        canvas_y = crop_rect.get("top", 0)
                        canvas_w = crop_rect.get("width", 0)
                        canvas_h = crop_rect.get("height", 0)
                        
                        # Converter coordenadas do canvas para coordenadas da imagem real
                        scale_x = scaled_width / canvas_width
                        scale_y = scaled_height / canvas_height
                        
                        # Se o usuário desenhou um retângulo válido, usar o centro da seleção
                        if canvas_w > 10 and canvas_h > 10:
                            # Calcular o centro da seleção do usuário
                            canvas_center_x = canvas_x + canvas_w / 2
                            canvas_center_y = canvas_y + canvas_h / 2
                            
                            # Converter para coordenadas da imagem real
                            real_center_x = canvas_center_x * scale_x
                            real_center_y = canvas_center_y * scale_y
                            
                            # Calcular posição do crop centrado na seleção do usuário
                            left = int(real_center_x - new_width / 2)
                            top = int(real_center_y - new_height / 2)
                            
                            # Garantir que não exceda os limites da imagem
                            left = max(0, min(left, scaled_width - new_width))
                            top = max(0, min(top, scaled_height - new_height))
                            right = left + new_width
                            bottom = top + new_height
                            
                            # Cortar a imagem usando a posição baseada na seleção do usuário
                            resized_image = temp_image.crop((left, top, right, bottom))
                        else:
                            # Seleção muito pequena, usar crop centralizado padrão
                            left = (scaled_width - new_width) // 2
                            top = (scaled_height - new_height) // 2
                            right = left + new_width
                            bottom = top + new_height
                            resized_image = temp_image.crop((left, top, right, bottom))
                    else:
                        # Nenhuma seleção, usar crop centralizado padrão
                        left = (scaled_width - new_width) // 2
                        top = (scaled_height - new_height) // 2
                        right = left + new_width
                        bottom = top + new_height
                        resized_image = temp_image.crop((left, top, right, bottom))
                else:
                    # Nenhuma seleção ainda, usar crop centralizado padrão
                    left = (scaled_width - new_width) // 2
                    top = (scaled_height - new_height) // 2
                    right = left + new_width
                    bottom = top + new_height
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
            
            # Escolha do formato de saída no menu lateral
            output_format_option = st.sidebar.selectbox(
                "Formato de saída",
                ["Manter formato original", "JPEG", "PNG", "WEBP"],
                help="Escolha o formato do arquivo final."
            )
            
            # Definir formato a ser usado
            if output_format_option == "Manter formato original":
                # Manter o formato original, com fallback para PNG
                save_format = original_format if original_format in ["JPEG", "PNG", "WEBP"] else "PNG"
            else:
                save_format = output_format_option
            
            # Ajustar modo da imagem para formatos que não suportam transparência (ex.: JPEG)
            if save_format == "JPEG" and resized_image.mode in ["RGBA", "LA", "P"]:
                resized_image = resized_image.convert("RGB")
            
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

# -------------------------------------------------------------
# Conversor de arquivos de imagem (ferramenta independente)
# -------------------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.subheader("🗂 Conversor de Imagens")

converter_file = st.sidebar.file_uploader(
    "Selecione uma imagem para converter",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'],
    key="converter_uploader",
    help="Envie uma imagem para apenas converter o formato, sem redimensionar."
)

converter_output_format = st.sidebar.selectbox(
    "Formato de saída do conversor",
    ["JPEG", "PNG", "WEBP", "BMP", "TIFF"],
    index=1,
    help="Formato do arquivo convertido."
)

converter_quality = st.sidebar.slider(
    "Qualidade (para JPEG/WEBP)",
    min_value=10,
    max_value=100,
    value=90,
    step=5,
    help="Afeta apenas formatos com qualidade configurável (JPEG e WEBP)."
)

if converter_file is not None:
    try:
        conv_image = Image.open(converter_file)
        conv_original_format = conv_image.format or "Desconhecido"
        
        conv_col1, conv_col2 = st.columns(2)
        
        with conv_col1:
            st.subheader("🗂 Conversor de Imagens")
            st.image(conv_image, caption=f"Imagem original ({conv_original_format})", use_container_width=True)
            st.info(f"**Formato original:** {conv_original_format}\n\n**Dimensões:** {conv_image.width} x {conv_image.height} pixels")
        
        # Preparar conversão
        conv_buffer = io.BytesIO()
        conv_save_format = converter_output_format.upper()
        
        # Ajustar modo para formatos sem transparência
        conv_to_save = conv_image
        if conv_save_format in ["JPEG", "BMP"] and conv_image.mode in ["RGBA", "LA", "P"]:
            conv_to_save = conv_image.convert("RGB")
        
        save_kwargs = {}
        if conv_save_format in ["JPEG", "WEBP"]:
            save_kwargs["quality"] = int(converter_quality)
        
        conv_to_save.save(conv_buffer, format=conv_save_format, **save_kwargs)
        conv_buffer.seek(0)
        
        with conv_col2:
            st.subheader("📥 Download da imagem convertida")
            conv_file_name_base = converter_file.name.rsplit(".", 1)[0]
            conv_file_name = f"{conv_file_name_base}_convertida.{conv_save_format.lower()}"
            
            st.download_button(
                label=f"⬇️ Baixar imagem convertida ({conv_save_format})",
                data=conv_buffer,
                file_name=conv_file_name,
                mime=f"image/{conv_save_format.lower()}",
                type="primary",
            )
    except Exception as e:
        st.error(f"Erro ao converter a imagem: {str(e)}")
        st.info("Verifique se o arquivo enviado é uma imagem válida.")
