{
    "name": "OpenID Connect Authentication",
    "version": "17.0.1.2.1",
    "author": "OpenG2P (OpenSPP fork)",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "external_dependencies": {"python": ["python-jose"]},
    "depends": ["auth_oauth"],
    "data": [
        "views/auth_oauth_templates.xml",
        "views/auth_oauth_provider.xml",
        "views/res_users.xml",
    ],
}
