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
DEFAULT_FOCUS = "Максимально естественная интеграция в участок и убедительный фотореализм без редизайна существующей архитектуры."


def join_items(items):
    return ", ".join([x.strip() for x in items if x and x.strip()])


def format_styles(styles):
    if not styles:
        return "Природный"
    return ", ".join([x.strip() for x in styles if x and x.strip()])


def architecture_lock_ru():
    return """СТРОГИЙ РЕЖИМ СОХРАНЕНИЯ АРХИТЕКТУРЫ:
Использовать исходное изображение как жёсткий референс и сохранить сцену максимально точно. Не менять архитектуру, геометрию, объёмы, контуры, фасады, окна, двери, кровли, террасы, дорожки, подпорные элементы, границы участка, крупные растения, ракурс камеры, перспективу, кадрирование и композицию. Не передвигать, не масштабировать, не перестраивать, не редизайнить и не переосмыслять никакие архитектурные элементы.

РАЗРЕШЕНЫ ТОЛЬКО ЛОКАЛЬНЫЕ МИНИМАЛЬНЫЕ ПРАВКИ:
Удалить только визуальный мусор, строительные остатки, случайные предметы, временные элементы и мелкий беспорядок. Допускается только очень деликатная локальная подчистка небольших дефектов поверхности, стыков и кромок без изменения формы, материала, конструкции и дизайна объектов. Всё остальное оставить без изменений."""


def architecture_lock_en():
    return """STRICT ARCHITECTURE PRESERVATION MODE:
Use the original image as a hard reference and preserve the scene as exactly as possible. Do not change the architecture, geometry, massing, outlines, facades, windows, doors, roofs, terraces, paths, retaining elements, site boundaries, major planting, camera angle, perspective, framing, or overall composition. Do not move, resize, rebuild, redesign, or reinterpret any architectural element.

ONLY MINIMAL LOCAL EDITS ARE ALLOWED:
Remove only visual clutter, construction debris, random objects, temporary elements, and minor mess. Allow only extremely delicate local cleanup of small surface defects, joints, and edges without changing the shape, material, construction, or design of any object. Keep everything else unchanged."""


def build_cleanup_only_ru(data):
    return f"""ЗАДАЧА:
Аккуратно отредактировать существующую фотографию участка в режиме cleanup only: убрать визуальный мусор и мелкие следы незавершённости, не меняя архитектуру и общий дизайн сцены.

КОНТЕКСТ:
Сохранить существующий рельеф, архитектуру, деревья, перспективу камеры, направление света, сезонность и общую атмосферу фотографии. Итоговое изображение должно выглядеть как та же самая сцена после аккуратной профессиональной визуальной подготовки, без ощущения редизайна.

{architecture_lock_ru()}

СВЕТ И АТМОСФЕРА:
{data['lighting']}. Спокойная естественная атмосфера, натуральная палитра, без глянцевого CGI-эффекта.

РЕАЛИЗМ:
Строгий фотореализм. Сохранить правильный масштаб, перспективу, глубину, естественные отражения, контактные тени и правдоподобные текстуры всех существующих материалов. Изображение должно выглядеть как профессиональная архитектурная фотография той же самой сцены, а не как заново сгенерированный проект.

ЧТО НЕЛЬЗЯ:
{data['dont_change']}

КРИТИЧЕСКИЙ АКЦЕНТ:
Только cleanup и микродоработки без изменений архитектуры. {data['focus']}
"""


