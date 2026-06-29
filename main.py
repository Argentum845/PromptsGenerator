import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Генератор промптов для водоёмов", page_icon="🌿", layout="wide")

FEATURE_TYPES = [
    "Плавательный пруд",
    "Декоративный пруд",
    "Каскад",
    "Ручей",
    "Пруд для уток",
    "Комбинированный водоём",
]

STYLES = [
    "Природный",
    "Скандинавский",
    "Премиальный минимализм",
    "Современный ландшафт",
    "Натуралистичный",
    "Архитектурный минимализм",
]

LIGHTING = [
    "Мягкий дневной свет",
    "Пасмурный рассеянный свет",
    "Спокойный вечерний свет",
]

MATERIALS = [
    "Натуральное дерево",
    "Крупные валуны",
    "Прибрежные злаки",
    "Осоки и водные растения",
    "Каменные ступени",
    "Минималистичная терраса",
]

DEFAULT_DONT = "Не менять ракурс камеры, дом, крупные деревья и фон. Без людей, без надписей, без логотипов, без чрезмерно бирюзовой воды, без курортного эффекта."


def join_items(items):
    return ", ".join([x.strip() for x in items if x and x.strip()])


def format_styles(styles):
    if not styles:
        return "Природный, скандинавский, премиальный минимализм"
    return ", ".join([x.strip() for x in styles if x and x.strip()])


def build_ru_prompt(data):
    duck_note = " Продумать мелководные зоны и спокойные участки берега, подходящие для уток." if data["feature_type"] == "Пруд для уток" else ""
    return f"""ЗАДАЧА:
Фотореалистично интегрировать новый объект ландшафтного дизайна в существующую фотографию участка так, чтобы он выглядел как реально построенный объект премиального уровня для коммерческого предложения.

КОНТЕКСТ:
Сохранить существующий рельеф, архитектуру, деревья, перспективу камеры, направление света, сезонность и общую атмосферу фотографии. Новый объект должен быть органично вписан в существующее окружение, без ощущения коллажа или визуальной вставки.

ОБЪЕКТ:
Тип объекта: {data['feature_type']}.
Расположение: {data['location']}.
Форма и геометрия: {data['shape']}.

СТИЛЬ:
{data['styles']}, дорого, сдержанно, современно, натурально, без декоративной перегруженности.

МАТЕРИАЛЫ И ДЕТАЛИ:
{data['materials']}.
Дополнительные детали: {data['details']}.{duck_note}

ОЧИСТКА И ДОРАБОТКА СЦЕНЫ:
Удалить с изображения весь визуальный мусор, строительные остатки, случайные предметы, временные элементы, беспорядок и всё, что удешевляет общий вид сцены. Все существующие сооружения, покрытия, дорожки, борта, лестницы, террасы, подпорные элементы и архитектурные детали должны выглядеть завершёнными, аккуратными, достроенными и конструктивно правдоподобными.

СВЕТ И АТМОСФЕРА:
{data['lighting']}. Спокойная премиальная атмосфера, естественная палитра, без глянцевого CGI-эффекта.

РЕАЛИЗМ:
Строгий фотореализм. Сохранить правильный масштаб, перспективу, глубину, физику воды, естественные отражения, контактные тени, правдоподобные текстуры дерева, камня, грунта и растительности. Изображение должно выглядеть как профессиональная архитектурная фотография уже реализованного объекта.

ЧТО НЕЛЬЗЯ:
{data['dont_change']}

КРИТИЧЕСКИЙ АКЦЕНТ:
{data['focus']}
"""


def build_en_prompt(data):
    duck_note = " Include shallow edges and calm shoreline areas suitable for ducks." if data["feature_type"] == "Пруд для уток" else ""
    return f"""TASK:
Photorealistically integrate a new landscape water feature into the existing site photo so it looks like a real, built, premium project suitable for a commercial proposal.

CONTEXT:
Preserve the existing terrain, architecture, trees, camera perspective, light direction, season, and overall atmosphere of the original photo. The new feature must feel naturally embedded into the environment, with no pasted-in or collage effect.

OBJECT:
Feature type: {data['feature_type']}.
Location: {data['location']}.
Shape and geometry: {data['shape']}.

STYLE:
{data['styles']}, refined, expensive-looking, contemporary, natural, without decorative excess.

MATERIALS AND DETAILS:
{data['materials']}.
Additional details: {data['details']}.{duck_note}

SCENE CLEANUP AND COMPLETION:
Remove all visual clutter, construction debris, random objects, temporary elements, mess, and anything that makes the scene feel unfinished or low-end. All existing structures, surfaces, paths, edges, stairs, decks, retaining elements, and architectural details should appear completed, refined, fully built, and constructionally believable.

LIGHT AND MOOD:
{data['lighting']}. Calm premium atmosphere, natural palette, no glossy CGI look.

REALISM:
Strict photorealism. Preserve accurate scale, perspective, depth, water physics, natural reflections, contact shadows, and believable textures of timber, stone, soil, and vegetation. The result should look like a professional architectural photo of a built project.

DO NOT:
{data['dont_change']}

KEY EMPHASIS:
{data['focus']}
"""


def build_edit_prompt(data):
    return f"Измени только {data['edit_request']}, всё остальное оставь без изменений. Сохрани ракурс, масштаб, перспективу, свет и общую атмосферу исходной сцены."


