# Cf : https://medium.com/quantrium-tech/creating-a-hello-world-api-functionality-using-swagger-ui-and-python-42e2a5335ff0
# swagger_template = dict(
#     info = {
#         'title': LazyString(lambda: 'My first Swagger UI document'),
#         'version': LazyString(lambda: '0.1'),
#         'description': LazyString(lambda: 'This document depicts a sample Swagger UI document and implements Hello World functionality after executing GET.'),
#     },
#     host = LazyString(lambda: request.host))
#
# swagger_config = {
#     "headers": [],
#     "specs": [
#             {"endpoint": 'hello_world',
#             "route": '/hello_world.json',
#             "rule_filter": lambda rule: True,
#             "model_filter": lambda tag: True,
#             }
#     ],
#     "static_url_path": "/flasgger_static",
#     "swagger_ui": True,
#     "specs_route": "/apidocs/"}
