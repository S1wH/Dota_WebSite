from rest_framework.versioning import URLPathVersioning


class Version(URLPathVersioning):
    default_version = 'v1.0'
    allowed_versions = ('v1.0', 'v1.1')
    version_param = 'version'