def build_add_water_feature_ru(data):
    duck_note = " Продумать мелководные зоны и спокойные участки берега, подходящие для уток." if data["feature_type"] == "Пруд для уток" else ""
    return f"""ЗАДАЧА:
Фотореалистично интегрировать новый объект ландшафтного дизайна в существующую фотографию участка так, чтобы он выглядел как реально построенный объект высокого уровня для коммерческого предложения, но без редизайна существующей архитектуры.

КОНТЕКСТ:
Сохранить существующий рельеф, архитектуру, деревья, перспективу камеры, направление света, сезонность и общую атмосферу фотографии. Новый объект должен быть органично вписан в существующее окружение, без ощущения коллажа или визуальной вставки.

ОБЪЕКТ:
Тип объекта: {data['feature_type']}.
Расположение: {data['location']}.
Форма и геометрия: {data['shape']}.

СТИЛЬ НОВОГО ОБЪЕКТА:
{data['styles']}, сдержанно, современно, натурально, без декоративной перегруженности.

МАТЕРИАЛЫ И ДЕТАЛИ НОВОГО ОБЪЕКТА:
{data['materials']}.
Дополнительные детали: {data['details']}.{duck_note}

{architecture_lock_ru()}

ДОПОЛНИТЕЛЬНОЕ ПРАВИЛО:
Всё, что не относится к новому водоёму и удалению мусора, оставить без изменений.

СВЕТ И АТМОСФЕРА:
{data['lighting']}. Спокойная естественная атмосфера, натуральная палитра, без глянцевого CGI-эффекта.

РЕАЛИЗМ:
Строгий фотореализм. Сохранить правильный масштаб, перспективу, глубину, физику воды, естественные отражения, контактные тени, правдоподобные текстуры дерева, камня, грунта и растительности. Изображение должно выглядеть как профессиональная архитектурная фотография уже реализованного объекта.

ЧТО НЕЛЬЗЯ:
{data['dont_change']}

КРИТИЧЕСКИЙ АКЦЕНТ:
Добавить только новый водоём и удалить визуальный мусор, не меняя существующую архитектуру. {data['focus']}
"""


def build_cleanup_only_en(data):
    return f"""TASK:
Carefully edit the existing site photo in cleanup-only mode: remove visual clutter and small signs of unfinished work without changing the architecture or the overall design of the scene.

CONTEXT:
Preserve the existing terrain, architecture, trees, camera perspective, light direction, season, and overall atmosphere of the original photo. The final image should look like the same scene after careful professional visual cleanup, not like a redesigned or regenerated project.

{architecture_lock_en()}

LIGHT AND MOOD:
{data['lighting']}. Calm natural atmosphere, natural palette, no glossy CGI look.

REALISM:
Strict photorealism. Preserve accurate scale, perspective, depth, natural reflections, contact shadows, and believable textures of all existing materials. The result should look like a professional architectural photograph of the exact same scene, not a newly generated redesign.

DO NOT:
{data['dont_change']}

KEY EMPHASIS:
Cleanup only and micro-refinements without architectural changes. {data['focus']}
"""


def build_add_water_feature_en(data):
    duck_note = " Include shallow edges and calm shoreline areas suitable for ducks." if data["feature_type"] == "Пруд для уток" else ""
    return f"""TASK:
Photorealistically integrate a new landscape water feature into the existing site photo so it looks like a real, built, high-quality project suitable for a commercial proposal, but without redesigning the existing architecture.

CONTEXT:
Preserve the existing terrain, architecture, trees, camera perspective, light direction, season, and overall atmosphere of the original photo. The new feature must feel naturally embedded into the environment, with no pasted-in or collage effect.

OBJECT:
Feature type: {data['feature_type']}.
Location: {data['location']}.
Shape and geometry: {data['shape']}.

STYLE OF THE NEW FEATURE:
{data['styles']}, restrained, contemporary, natural, without decorative excess.

MATERIALS AND DETAILS OF THE NEW FEATURE:
{data['materials']}.
Additional details: {data['details']}.{duck_note}

{architecture_lock_en()}

ADDITIONAL RULE:
Everything not related to the new water feature and clutter removal must remain unchanged.

LIGHT AND MOOD:
{data['lighting']}. Calm natural atmosphere, natural palette, no glossy CGI look.

REALISM:
Strict photorealism. Preserve accurate scale, perspective, depth, water physics, natural reflections, contact shadows, and believable textures of timber, stone, soil, and vegetation. The result should look like a professional architectural photograph of a built project.

DO NOT:
{data['dont_change']}

KEY EMPHASIS:
Add only the new water feature and remove visual clutter without changing the existing architecture. {data['focus']}
"""


