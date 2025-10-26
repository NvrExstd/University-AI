import graphviz

# Создание графа с направлением слева направо и размером холста
causal_diagram = graphviz.Digraph('Ишикава', format='png')
causal_diagram.attr(rankdir='LR', size='12,10')
causal_diagram.graph_attr.update(dpi='300')
causal_diagram.node_attr.update(style='filled', fillcolor='lightblue', shape='box', fontsize='16')
causal_diagram.edge_attr.update(penwidth='2')

# Центральная проблема
causal_diagram.node('П', 'Недостаток управления проектами\nв компании "Медприбор"')

# Основные причины (ветви)
causal_diagram.node('У', 'Управление и организация')
causal_diagram.node('Пл', 'Планирование и оценка')
causal_diagram.node('Р', 'Ресурсы и кадры')
causal_diagram.node('Т', 'Технические сложности')
causal_diagram.node('В', 'Взаимодействие и коммуникации')
causal_diagram.node('О', 'Общая неопределённость')

# Связи к проблеме
for cause in ['У', 'Пл', 'Р', 'Т', 'В', 'О']:
    causal_diagram.edge('П', cause)

# Детализация для "Управление и организация"
causal_diagram.node('У1', 'Отсутствие уполномоченного органа')
causal_diagram.node('У2', 'Нет единой системы управления')
causal_diagram.edge('У', 'У1')
causal_diagram.edge('У', 'У2')

# Детализация для "Планирование и оценка"
causal_diagram.node('Пл1', 'Отсутствие оценки ценности проектов')
causal_diagram.node('Пл2', 'Нет стандартов и документов')
causal_diagram.edge('Пл', 'Пл1')
causal_diagram.edge('Пл', 'Пл2')

# Детализация для "Ресурсы и кадры"
causal_diagram.node('Р1', 'Недостаток инженерных специалистов')
causal_diagram.node('Р2', 'Отсутствие оборудования')
causal_diagram.edge('Р', 'Р1')
causal_diagram.edge('Р', 'Р2')

# Детализация для "Технические сложности"
causal_diagram.node('Т1', 'Проблемы с технологией и конструкцией')
causal_diagram.node('Т2', 'Неопределённые требования заказчика')
causal_diagram.edge('Т', 'Т1')
causal_diagram.edge('Т', 'Т2')

# Детализация для "Взаимодействие и коммуникации"
causal_diagram.node('В1', 'Разрозненное управление проектами')
causal_diagram.node('В2', 'Необходимость договоров с партнёрами')
causal_diagram.edge('В', 'В1')
causal_diagram.edge('В', 'В2')

# Детализация для "Общая неопределённость"
causal_diagram.node('О1', 'Отсутствует устав проекта')
causal_diagram.node('О2', 'Длительный поиск технических решений')
causal_diagram.edge('О', 'О1')
causal_diagram.edge('О', 'О2')

# Сохранение и отображение
causal_diagram.render('medpribor_ishikawa_diagram', view=True)
