from django.db import models

from core.middleware.thread_user import CuserMiddleware

current_user = CuserMiddleware.get_user()


class AuditableQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_deleted=True)

    # def delete(self, **kwargs):
    #     kwargs['is_deleted'] = False
    #     kwargs['modified_on'] = datetime()
    #     kwargs['modified_by'] = current_user
    #     return self.update(**kwargs)
    #
    # def force_delete(self):
    #     return self.delete()
    #
    # def update(self, **kwargs):
    #     kwargs['modified_on'] = datetime()
    #     kwargs['modified_by'] = current_user
    #     return self.update(**kwargs)


class AuditableManager(models.Manager):
    def get_queryset(self):
        return AuditableQueryset(model=self.model, using=self._db, hints=self._hints)

    def active(self):
        return self.get_queryset().active()

    # def delete(self, **kwargs):
    #     return self.get_queryset().update(**kwargs)
    #
    # def force_delete(self):
    #     return self.get_queryset().force_delete()
    #
    # def update(self, **kwargs):
    #     return self.get_queryset().update(**kwargs)

