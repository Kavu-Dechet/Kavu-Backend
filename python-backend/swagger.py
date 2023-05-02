from flasgger import Flasgger

swagger_template = dict(
    info={
        'title': 'KavuDechet API',
        'version': '1.0',
        'description': 'API documentation for KavuDechet application.',
    })

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'kavudechet_api_spec',
            "route": '/kavudechet_api_spec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
