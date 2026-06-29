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
    "Премиальный минимализм",
    "Architectural landscape",
    "Editorial architectural photo",
    "High-end resort restraint",
    "Скандинавский",
    "Современный ландшафт",
    "Природный",
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
DEFAULT_FOCUS = (
    "Изображение должно выглядеть как high-end editorial architectural visualization: "
    "дорого, глубоко, чисто, выразительно, с благородной тональностью материалов, "
    "контролируемым светом, богатой пространственной глубиной и ощущением "
    "finished premium project без редизайна существующей архитектуры."
)
DEFAULT_PROBLEM_AREAS = "Слева терраса выглядит недостроенной; у дома убрать кучу древесины и строительных остатков; на настиле и по кромкам убрать мелкий визуальный мусор; общую подачу кадра сделать чище и благороднее."
DEFAULT_ALLOWED_FIXES = (
    "Удалить мусор и случайные предметы; визуально подчистить мелкие дефекты поверхностей; "
    "сделать материалы чище, ровнее и благороднее; усилить архитектурную выразительность кадра "
    "за счёт более дорогой тональности, более глубокого света, более чистых стыков, "
    "более собранной композиции посадок и более премиального ощущения finished project "
    "без изменения архитектуры и геометрии."
)


def join_items(items):
    return ", ".join([x.strip() for x in items if x and x.strip()])


def format_styles(styles):
    if not styles:
        return "Премиальный минимализм"
    return ", ".join([x.strip() for x in styles if x and x.strip()])


def architecture_lock_ru():
    return """СТРОГИЙ РЕЖИМ СОХРАНЕНИЯ АРХИТЕКТУРЫ:
Использовать исходное изображение как жёсткий референс и сохранить сцену максимально точно. Не менять архитектуру, геометрию, объёмы, контуры, фасады, окна, двери, кровли, террасы, дорожки, подпорные элементы, границы участка, крупные растения, ракурс камеры, перспективу, кадрирование и композицию. Не передвигать, не масштабировать, не перестраивать, не редизайнить и не переосмыслять никакие архитектурные элементы."""


def architecture_lock_en():
    return """STRICT ARCHITECTURE PRESERVATION MODE:
Use the original image as a hard reference and preserve the scene as exactly as possible. Do not change the architecture, geometry, massing, outlines, facades, windows, doors, roofs, terraces, paths, retaining elements, site boundaries, major planting, camera angle, perspective, framing, or overall composition. Do not move, resize, rebuild, redesign, or reinterpret any architectural element."""


def local_edits_ru(data):
    return f"""РАЗРЕШЕНЫ ТОЛЬКО СЛЕДУЮЩИЕ ЛОКАЛЬНЫЕ ПРАВКИ:
Проблемные зоны кадра: {data['problem_areas']}

Разрешённые локальные улучшения: {data['allowed_fixes']}

Всё, что не относится к перечисленным проблемным зонам, новому водоёму и удалению мусора, оставить без изменений."""


def local_edits_en(data):
    return f"""ONLY THE FOLLOWING LOCAL EDITS ARE ALLOWED:
Problem areas in the frame: {data['problem_areas']}

Allowed local improvements: {data['allowed_fixes']}

Everything not related to the listed problem areas, the new water feature, and clutter removal must remain unchanged."""


