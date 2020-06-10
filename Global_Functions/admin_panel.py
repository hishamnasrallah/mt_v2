from django.contrib import admin


class AfterSave(admin.ModelAdmin):

    def save_model(self, request: object, obj: object, form: object, change: object) -> object:
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        if getattr(obj, 'updated_by', None) is None:
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

