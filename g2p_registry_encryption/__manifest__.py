{
    "name": "G2P Registry: Encryption",
    "category": "G2P",
    "version": "17.0.1.2.1",
    "sequence": 1,
    "author": "OpenG2P (OpenSPP fork)",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "depends": ["g2p_encryption", "g2p_registry_base", "g2p_registry_individual"],
    "data": [
        "data/registry_encryption_provider.xml",
        "views/decrypted_partner.xml",
        "views/encryption_provider.xml",
        "views/res_config_view.xml",
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_qweb": [],
    },
    "demo": [],
    "images": [],
    "application": False,
    "installable": True,
    "auto_install": False,
}