def build_cleanup_only_ru(data):
    return f"""ЗАДАЧА:
Аккуратно отредактировать существующую фотографию участка в режиме cleanup only: убрать визуальный мусор, локальные признаки незавершённости и улучшить только явно указанные проблемные зоны, не меняя архитектуру и общий дизайн сцены.

КОНТЕКСТ:
Сохранить существующий рельеф, архитектуру, деревья, перспективу камеры, направление света, сезонность и общую атмосферу фотографии. Итоговое изображение должно выглядеть как та же самая сцена после аккуратной профессиональной визуальной подготовки, без ощущения редизайна.

{architecture_lock_ru()}

{local_edits_ru(data)}

СВЕТ И АТМОСФЕРА:
{data['lighting']}. Свет должен выглядеть дорогим и художественно контролируемым, как в premium editorial architectural photography: мягкий объёмный свет, благородная тональность, чистый воздух, хорошая читаемость планов, выразительные тени, без серой мутности, без плоского пасмурного ощущения, без CGI-глянца.

РЕАЛИЗМ:
Строгий фотореализм. Сохранить правильный масштаб, перспективу, глубину, естественные отражения, контактные тени и правдоподобные текстуры всех существующих материалов. Изображение должно выглядеть не как обычный документальный снимок участка, а как high-end editorial architectural visualization: более выразительная композиция, более дорогая подача материалов, более собранная сценография и ощущение завершённого премиального проекта.

ЧТО НЕЛЬЗЯ:
{data['dont_change']}

КРИТИЧЕСКИЙ АКЦЕНТ:
Только cleanup и локальные микродоработки по указанным зонам без изменений архитектуры. {data['focus']}
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

{local_edits_ru(data)}

СВЕТ И АТМОСФЕРА:
{data['lighting']}. Свет должен выглядеть дорогим и художественно контролируемым, как в premium editorial architectural photography: мягкий объёмный свет, благородная тональность, чистый воздух, хорошая читаемость планов, выразительные тени, без серой мутности, без плоского пасмурного ощущения, без CGI-глянца.

РЕАЛИЗМ:
Строгий фотореализм. Сохранить правильный масштаб, перспективу, глубину, физику воды, естественные отражения, контактные тени, правдоподобные текстуры дерева, камня, грунта и растительности. Изображение должно выглядеть не как обычный реалистичный img2img-результат, а как high-end editorial architectural visualization: более выразительная композиция, более дорогая подача материалов, более благородная тональность, более собранная сценография и ощущение завершённого премиального проекта.

ЧТО НЕЛЬЗЯ:
{data['dont_change']}

КРИТИЧЕСКИЙ АКЦЕНТ:
Добавить только новый водоём и выполнить локальные правки по указанным проблемным зонам, не меняя существующую архитектуру. {data['focus']}
"""


def build_cleanup_only_en(data):
    return f"""TASK:
Carefully edit the existing site photo in cleanup-only mode: remove visual clutter, local signs of unfinished work, and improve only the explicitly listed problem areas without changing the architecture or the overall design of the scene.

CONTEXT:
Preserve the existing terrain, architecture, trees, camera perspective, light direction, season, and overall atmosphere of the original photo. The final image should look like the same scene after careful professional visual cleanup, not like a redesigned or regenerated project.

{architecture_lock_en()}

{local_edits_en(data)}

LIGHT AND MOOD:
{data['lighting']}. The light should feel expensive and artistically controlled, like premium editorial architectural photography: soft volumetric light, refined tonality, clean air, clear spatial readability, expressive shadows, no muddy gray cast, no flat overcast feel, no glossy CGI look.

REALISM:
Strict photorealism. Preserve accurate scale, perspective, depth, natural reflections, contact shadows, and believable textures of all existing materials. The result should look not like an ordinary documentary site photo, but like a high-end editorial architectural visualization with stronger composition, more premium material rendering, more controlled scene styling, and a finished premium-project feeling.

DO NOT:
{data['dont_change']}

KEY EMPHASIS:
Cleanup only and local micro-refinements in the listed areas, with no architectural changes. {data['focus']}
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

{local_edits_en(data)}

LIGHT AND MOOD:
{data['lighting']}. The light should feel expensive and artistically controlled, like premium editorial architectural photography: soft volumetric light, refined tonality, clean air, clear spatial readability, expressive shadows, no muddy gray cast, no flat overcast feel, no glossy CGI look.

REALISM:
Strict photorealism. Preserve accurate scale, perspective, depth, water physics, natural reflections, contact shadows, and believable textures of timber, stone, soil, and vegetation. The result should look not like an ordinary realistic img2img output, but like a high-end editorial architectural visualization with stronger composition, more premium material rendering, more refined tonality, more controlled scene styling, and a finished premium-project feeling.

DO NOT:
{data['dont_change']}

KEY EMPHASIS:
Add only the new water feature and perform only the listed local fixes without changing the existing architecture. {data['focus']}
"""


