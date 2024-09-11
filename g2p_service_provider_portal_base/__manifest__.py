{
    "name": "G2P Service Provider Portal: Base",
    "category": "OpenG2P",
    "version": "17.0.1.2.1",
    "sequence": 1,
    "author": "OpenG2P (OpenSPP fork)",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "depends": ["account", "website"],
    "data": [
        "views/about_us.xml",
        "views/base.xml",
        "views/home.xml",
        "views/contact_us.xml",
        "views/login.xml",
        "views/profile.xml",
        "views/other.xml",
        "views/menu_view.xml",
        "views/service_provider_extend_view.xml",
    ],
    "assets": {
        "web.assets_frontend": [],
        "web.assets_common": [],
        "website.assets_wysiwyg": [],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
