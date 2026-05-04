import os
import tempfile
import streamlit as st
import pandas as pd
from src.services.inference_service import run_audio_inference, run_image_inference
from src.services.regional_service import load_ebird_species

def render_upload():
    st.title("Ingreso de Datos al Sistema")
    st.caption("Gestiona los registros mediante carga masiva (CSV) o inferencia de IA en tiempo real.")

    tab1, tab2 = st.tabs(["Carga de Lotes (CSV)", "Inferencia en Tiempo Real (IA)"])

    with tab1:
        st.markdown(
            """
            <div class="section-card">
                <h3>Archivos requeridos</h3>
                <p>
                    Para ejecutar el análisis multimodal se necesitan registros acústicos, visuales,
                    catálogo de especies y zonas geográficas.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        audio_file = st.file_uploader("CSV de eventos acústicos", type=["csv"])
        visual_file = st.file_uploader("CSV de eventos visuales", type=["csv"])
        species_file = st.file_uploader("CSV de catálogo de especies", type=["csv"])
        zones_file = st.file_uploader("CSV de zonas geográficas", type=["csv"])

        if audio_file and visual_file and species_file and zones_file:
            audio_df = pd.read_csv(audio_file)
            visual_df = pd.read_csv(visual_file)
            species_df = pd.read_csv(species_file)
            zones_df = pd.read_csv(zones_file)

            st.session_state["custom_data"] = {
                "audio": audio_df,
                "visual": visual_df,
                "species": species_df,
                "zones": zones_df,
            }

            st.success("Datos cargados correctamente. Ya puedes ir a Análisis IA o Mapas de calor.")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Audio", len(audio_df))
            col2.metric("Visual", len(visual_df))
            col3.metric("Especies", len(species_df))
            col4.metric("Zonas", len(zones_df))

        else:
            st.info("Puedes seguir usando la data de prueba mientras no cargues archivos reales.")

    with tab2:
        st.markdown(
            """
            <div class="section-card">
                <h3>Identificación mediante IA</h3>
                <p>
                    Sube un audio de un canto (.mp3, .wav) o una imagen (.jpg, .png) capturada en campo. 
                    El modelo identificará la especie y validará su coherencia con eBird.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        col_input, col_result = st.columns(2)
        
        with col_input:
            file_type = st.radio("Tipo de archivo a analizar", ["Audio", "Imagen"], horizontal=True)
            
            if file_type == "Audio":
                uploaded_file = st.file_uploader("Sube el audio del canto", type=["mp3", "wav"])
            else:
                uploaded_file = st.file_uploader("Sube la fotografía del ave", type=["jpg", "jpeg", "png"])
            
            zones_df = st.session_state.get("custom_data", {}).get("zones")
            if zones_df is not None and not zones_df.empty:
                zone_options = dict(zip(zones_df["zone_id"], zones_df["nombre_zona"]))
                selected_zone_id = st.selectbox("Zona de la observación", options=list(zone_options.keys()), format_func=lambda x: zone_options[x])
            else:
                st.warning("No hay zonas cargadas en el sistema.")
                selected_zone_id = None
                
            analyze_btn = st.button("Analizar con IA", type="primary", disabled=not uploaded_file or not selected_zone_id)
        
        with col_result:
            if analyze_btn:
                with st.spinner("Procesando con red neuronal..."):
                    species_df = st.session_state["custom_data"]["species"]
                    
                    # Guardar archivo temporalmente para que BirdNET lo pueda leer
                    tmp_dir = os.path.join(os.getcwd(), ".tmp")
                    os.makedirs(tmp_dir, exist_ok=True)
                    tmp_file_path = os.path.join(tmp_dir, uploaded_file.name)
                    
                    with open(tmp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    if file_type == "Audio":
                        result = run_audio_inference(tmp_file_path, selected_zone_id, species_df)
                        
                        # Add to session state
                        new_row_df = pd.DataFrame([result])
                        st.session_state["custom_data"]["audio"] = pd.concat([st.session_state["custom_data"]["audio"], new_row_df], ignore_index=True)
                        conf_col = "confidence_audio"
                        
                    else:
                        result = run_image_inference(tmp_file_path, selected_zone_id, species_df)
                        
                        # Add to session state
                        new_row_df = pd.DataFrame([result])
                        st.session_state["custom_data"]["visual"] = pd.concat([st.session_state["custom_data"]["visual"], new_row_df], ignore_index=True)
                        conf_col = "confidence_visual"

                    # Get species name and check if it's new
                    sp_info_df = species_df[species_df["species_id"] == result["species_id"]]
                    if sp_info_df.empty:
                        # Especie no está en el catálogo local, la agregamos
                        sp_sci = result.get("_sci_name", "Desconocido")
                        sp_name = result.get("_com_name", sp_sci)
                        new_sp_df = pd.DataFrame([{
                            "species_id": result["species_id"],
                            "nombre_comun": sp_name,
                            "nombre_cientifico": sp_sci,
                            "familia": "Detectada por IA",
                            "habitat": "Automático",
                            "altitud_min": 0,
                            "altitud_max": 4000,
                            "modo_deteccion": "audio-visual"
                        }])
                        st.session_state["custom_data"]["species"] = pd.concat([species_df, new_sp_df], ignore_index=True)
                        species_df = st.session_state["custom_data"]["species"]
                    else:
                        sp_info = sp_info_df.iloc[0]
                        sp_name = sp_info["nombre_comun"]
                        sp_sci = sp_info["nombre_cientifico"]
                    
                    # Check regional coherence
                    ebird_df = load_ebird_species()
                    is_in_ebird = "No"
                    if not ebird_df.empty:
                        # Simple check if scientific name is in eBird
                        sci_names = ebird_df["nombre_cientifico"].str.lower().str.strip().tolist()
                        if sp_sci.lower().strip() in sci_names:
                            is_in_ebird = "Sí"
                    
                    st.success("¡Análisis completado!")
                    st.markdown(f"### {sp_name}")
                    st.caption(f"_{sp_sci}_")
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Confianza de IA", f"{int(result[conf_col]*100)}%")
                    
                    if is_in_ebird == "Sí":
                        c2.metric("Coherencia eBird", "Presente", help="Especie esperada en la región según datos recientes de eBird.")
                    else:
                        c2.metric("Coherencia eBird", "Inusual", delta="- Revisar", delta_color="inverse", help="Especie no registrada recientemente en eBird para esta zona.")
                        
                    st.info("El registro ha sido añadido al sistema y los mapas de calor se han actualizado automáticamente.")