from graphviz import Digraph

dot = Digraph('ScheduleSystem', format='png')

# Увеличиваем размер холста в дюймах (ширина, высота)
dot.attr(size='12,12')

# Повышаем разрешение выхода — dpi для bitmap формата (по умолчанию 96)
dot.graph_attr.update(dpi='300')

# Увеличиваем размер шрифтов для узлов и толщину линий
dot.node_attr.update(fontsize='16')
dot.edge_attr.update(penwidth='2')

# Определяем узлы (классы)
dot.node('A', 'Автотранспортное\nпредприятие')
dot.node('B', 'Служба движения')
dot.node('C', 'Начальник\nпредприятия')
dot.node('D', 'Расписание\n(Маршрутное,\nПоездное,\nСтанционное)')
dot.node('E', 'Поезд\n(транспортное средство)')
dot.node('F', 'Механик')
dot.node('G', 'Техническое\nсостояние')
dot.node('H', 'Резервный поезд')
dot.node('I', 'Водитель')
dot.node('J', 'Наряд работы')

# Добавляем связи (отношения)
dot.edge('A', 'B', label='имеет')
dot.edge('A', 'C', label='имеет')
dot.edge('B', 'D', label='разрабатывает')
dot.edge('C', 'D', label='утверждает')
dot.edge('D', 'E', label='содержит')
dot.edge('E', 'G', label='имеет')
dot.edge('G', 'F', label='проверяется')
dot.edge('G', 'H', label='при неисправности\nзаменяется')
dot.edge('I', 'J', label='получает')
dot.edge('J', 'E', label='для эксплуатации')

# Сохраняем и создаём файл с изображением
dot.render('high_res_transport_schedule_diagram')