def enhance_prompt_with_ai(prompt_text, language="ru"):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if language == "ru":
        instructions = """
Ты — эксперт по улучшению промптов для генерации фотореалистичных изображений в ландшафтной архитектуре.

Твоя задача:
- НЕ отвечать на промпт
- НЕ описывать, что ты сделал
- НЕ добавлять пояснения
- вернуть ТОЛЬКО улучшенную версию промпта

Что нужно улучшить:
- сделать формулировки более точными и профессиональными
- усилить фотореализм
- усилить премиальный, природный, скандинавский стиль
- сохранить идею исходного промпта
- сохранить ограничения и запреты
- отдельно подчеркнуть очистку сцены от визуального мусора и завершённый вид всех сооружений
- не уводить сцену в CGI, resort, fantasy или overly stylized look
- не добавлять людей, текст, логотипы или лишние объекты
"""
    else:
        instructions = """
You are an expert prompt editor for photorealistic landscape architecture image generation.

Your task:
- DO NOT answer the prompt
- DO NOT explain anything
- DO NOT add commentary
- return ONLY the improved prompt

Improve the prompt by:
- making it more precise and professional
- strengthening photorealism
- strengthening the premium natural Scandinavian style
- preserving the original intent
- preserving all constraints and prohibitions
- explicitly reinforcing scene cleanup and the fully completed look of all structures
- avoiding CGI, resort, fantasy, or overly stylized looks
- not adding people, text, logos, or unnecessary objects
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=instructions,
        input=prompt_text,
    )

    return response.output_text.strip()


st.title("🌿 Генератор мастер-промптов для ландшафтных водоёмов")
st.write("Заполни поля, и приложение соберёт базовый мастер-промпт, а затем сможет усилить его через ИИ.")

with st.sidebar:
    st.header("Как заполнять")
    st.markdown(
        """
- Выбери тип водоёма.
- Коротко опиши, где он должен быть на фото.
- Выбери один или несколько стилей.
- Укажи форму, материалы и важные детали.
- Зафиксируй ограничения: что нельзя менять.
- При необходимости добавь фразу для локальной правки.
- Для усиления через ИИ добавь OPENAI_API_KEY в secrets приложения.
        """
    )

col1, col2 = st.columns(2)

with col1:
    feature_type = st.selectbox("Тип объекта", FEATURE_TYPES)
    location = st.text_area("Расположение на участке", "Перед домом, справа от террасы")
    shape = st.text_area("Форма и геометрия", "Вытянутый водоём с мягкой береговой линией, неглубокими заходами и природной геометрией")
    styles = st.multiselect("Стили", STYLES, default=["Природный", "Скандинавский"])
    lighting = st.selectbox("Свет и атмосфера", LIGHTING)

with col2:
    materials = st.multiselect("Материалы", MATERIALS, default=["Натуральное дерево", "Крупные валуны", "Прибрежные злаки"])
    details = st.text_area("Дополнительные детали", "Чистая прозрачная вода, сдержанные посадки, благородные натуральные материалы")
    dont_change = st.text_area("Что нельзя менять", DEFAULT_DONT)
    focus = st.text_area("Критический акцент", "Максимально естественная интеграция в участок, очистка сцены от мусора и убедительный премиальный реализм")
    edit_request = st.text_input("Если нужна локальная правка", "форму и линию берега водоёма")

form_data = {
    "feature_type": feature_type,
    "location": location,
    "shape": shape,
    "styles": format_styles(styles),
    "lighting": lighting,
    "materials": join_items(materials),
    "details": details,
    "dont_change": dont_change,
    "focus": focus,
    "edit_request": edit_request,
}

st.divider()

if st.button("Собрать промпты", type="primary"):
    ru_prompt = build_ru_prompt(form_data)
    en_prompt = build_en_prompt(form_data)
    edit_prompt = build_edit_prompt(form_data)

    st.session_state["ru_prompt"] = ru_prompt
    st.session_state["en_prompt"] = en_prompt
    st.session_state["edit_prompt"] = edit_prompt

if "ru_prompt" in st.session_state:
    tab1, tab2, tab3 = st.tabs(["RU prompt", "EN prompt", "Prompt для правки"])

    with tab1:
        st.text_area("Готовый промпт на русском", st.session_state["ru_prompt"], height=460)
        st.download_button("Скачать RU prompt", st.session_state["ru_prompt"], file_name="ru_prompt.txt")
        if st.button("Усилить RU prompt через ИИ"):
            try:
                with st.spinner("ИИ усиливает русский промпт..."):
                    st.session_state["improved_ru"] = enhance_prompt_with_ai(st.session_state["ru_prompt"], language="ru")
            except Exception as e:
                st.error(f"Не удалось усилить промпт: {e}")

        if "improved_ru" in st.session_state:
            st.text_area("Усиленный RU prompt", st.session_state["improved_ru"], height=460)
            st.download_button("Скачать усиленный RU prompt", st.session_state["improved_ru"], file_name="ru_prompt_improved.txt")

    with tab2:
        st.text_area("Готовый промпт на английском", st.session_state["en_prompt"], height=460)
        st.download_button("Скачать EN prompt", st.session_state["en_prompt"], file_name="en_prompt.txt")
        if st.button("Enhance EN prompt with AI"):
            try:
                with st.spinner("AI is enhancing the English prompt..."):
                    st.session_state["improved_en"] = enhance_prompt_with_ai(st.session_state["en_prompt"], language="en")
            except Exception as e:
                st.error(f"Could not enhance prompt: {e}")

        if "improved_en" in st.session_state:
            st.text_area("Enhanced EN prompt", st.session_state["improved_en"], height=460)
            st.download_button("Скачать усиленный EN prompt", st.session_state["improved_en"], file_name="en_prompt_improved.txt")

    with tab3:
        st.text_area("Короткий промпт для итерационной правки", st.session_state["edit_prompt"], height=120)
        st.download_button("Скачать prompt для правки", st.session_state["edit_prompt"], file_name="edit_prompt.txt")
else:
    st.info("Нажми «Собрать промпты», чтобы увидеть результат.")
