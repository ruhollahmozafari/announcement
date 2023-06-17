from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ in order to access to updated fields in save method,\
        overwrite this method , can be used in all models in case of using signals 
        """

        if self.pk:
            # If self.pk is not None then it's an update.
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            # This will get the current model state since super().save() isn't called yet.
            # This gets the newly instantiated Mode object with the new values.
            new = self
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if (old_value := getattr(old, field_name)) != (
                        new_value := getattr(new, field_name)
                    ):
                        temp = {
                            "field": str(field_name),
                            "old": old_value,
                            "new": new_value,
                        }
                        temp = field_name
                        changed_fields.append(temp)
                except Exception as ex:  # Catch field does not exist exception
                    pass
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)


def show_duration(func):
    """just a decorator to show the duration of a method or function for debug usage"""
    import datetime as dt
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1 = dt.datetime.now()
        temp = func(*args, **kwargs)
        duration = dt.datetime.now() - t1
        dt.timedelta

        return temp

    return wrapper
