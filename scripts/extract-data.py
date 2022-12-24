import ast
import astor
from glob import glob
import pandas as pd
paths = glob("point_e/**/*.py", recursive = True)
functions_name, functions_doc, functions_body , file_path = [] , [] , [], []
for path in paths:
  with open(path) as f:
    code = f.read()

  node = ast.parse(code)

  classes = [node for node in node.body if isinstance(node, ast.ClassDef)]
  functions = [node for node in node.body if isinstance(node, ast.FunctionDef)]
  for _class in classes:
      functions.extend([node for node in _class.body if isinstance(node, ast.FunctionDef)])
  for f in functions:
    source = astor.to_source(f)
    docstring = ast.get_docstring(f) if ast.get_docstring(f) else ''
    function = source.replace(ast.get_docstring(f, clean=False), '') if docstring else source
    functions_name.append(f.name)
    functions_doc.append(docstring)
    functions_body.append(function)
    file_path.append(path)

data_dict = {'function_name': functions_name, 'docstring': functions_doc, 'function_body': functions_body, 'file_path': file_path}
dataframe = pd.DataFrame(data = data_dict)
dataframe.to_csv('functions_data.csv', header=True, index=False)



