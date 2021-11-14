from json import load, dump

def gen_model(string, texture='default.png'):
  string = string.upper()

  string_len = 0
  for char in string:
    if char in len_dict:
      string_len += len_dict[char]
  start_point = int(string_len / 2 * -1) + len_dict[string[0]] / 2

  model = {'name': string.lower(), "texture": texture, "texture_size": [ 1000, 1000 ]}
  model['parts'] = []
  
  for i, char in enumerate(string):
    part = chars[char]
    if part:
      part['position'] = [start_point - ((32 - len_dict[char]) / 2), 0, 0]
      part['name'] = str(i)
      model['parts'].append(part.copy())
    start_point += len_dict[char]
    del part

  with open(f'models/{string.lower()}.mimodel', 'w+') as file:
    dump(model, file)

def gen_len(model):
  widths = {}
  for part in model['parts']:
    widths.update(iter_groups(part))
  return widths

def copy_chars(model):
  chars = {}
  for part in model['parts']:
    chars.update(iter_groups_copy(part))
  return chars

def iter_groups_copy(group):
  if 'shapes' in group:
    return {group['name']: group}
  elif 'parts' in group:
    widths = {}
    for part in group['parts']:
      widths.update(iter_groups_copy(part))
    return widths

def iter_groups(group):
  if 'shapes' in group:
    return {group['name']: widest_block(group['shapes'])}
  elif 'parts' in group:
    widths = {}
    for part in group['parts']:
      widths.update(iter_groups(part))
    return widths

def widest_block(shapes):
  widths = [abs(shape['from'][0]) + shape['to'][0] for shape in shapes if shape['type'] == 'block']
  return max(widths)

with open('mc_letters_default.mimodel') as file:
  model_dict = load(file)
len_dict = gen_len(model_dict)
chars = copy_chars(model_dict)
len_dict[' '] = 32
chars[' '] = {}
del model_dict

if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser(description='Generate Minecraft-styled .mimodel files.')
  parser.add_argument('-i','--input', nargs='+', help='What text to generate the .mimodel from.', required=True)
  parser.add_argument('-t','--texture', help='What texture file to use for the model.')
  args = parser.parse_args()
  if args.input:
    gen_model(' '.join(args.input))
