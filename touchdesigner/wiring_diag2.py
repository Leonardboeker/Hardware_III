"""TD deep diagnostic - lists EVERY child of /project1, identifies which .toe is open."""

print('--- which .toe is open? ---')
try:
    print('  project.name = ' + str(project.name))
except Exception as e:
    print('  project.name error: ' + str(e))
try:
    print('  project.folder = ' + str(project.folder))
except Exception as e:
    print('  project.folder error: ' + str(e))
try:
    # full file path of the .toe
    print('  project.filename = ' + str(getattr(project, 'filename', '?')))
except Exception as e:
    print('  project.filename error: ' + str(e))

print('--- direct children of /project1 (depth 1) ---')
try:
    children = list(op('/project1').children)
    print('  total children: ' + str(len(children)))
    for c in children[:50]:
        print('    ' + c.name + '  (type=' + str(c.type) + ')')
    if len(children) > 50:
        print('    ... and ' + str(len(children) - 50) + ' more')
except Exception as e:
    print('  error: ' + str(e))

print('--- everything in entire tree (depth 50, count by type) ---')
try:
    all_nodes = op('/').findChildren(depth=50)
    print('  total operators: ' + str(len(all_nodes)))
    # find any with "panel" or "method" in name
    matches = [n for n in all_nodes if 'panel' in n.name.lower() or 'method' in n.name.lower() or 'metric' in n.name.lower() or 'slider' in n.name.lower()]
    print('  panel/method/metric/slider matches: ' + str(len(matches)))
    for m in matches[:20]:
        print('    ' + m.path + '  (type=' + str(m.type) + ')')
except Exception as e:
    print('  error: ' + str(e))
