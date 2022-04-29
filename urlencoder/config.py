class CommonConfig(object):
    DEBUG = False


class DevelopmentConfig(CommonConfig):
    DEBUG = True


class ProductionConfig(CommonConfig):
    DEBUG = False