def build_edit_prompt(data, mode):
    if mode == "Cleanup only":
        return "Измени только уборку визуального мусора и микродоработки мелких дефектов. Всё остальное оставь без изменений. Не менять архитектуру, геометрию, объёмы, фасады, окна, дорожки, террасы, перспективу и композицию кадра."
    return f"Измени только новый водоём и удаление визуального мусора, всё остальное оставь без изменений. Не менять архитектуру, геометрию, объёмы, фасады, окна, дорожки, террасы, перспективу и композицию кадра. Локальная правка: {data['edit_request']}."


st.title("🌿 Генератор мастер-промптов для ландшафтных водоёмов")
st.write("Версия без AI-усиления: приложение собирает готовые промпты с жёстким сохранением архитектуры и отдельными режимами работы.")

with st.sidebar:
    st.header("Режим")
    mode = st.radio("Что нужно сделать", ["Cleanup only", "Add water feature"], index=1)

    st.header("Как заполнять")
    st.markdown(
        """
- Cleanup only: только зачистка кадра и микродоработки без изменения архитектуры.
- Add water feature: добавить новый водоём, но сохранить существующую архитектуру.
- Можно выбрать несколько стилей сразу.
- Чем точнее описаны форма, расположение и ограничения, тем стабильнее результат.
        """
    )

col1, col2 = st.columns(2)

with col1:
    feature_type = st.selectbox("Тип объекта", FEATURE_TYPES, disabled=(mode == "Cleanup only"))
    location = st.text_area("Расположение на участке", "Перед домом, справа от террасы", disabled=(mode == "Cleanup only"))
    shape = st.text_area(
        "Форма и геометрия",
        "Вытянутый водоём с мягкой береговой линией, неглубокими заходами и природной геометрией",
        disabled=(mode == "Cleanup only")
    )
    styles = st.multiselect("Стили", STYLES, default=["Природный"])
    lighting = st.selectbox("Свет и атмосфера", LIGHTING)

with col2:
    materials = st.multiselect(
        "Материалы",
        MATERIALS,
        default=["Натуральное дерево", "Крупные валуны", "Прибрежные злаки"],
        disabled=(mode == "Cleanup only")
    )
    details = st.text_area(
        "Дополнительные детали",
        "Чистая прозрачная вода, сдержанные посадки, благородные натуральные материалы",
        disabled=(mode == "Cleanup only")
    )
    dont_change = st.text_area("Что нельзя менять", DEFAULT_DONT)
    focus = st.text_area("Критический акцент", DEFAULT_FOCUS)
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
    if mode == "Cleanup only":
        ru_prompt = build_cleanup_only_ru(form_data)
        en_prompt = build_cleanup_only_en(form_data)
    else:
        ru_prompt = build_add_water_feature_ru(form_data)
        en_prompt = build_add_water_feature_en(form_data)

    edit_prompt = build_edit_prompt(form_data, mode)

    tab1, tab2, tab3 = st.tabs(["RU prompt", "EN prompt", "Prompt для правки"])

    with tab1:
        st.text_area("Готовый промпт на русском", ru_prompt, height=560)
        st.download_button("Скачать RU prompt", ru_prompt, file_name="ru_prompt.txt")

    with tab2:
        st.text_area("Готовый промпт на английском", en_prompt, height=560)
        st.download_button("Скачать EN prompt", en_prompt, file_name="en_prompt.txt")

    with tab3:
        st.text_area("Короткий промпт для итерационной правки", edit_prompt, height=140)
        st.download_button("Скачать prompt для правки", edit_prompt, file_name="edit_prompt.txt")
else:
    st.info("Нажми «Собрать промпты», чтобы увидеть результат.")