def build_edit_prompt(data, mode):
    if mode == "Cleanup only":
        return f"Измени только следующие проблемные зоны: {data['problem_areas']}. Разрешены только такие локальные правки: {data['allowed_fixes']}. Сделай подачу кадра более дорогой, глубокой и архитектурно выразительной, как в premium editorial architectural visualization. Всё остальное оставь без изменений. Не менять архитектуру, геометрию, объёмы, фасады, окна, дорожки, террасы, перспективу и композицию кадра."
    return f"Измени только новый водоём и следующие проблемные зоны: {data['problem_areas']}. Разрешены только такие локальные правки: {data['allowed_fixes']}. Сделай подачу кадра более дорогой, глубокой и архитектурно выразительной, как в premium editorial architectural visualization. Всё остальное оставь без изменений. Не менять архитектуру, геометрию, объёмы, фасады, окна, дорожки, террасы, перспективу и композицию кадра. Локальная правка: {data['edit_request']}."


st.title("🌿 Генератор мастер-промптов для ландшафтных водоёмов")
st.write("Версия без AI-усиления: точечные промпты для cleanup и добавления водоёма с жёстким сохранением архитектуры и более дорогой визуальной подачей.")

with st.sidebar:
    st.header("Режим")
    mode = st.radio("Что нужно сделать", ["Cleanup only", "Add water feature"], index=1)
    st.header("Как заполнять")
    st.markdown(
        """
- Укажи проблемные зоны кадра максимально предметно.
- Отдельно опиши, что именно разрешено улучшать локально.
- Cleanup only: только зачистка и локальные доработки без изменения архитектуры.
- Add water feature: добавить новый водоём и одновременно подчистить только указанные зоны.
- Для более дорогой картинки оставляй в стилях architectural и editorial формулировки.
        """
    )

col1, col2 = st.columns(2)

with col1:
    feature_type = st.selectbox("Тип объекта", FEATURE_TYPES, disabled=(mode == "Cleanup only"))
    location = st.text_area("Расположение на участке", "Перед домом, справа от террасы", disabled=(mode == "Cleanup only"))
    shape = st.text_area("Форма и геометрия", "Вытянутый водоём с мягкой береговой линией, неглубокими заходами и природной геометрией", disabled=(mode == "Cleanup only"))
    styles = st.multiselect(
        "Стили",
        STYLES,
        default=["Премиальный минимализм", "Architectural landscape", "Editorial architectural photo"]
    )
    lighting = st.selectbox("Свет и атмосфера", LIGHTING)
    problem_areas = st.text_area("Проблемные зоны кадра", DEFAULT_PROBLEM_AREAS, height=140)

with col2:
    materials = st.multiselect(
        "Материалы",
        MATERIALS,
        default=["Натуральное дерево", "Крупные валуны", "Прибрежные злаки"],
        disabled=(mode == "Cleanup only")
    )
    details = st.text_area(
        "Дополнительные детали",
        "Чистая вода с естественной глубиной и красивыми отражениями, layered planting, выразительные крупные камни, благородные натуральные материалы, дорогая архитектурная подача, ощущение finished premium landscape project",
        disabled=(mode == "Cleanup only")
    )
    allowed_fixes = st.text_area("Что разрешено улучшить локально", DEFAULT_ALLOWED_FIXES, height=140)
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
    "problem_areas": problem_areas,
    "allowed_fixes": allowed_fixes,
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
        st.text_area("Готовый промпт на русском", ru_prompt, height=620)
        st.download_button("Скачать RU prompt", ru_prompt, file_name="ru_prompt.txt")

    with tab2:
        st.text_area("Готовый промпт на английском", en_prompt, height=620)
        st.download_button("Скачать EN prompt", en_prompt, file_name="en_prompt.txt")

    with tab3:
        st.text_area("Короткий промпт для итерационной правки", edit_prompt, height=180)
        st.download_button("Скачать prompt для правки", edit_prompt, file_name="edit_prompt.txt")
else:
    st.info("Нажми «Собрать промпты», чтобы увидеть результат.")
