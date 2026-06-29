import streamlit as st

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
        return "Природный"
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

ОЧИСТКА И АККУРАТНАЯ ДОРАБОТКА:
Убрать из кадра только визуальный мусор, строительные остатки, случайные предметы, временные элементы и общий беспорядок. Допускаются только небольшие деликатные доработки, которые делают существующие постройки, покрытия, кромки, стыки и детали визуально более аккуратными, целостными и завершёнными. Не менять архитектуру, геометрию, объёмы, фасады, окна, террасы, дорожки, планировку участка, пропорции объектов, перспективу камеры и общую композицию сцены. Не делать редизайн и не переосмыслять архитектурные решения, а только мягко подчистить и слегка довести существующее состояние до более дорогого визуального вида.

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

CLEANUP AND SUBTLE FINISHING:
Remove only visual clutter, construction debris, random objects, temporary elements, and general mess from the scene. Allow only small, delicate refinements that make the existing buildings, surfaces, edges, joints, and details look cleaner, more cohesive, and more finished. Do not change the architecture, geometry, massing, facades, windows, terraces, paths, site layout, object proportions, camera perspective, or overall composition of the scene. Do not redesign or reinterpret the architecture; only perform a gentle cleanup and slight finishing pass for a more polished, premium-looking result.

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


st.title("🌿 Генератор мастер-промптов для ландшафтных водоёмов")
st.write("Заполни поля, и приложение соберёт готовый мастер-промпт на русском и английском, плюс короткий промпт для правок.")

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
        """
    )

col1, col2 = st.columns(2)

with col1:
    feature_type = st.selectbox("Тип объекта", FEATURE_TYPES)
    location = st.text_area("Расположение на участке", "Перед домом, справа от террасы")
    shape = st.text_area("Форма и геометрия", "Вытянутый водоём с мягкой береговой линией, неглубокими заходами и природной геометрией")
    styles = st.multiselect("Стили", STYLES, default=["Природный"])
    lighting = st.selectbox("Свет и атмосфера", LIGHTING)

with col2:
    materials = st.multiselect("Материалы", MATERIALS, default=["Натуральное дерево", "Крупные валуны", "Прибрежные злаки"])
    details = st.text_area("Дополнительные детали", "Чистая прозрачная вода, сдержанные посадки, благородные натуральные материалы")
    dont_change = st.text_area("Что нельзя менять", DEFAULT_DONT)
    focus = st.text_area("Критический акцент", "Максимально естественная интеграция в участок и убедительный премиальный реализм")
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

    tab1, tab2, tab3 = st.tabs(["RU prompt", "EN prompt", "Prompt для правки"])

    with tab1:
        st.text_area("Готовый промпт на русском", ru_prompt, height=520)
        st.download_button("Скачать RU prompt", ru_prompt, file_name="ru_prompt.txt")

    with tab2:
        st.text_area("Готовый промпт на английском", en_prompt, height=520)
        st.download_button("Скачать EN prompt", en_prompt, file_name="en_prompt.txt")

    with tab3:
        st.text_area("Короткий промпт для итерационной правки", edit_prompt, height=120)
        st.download_button("Скачать prompt для правки", edit_prompt, file_name="edit_prompt.txt")
else:
    st.info("Нажми «Собрать промпты», чтобы увидеть результат.")
