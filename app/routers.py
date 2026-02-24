class DatabaseRouter:
 
    MONGO_MODELS = {'searchlog'}
    MONGO_APP = 'app'
    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.MONGO_MODELS:
            return 'mongodb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.MONGO_MODELS:
            return 'mongodb'
        return 'default'



    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        if model_name in self.MONGO_MODELS:
            return db == 'mongodb'
        
        if db == 'mongodb':
            return False
    
        return db == 'default'